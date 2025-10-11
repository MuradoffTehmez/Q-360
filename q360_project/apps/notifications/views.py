"""
Search views for Q360 system
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .search import simple_search
from apps.accounts.models import User
from apps.competencies.models import Competency
from apps.training.models import TrainingResource
from apps.departments.models import Department
from django.contrib.postgres.search import SearchVector
from django.db.models import Q


@login_required
def global_search_view(request):
    """
    Main search view that renders search results page
    """
    query = request.GET.get('q', '').strip()
    
    if query:
        # Perform search
        results = simple_search(
            query, 
            model_classes=[
                User, 
                Competency, 
                TrainingResource,
                Department
            ]
        )
        
        # Limit results for display
        context = {
            'query': query,
            'results': results[:50],  # Show max 50 results
            'total_results': len(results),
        }
    else:
        context = {
            'query': '',
            'results': [],
            'total_results': 0,
        }
    
    return render(request, 'search/results.html', context)


@login_required
@require_http_methods(["GET"])
def search_autocomplete(request):
    """
    AJAX endpoint for search autocomplete
    """
    query = request.GET.get('q', '').strip()
    results = []
    
    if len(query) >= 2:  # Only search if query is at least 2 characters
        # Search in users
        user_results = User.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query) |
            Q(email__icontains=query)
        )[:5]
        
        for user in user_results:
            results.append({
                'title': user.get_full_name() or user.username,
                'content': f"İstifadəçi - {user.email}",
                'url': f'/accounts/profile/{user.id}/',
                'category': 'İstifadəçilər'
            })
        
        # Search in competencies
        competency_results = Competency.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )[:5]
        
        for comp in competency_results:
            results.append({
                'title': comp.name,
                'content': comp.description[:100] + '...' if len(comp.description) > 100 else comp.description,
                'url': f'/competencies/{comp.id}/',
                'category': 'Kompetensiyalar'
            })
        
        # Search in training resources
        training_results = TrainingResource.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )[:5]
        
        for training in training_results:
            results.append({
                'title': training.title,
                'content': training.description[:100] + '...' if len(training.description) > 100 else training.description,
                'url': f'/training/{training.id}/',
                'category': 'Təlimlər'
            })
    
    return JsonResponse({'results': results, 'query': query})


@login_required
@csrf_exempt
def search_api(request):
    """
    API endpoint for search functionality
    """
    if request.method == 'GET':
        query = request.GET.get('q', '').strip()
        model = request.GET.get('model', None)  # Optional model filter
        
        if len(query) < 2:
            return JsonResponse({'error': 'Query must be at least 2 characters'}, status=400)
        
        results = []
        
        # Search based on model parameter or search all
        if model == 'user':
            search_results = User.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(username__icontains=query) |
                Q(email__icontains=query)
            )[:10]
            
            for user in search_results:
                results.append({
                    'id': user.id,
                    'title': user.get_full_name() or user.username,
                    'content': user.email,
                    'model': 'user',
                    'url': f'/accounts/profile/{user.id}/'
                })
        elif model == 'competency':
            search_results = Competency.objects.annotate(
                search=SearchVector('name', 'description')
            ).filter(search=query)[:10]
            
            for comp in search_results:
                results.append({
                    'id': comp.id,
                    'title': comp.name,
                    'content': comp.description[:100] + '...' if len(comp.description) > 100 else comp.description,
                    'model': 'competency',
                    'url': f'/competencies/{comp.id}/'
                })
        elif model == 'training':
            search_results = TrainingResource.objects.annotate(
                search=SearchVector('title', 'description')
            ).filter(search=query)[:10]
            
            for training in search_results:
                results.append({
                    'id': training.id,
                    'title': training.title,
                    'content': training.description[:100] + '...' if len(training.description) > 100 else training.description,
                    'model': 'training',
                    'url': f'/training/{training.id}/'
                })
        else:
            # Search all models if no specific model requested
            all_results = simple_search(query)
            for result in all_results[:20]:  # Limit total results
                results.append({
                    'id': getattr(result['object'], 'id', None),
                    'title': result['title'],
                    'content': result['content_snippet'],
                    'model': result['model_name'],
                    'url': result['url']
                })
        
        return JsonResponse({
            'query': query,
            'results': results,
            'count': len(results)
        })
    
    return JsonResponse({'error': 'Only GET method allowed'}, status=405)