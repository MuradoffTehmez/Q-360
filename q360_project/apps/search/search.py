"""
Global search functionality for Q360 system
Optimized with PostgreSQL Full-Text Search and Trigram indexes
"""
from django.contrib.postgres.search import (
    SearchVector, SearchQuery, SearchRank,
    TrigramSimilarity, SearchHeadline
)
from django.db.models import Q, F, Value, Count
from django.apps import apps
from django.conf import settings
from django.db import connection

def advanced_search(query, user=None, use_trigram=True, min_similarity=0.3):
    """
    Advanced search with PostgreSQL Full-Text Search and Trigram similarity.

    Args:
        query: Axtarış sorğusu
        user: İstifadəçi (icazə yoxlaması üçün)
        use_trigram: Trigram oxşarlığını istifadə et (fuzzy search)
        min_similarity: Minimum oxşarlıq dərəcəsi (0-1)

    Returns:
        Sıralanmış axtarış nəticələri
    """
    results = {}

    # Define searchable models and their search configuration
    search_configs = {
        'accounts.User': {
            'search_fields': ['first_name', 'last_name', 'username', 'email'],
            'trigram_fields': ['first_name', 'last_name', 'username'],
            'display_fields': ['get_full_name', 'email'],
            'title_field': 'get_full_name',
            'url_pattern': 'accounts:profile',
            'url_field': 'id'
        },
        'competencies.Competency': {
            'search_fields': ['name', 'description'],
            'trigram_fields': ['name'],
            'display_fields': ['name', 'description'],
            'title_field': 'name',
            'url_pattern': 'competencies:competency-detail',
            'url_field': 'id'
        },
        'training.TrainingResource': {
            'search_fields': ['title', 'description'],
            'trigram_fields': ['title'],
            'display_fields': ['title', 'description'],
            'title_field': 'title',
            'url_pattern': 'training:training-detail',
            'url_field': 'id'
        },
        'departments.Department': {
            'search_fields': ['name', 'description'],
            'trigram_fields': ['name'],
            'display_fields': ['name', 'description'],
            'title_field': 'name',
            'url_pattern': 'departments:detail',
            'url_field': 'id'
        },
        'evaluations.Question': {
            'search_fields': ['text'],
            'trigram_fields': ['text'],
            'display_fields': ['text'],
            'title_field': 'text',
            'url_pattern': 'evaluations:question-detail',
            'url_field': 'id'
        }
    }

    # For each model, perform advanced search
    for model_path, config in search_configs.items():
        try:
            app_label, model_name = model_path.split('.')
            model = apps.get_model(app_label, model_name)

            # Build FTS search vector
            search_vector = SearchVector(*config['search_fields'], config='azerbaijani')
            search_query = SearchQuery(query, config='azerbaijani')

            qs = model.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            )

            # Trigram similarity for fuzzy matching
            if use_trigram and config.get('trigram_fields'):
                # Calculate combined trigram similarity
                trigram_annotations = {}
                for i, field in enumerate(config['trigram_fields']):
                    trigram_annotations[f'similarity_{i}'] = TrigramSimilarity(field, query)

                qs = qs.annotate(**trigram_annotations)

                # Build OR filter for all trigram fields
                trigram_filter = Q()
                for i in range(len(config['trigram_fields'])):
                    trigram_filter |= Q(**{f'similarity_{i}__gte': min_similarity})

                # Combine FTS and trigram results
                qs = qs.filter(Q(search=search_query) | trigram_filter)

                # Calculate combined score (FTS rank + avg trigram similarity)
                similarity_sum = sum(F(f'similarity_{i}') for i in range(len(config['trigram_fields'])))
                qs = qs.annotate(
                    combined_score=F('rank') + (similarity_sum / len(config['trigram_fields']))
                )
                order_field = '-combined_score'
            else:
                # FTS only
                qs = qs.filter(search=search_query)
                order_field = '-rank'

            # Apply user permissions
            if user and hasattr(model, 'user'):
                qs = filter_by_user_permissions(qs, user, model)

            qs = qs.order_by(order_field)[:10]

            # Convert to result format with search highlighting
            results[model_name.lower()] = [
                {
                    'title': getattr(result, config['title_field'], str(result)),
                    'display_text': format_display_text(result, config['display_fields']),
                    'highlighted': generate_search_headline(result, config['search_fields'], query),
                    'url': get_object_url(result, config),
                    'model': model_name,
                    'score': getattr(result, 'combined_score', getattr(result, 'rank', 0))
                }
                for result in qs
            ]
        except LookupError:
            continue
        except Exception as e:
            # Log error but continue
            print(f"Search error for {model_path}: {str(e)}")
            continue

    return results


def global_search(query, user=None):
    """
    Perform global search across multiple model types.
    Wrapper for advanced_search with default settings.
    """
    return advanced_search(query, user=user, use_trigram=True, min_similarity=0.3)


def generate_search_headline(obj, search_fields, query):
    """
    PostgreSQL search headline ilə nəticə vurğulanması.

    Args:
        obj: Model obyekti
        search_fields: Axtarış sahələri
        query: Axtarış sorğusu

    Returns:
        Vurğulanmış mətn
    """
    headlines = []
    for field in search_fields[:2]:  # İlk 2 sahə
        try:
            if hasattr(obj, field):
                field_value = getattr(obj, field)
                if field_value:
                    # SearchHeadline istifadə edərək vurğulama
                    from django.contrib.postgres.search import SearchQuery
                    search_query = SearchQuery(query, config='azerbaijani')
                    headline = SearchHeadline(
                        Value(str(field_value)),
                        search_query,
                        start_sel='<mark>',
                        stop_sel='</mark>',
                        max_words=30,
                        min_words=15
                    )
                    headlines.append(str(headline))
        except:
            continue

    return ' ... '.join(headlines) if headlines else None


