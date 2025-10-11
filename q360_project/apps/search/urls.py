from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.global_search_view, name='search'),
    path('autocomplete/', views.search_autocomplete, name='autocomplete'),
    path('api/', views.search_api, name='api'),
]