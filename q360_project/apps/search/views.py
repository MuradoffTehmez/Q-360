"""
Search views for Q360 system
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from apps.accounts.models import User
from apps.competencies.models import Competency
from apps.training.models import TrainingResource
from apps.departments.models import Department


@login_required
def global_search_view(request):
    """
    Main search view that renders search results page
    """
    query = request.GET.get('q', '').strip()
    
    if query and len(query) >= 2:
        # Perform search across multiple models
        results = []
        
        # Search in users
        user_results = User.objects.annotate(
            search=SearchVector('first_name', 'last_name', 'username', 'email'),
            rank=SearchRank(SearchVector('first_name', 'last_name', 'username', 'email'), SearchQuery(query))
        ).filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(search=SearchQuery(query))
        ).order_by('-rank')[:10]
        
        for user in user_results:
            results.append({
                'title': user.get_full_name() or user.username,
                'content': f"İstifadəçi - {user.email}",
                'url': f'/accounts/profile/{user.id}/',
                'category': 'İstifadəçilər',
                'model': 'user',
                'rank': getattr(user, 'rank', 0)
            })
        
        # Search in competencies
        competency_results = Competency.objects.annotate(
            search=SearchVector('name', 'description'),
            rank=SearchRank(SearchVector('name', 'description'), SearchQuery(query))
        ).filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(search=SearchQuery(query))
        ).order_by('-rank')[:10]
        
        for comp in competency_results:
            results.append({
                'title': comp.name,
                'content': comp.description[:100] + '...' if len(comp.description) > 100 else comp.description,
                'url': f'/competencies/{comp.id}/',
                'category': 'Kompetensiyalar',
                'model': 'competency',
                'rank': getattr(comp, 'rank', 0)
            })
        
        # Search in training resources
        training_results = TrainingResource.objects.annotate(
            search=SearchVector('title', 'description'),
            rank=SearchRank(SearchVector('title', 'description'), SearchQuery(query))
        ).filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(search=SearchQuery(query))
        ).order_by('-rank')[:10]
        
        for training in training_results:
            results.append({
                'title': training.title,
                'content': training.description[:100] + '...' if len(training.description) > 100 else training.description,
                'url': f'/training/{training.id}/',
                'category': 'Təlimlər',
                'model': 'training',
                'rank': getattr(training, 'rank', 0)
            })
        
        # Search in departments
        department_results = Department.objects.annotate(
            search=SearchVector('name', 'description'),
            rank=SearchRank(SearchVector('name', 'description'), SearchQuery(query))
        ).filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(search=SearchQuery(query))
        ).order_by('-rank')[:10]
        
        for dept in department_results:
            results.append({
                'title': dept.name,
                'content': dept.description[:100] + '...' if len(dept.description) > 100 else dept.description,
                'url': f'/departments/{dept.id}/',
                'category': 'Şöbələr',
                'model': 'department',
                'rank': getattr(dept, 'rank', 0)
            })
        
        # Sort all results by rank
        results.sort(key=lambda x: x['rank'], reverse=True)
        total_results = len(results)
    else:
        results = []
        total_results = 0
    
    import json

    context = {
        'query': query,
        'results': results,
        'results_json': json.dumps(results) if results else '[]',
        'total_results': total_results,
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
@require_http_methods(["GET"])
def search_api(request):
    """
    API endpoint for search functionality
    """
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'error': 'Query must be at least 2 characters'}, status=400)
    
    results = []
    
    # Search in users
    user_results = User.objects.annotate(
        search=SearchVector('first_name', 'last_name', 'username', 'email'),
        rank=SearchRank(SearchVector('first_name', 'last_name', 'username', 'email'), SearchQuery(query))
    ).filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(username__icontains=query) |
        Q(email__icontains=query) |
        Q(search=SearchQuery(query))
    ).order_by('-rank')[:10]
    
    for user in user_results:
        results.append({
            'id': user.id,
            'title': user.get_full_name() or user.username,
            'content': f"İstifadəçi - {user.email}",
            'url': f'/accounts/profile/{user.id}/',
            'category': 'İstifadəçilər',
            'model': 'user',
            'rank': float(getattr(user, 'rank', 0))
        })
    
    # Search in competencies
    competency_results = Competency.objects.annotate(
        search=SearchVector('name', 'description'),
        rank=SearchRank(SearchVector('name', 'description'), SearchQuery(query))
    ).filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(search=SearchQuery(query))
    ).order_by('-rank')[:10]
    
    for comp in competency_results:
        results.append({
            'id': comp.id,
            'title': comp.name,
            'content': comp.description[:100] + '...' if len(comp.description) > 100 else comp.description,
            'url': f'/competencies/{comp.id}/',
            'category': 'Kompetensiyalar',
            'model': 'competency',
            'rank': float(getattr(comp, 'rank', 0))
        })
    
    # Search in training resources
    training_results = TrainingResource.objects.annotate(
        search=SearchVector('title', 'description'),
        rank=SearchRank(SearchVector('title', 'description'), SearchQuery(query))
    ).filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(search=SearchQuery(query))
    ).order_by('-rank')[:10]
    
    for training in training_results:
        results.append({
            'id': training.id,
            'title': training.title,
            'content': training.description[:100] + '...' if len(training.description) > 100 else training.description,
            'url': f'/training/{training.id}/',
            'category': 'Təlimlər',
            'model': 'training',
            'rank': float(getattr(training, 'rank', 0))
        })
    
    # Search in departments
    department_results = Department.objects.annotate(
        search=SearchVector('name', 'description'),
        rank=SearchRank(SearchVector('name', 'description'), SearchQuery(query))
    ).filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(search=SearchQuery(query))
    ).order_by('-rank')[:10]
    
    for dept in department_results:
        results.append({
            'id': dept.id,
            'title': dept.name,
            'content': dept.description[:100] + '...' if len(dept.description) > 100 else dept.description,
            'url': f'/departments/{dept.id}/',
            'category': 'Şöbələr',
            'model': 'department',
            'rank': float(getattr(dept, 'rank', 0))
        })
    
    # Sort all results by rank
    results.sort(key=lambda x: x['rank'], reverse=True)
    
    return JsonResponse({
        'query': query,
        'results': results,
        'count': len(results)
    })