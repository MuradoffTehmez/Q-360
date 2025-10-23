from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('', views.support_dashboard, name='dashboard'),
    path('create/', views.ticket_create, name='ticket_create'),
    path('<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('<int:pk>/close/', views.ticket_close, name='ticket_close'),
]
