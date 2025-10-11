"""
Global search functionality for Q360 system
"""
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q, F
from django.apps import apps
from django.conf import settings

def global_search(query, user=None):
    """
    Perform global search across multiple model types
    """
    results = {}
    
    # Define searchable models and their search configuration
    search_configs = {
        'accounts.User': {
            'search_fields': ['first_name', 'last_name', 'username', 'email'],
            'display_fields': ['get_full_name', 'email'],
            'title_field': 'get_full_name',
            'url_pattern': 'accounts:profile',  # This needs to be dynamic
            'url_field': 'id'
        },
        'competencies.Competency': {
            'search_fields': ['name', 'description'],
            'display_fields': ['name', 'description'],
            'title_field': 'name',
            'url_pattern': 'competencies:competency-detail',
            'url_field': 'id'
        },
        'training.TrainingResource': {
            'search_fields': ['title', 'description'],
            'display_fields': ['title', 'description'],
            'title_field': 'title',
            'url_pattern': 'training:training-detail',
            'url_field': 'id'
        },
        'departments.Department': {
            'search_fields': ['name', 'description'],
            'display_fields': ['name', 'description'],
            'title_field': 'name',
            'url_pattern': 'departments:detail',
            'url_field': 'id'
        },
        'evaluations.Question': {
            'search_fields': ['text'],
            'display_fields': ['text'],
            'title_field': 'text',
            'url_pattern': 'evaluations:question-detail',
            'url_field': 'id'
        }
    }
    
    # For each model, perform search and collect results
    for model_path, config in search_configs.items():
        try:
            app_label, model_name = model_path.split('.')
            model = apps.get_model(app_label, model_name)
            
            # Build search vector from configured fields
            search_vector = SearchVector(*config['search_fields'])
            search_query = SearchQuery(query)
            
            # Apply permission filters based on user
            qs = model.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')
            
            # Apply additional permissions if user is provided
            if user and hasattr(model, 'user'):
                if hasattr(model, 'user_can_view'):
                    # If model has custom permission method
                    qs = [obj for obj in qs if obj.user_can_view(user)]
                else:
                    # Default: filter by visibility based on user role
                    qs = filter_by_user_permissions(qs, user, model)
            
            # Convert to result format
            results[model_name.lower()] = [
                {
                    'title': getattr(result, config['title_field'], str(result)),
                    'display_text': format_display_text(result, config['display_fields']),
                    'url': get_object_url(result, config),
                    'model': model_name,
                    'rank': getattr(result, 'rank', 1)
                }
                for result in qs[:10]  # Limit to top 10 results per model
            ]
        except LookupError:
            # Model doesn't exist, skip it
            continue
    
    return results

def format_display_text(obj, fields):
    """
    Format display text from specified fields
    """
    parts = []
    for field in fields:
        try:
            if hasattr(obj, field):
                value = getattr(obj, field)
                if callable(value):
                    value = value()
                if value:
                    parts.append(str(value))
        except:
            continue
    return ' | '.join(parts[:2])  # Limit to first 2 fields

def get_object_url(obj, config):
    """
    Generate URL for search result object
    """
    try:
        # This is a simplified URL generation - in real implementation
        # you'd need to properly reverse URLs
        url_field_val = getattr(obj, config['url_field'])
        return f"/{config['url_field']}/{url_field_val}/"
    except:
        return "#"

def filter_by_user_permissions(qs, user, model):
    """
    Apply basic permission filtering based on user role
    """
    # This is a generic implementation - specific models may need custom logic
    if model.__name__ == 'User':
        # Users can typically only see active users
        if hasattr(model, 'is_active'):
            qs = qs.filter(is_active=True)
    
    # For evaluation-related models, apply appropriate filters
    # This would depend on the model and user permissions
    
    return qs

def simple_search(query, model_classes=None):
    """
    Simple search across specified model classes
    """
    if model_classes is None:
        # Default to most commonly searched models
        model_classes = [
            apps.get_model('accounts', 'User'),
            apps.get_model('competencies', 'Competency'),
            apps.get_model('training', 'TrainingResource'),
        ]
    
    results = []
    query_obj = SearchQuery(query)
    
    for model_class in model_classes:
        # Build search vector - we'll search in the most standard fields
        search_fields = []
        
        # Determine appropriate search fields based on model
        if model_class._meta.model_name == 'user':
            search_fields = ['first_name', 'last_name', 'username', 'email']
        elif hasattr(model_class, 'name'):
            search_fields = ['name']
            if hasattr(model_class, 'title'):
                search_fields.append('title')
            if hasattr(model_class, 'description'):
                search_fields.append('description')
        elif hasattr(model_class, 'title'):
            search_fields = ['title']
            if hasattr(model_class, 'description'):
                search_fields.append('description')
        else:
            # Use all text fields
            search_fields = [
                field.name for field in model_class._meta.fields 
                if field.get_internal_type() in ['CharField', 'TextField']
                and field.name not in ['password', 'api_key', 'token']
            ]
        
        # Only proceed if we have searchable fields
        if search_fields:
            search_vector = SearchVector(*search_fields[:4])  # Limit to first 4 fields
            
            model_results = model_class.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, query_obj)
            ).filter(search=query_obj).order_by('-rank')[:10]
            
            for result in model_results:
                results.append({
                    'object': result,
                    'model_name': model_class._meta.model_name,
                    'app_label': model_class._meta.app_label,
                    'title': get_search_result_title(result),
                    'content_snippet': get_search_result_content(result, search_fields),
                    'rank': getattr(result, 'rank', 0),
                    'url': get_search_result_url(result)
                })
    
    # Sort all results by rank
    results.sort(key=lambda x: x['rank'], reverse=True)
    return results

def get_search_result_title(obj):
    """
    Get an appropriate title for the search result
    """
    # Try common title fields in order of preference
    for field in ['title', 'name', 'first_name', 'last_name', 'username', 'email']:
        if hasattr(obj, field):
            value = getattr(obj, field)
            if value:
                if callable(value):
                    return str(value())
                return str(value)
    
    # If no common field is found, use string representation
    return str(obj)

def get_search_result_content(obj, search_fields):
    """
    Get content snippet for search result
    """
    content_parts = []
    
    for field_name in search_fields[:2]:  # Get first 2 fields as content
        if hasattr(obj, field_name):
            value = getattr(obj, field_name)
            if value and str(value).strip():
                if callable(value):
                    value = value()
                content_parts.append(str(value)[:100])  # Limit to 100 chars
    
    return '... '.join(content_parts)

def get_search_result_url(obj):
    """
    Generate URL for search result - this would need to be customized per model
    """
    model_name = obj._meta.model_name
    app_label = obj._meta.app_label
    
    # Default URL patterns (would need to be customized per project)
    if model_name == 'user':
        return f'/accounts/profile/{getattr(obj, "id", "")}/'
    elif model_name == 'competency':
        return f'/competencies/{getattr(obj, "id", "")}/'
    elif model_name == 'trainingresource':
        return f'/training/{getattr(obj, "id", "")}/'
    elif model_name == 'department':
        return f'/departments/{getattr(obj, "id", "")}/'
    
    return f'/{app_label}/{model_name}/{getattr(obj, "id", "")}/'