def optimize_search_indexes():
    """
    PostgreSQL üçün axtarış indekslərini optimallaşdırır.
    Bu funksiya migration fayllarında və ya management command-da istifadə edilməlidir.
    """
    with connection.cursor() as cursor:
        # pg_trgm extension aktivləşdir
        cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

        # Azərbaycan dili üçün FTS konfiqurasiyası
        try:
            cursor.execute("""
                CREATE TEXT SEARCH CONFIGURATION azerbaijani (COPY = simple);
            """)
        except:
            # Artıq mövcuddursa, xəta atmayacaq
            pass

    return True


def create_search_indexes_sql():
    """
    Axtarış indekslərini yaratmaq üçün SQL sorğuları qaytarır.
    Migration fayllarında istifadə üçün.
    """
    return [
        # User table trigram indexes
        "CREATE INDEX IF NOT EXISTS accounts_user_first_name_trgm_idx ON accounts_user USING gin (first_name gin_trgm_ops);",
        "CREATE INDEX IF NOT EXISTS accounts_user_last_name_trgm_idx ON accounts_user USING gin (last_name gin_trgm_ops);",
        "CREATE INDEX IF NOT EXISTS accounts_user_username_trgm_idx ON accounts_user USING gin (username gin_trgm_ops);",

        # Competency table trigram indexes
        "CREATE INDEX IF NOT EXISTS competencies_competency_name_trgm_idx ON competencies_competency USING gin (name gin_trgm_ops);",

        # Training table trigram indexes
        "CREATE INDEX IF NOT EXISTS training_trainingresource_title_trgm_idx ON training_trainingresource USING gin (title gin_trgm_ops);",

        # Department table trigram indexes
        "CREATE INDEX IF NOT EXISTS departments_department_name_trgm_idx ON departments_department USING gin (name gin_trgm_ops);",
    ]


class FacetedSearch:
    """
    Faceted search - Filter kombinasiyaları ilə təkmilləşdirilmiş axtarış.
    """

    def __init__(self, query='', models=None):
        """
        Initialize faceted search.

        Args:
            query: Axtarış sorğusu
            models: Axtarış ediləcək model list-i
        """
        self.query = query
        self.models = models or ['accounts.User', 'competencies.Competency', 'training.TrainingResource']
        self.filters = {}
        self.results = {}
        self.facets = {}

    def add_filter(self, facet_name, value):
        """
        Filter əlavə edir.

        Args:
            facet_name: Filter adı (role, department, status, date_range)
            value: Filter dəyəri
        """
        self.filters[facet_name] = value
        return self

    def execute(self):
        """
        Faceted search icra edir.

        Returns:
            Search results ilə birlikdə facet counts
        """
        from django.apps import apps

        for model_path in self.models:
            app_label, model_name = model_path.split('.')
            model = apps.get_model(app_label, model_name)

            # Base queryset
            qs = model.objects.all()

            # Apply text search
            if self.query:
                search_vector = SearchVector(*self._get_search_fields(model))
                search_query = SearchQuery(self.query, config='azerbaijani')
                qs = qs.annotate(search=search_vector).filter(search=search_query)

            # Apply facet filters
            for facet_name, value in self.filters.items():
                if hasattr(model, facet_name):
                    qs = qs.filter(**{facet_name: value})

            # Get results
            self.results[model_name.lower()] = list(qs[:50])

            # Calculate facets for this model
            self.facets[model_name.lower()] = self._calculate_facets(model, qs)

        return {
            'results': self.results,
            'facets': self.facets,
            'query': self.query,
            'filters': self.filters
        }

    def _get_search_fields(self, model):
        """Model üçün axtarış sahələrini qaytarır."""
        field_map = {
            'User': ['first_name', 'last_name', 'username', 'email'],
            'Competency': ['name', 'description'],
            'TrainingResource': ['title', 'description']
        }
        return field_map.get(model.__name__, ['name'])

    def _calculate_facets(self, model, queryset):
        """
        Facet counts hesablayır.

        Returns:
            Facet adı və count-ları
        """
        facets = {}

        # Role facets (for User model)
        if hasattr(model, 'role'):
            facets['role'] = queryset.values('role').annotate(count=Count('id'))

        # Department facets
        if hasattr(model, 'department'):
            facets['department'] = queryset.values('department__name').annotate(count=Count('id'))

        # Status facets
        if hasattr(model, 'is_active'):
            facets['is_active'] = queryset.values('is_active').annotate(count=Count('id'))

        # Date range facets (created_at)
        if hasattr(model, 'created_at'):
            from django.utils import timezone
            from datetime import timedelta

            now = timezone.now()
            facets['date_range'] = {
                'today': queryset.filter(created_at__date=now.date()).count(),
                'this_week': queryset.filter(created_at__gte=now - timedelta(days=7)).count(),
                'this_month': queryset.filter(created_at__gte=now - timedelta(days=30)).count(),
                'this_year': queryset.filter(created_at__year=now.year).count()
            }

        return facets


def global_search_old(query, user=None):
    """
    Old global search implementation (kept for backward compatibility).
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