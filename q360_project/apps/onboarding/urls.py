from django.urls import path

from . import views

app_name = "onboarding"

urlpatterns = [
    path("", views.OnboardingDashboardView.as_view(), name="dashboard"),
    path("dashboard/", views.OnboardingDashboardView.as_view(), name="dashboard"),
    path("processes/", views.OnboardingProcessListView.as_view(), name="process-list"),
    path("processes/new/", views.OnboardingProcessCreateView.as_view(), name="process-create"),
    path("processes/<int:pk>/", views.OnboardingProcessDetailView.as_view(), name="process-detail"),
    path("processes/<int:pk>/complete/", views.ProcessCompleteView.as_view(), name="process-complete"),
    path("processes/<int:pk>/cancel/", views.ProcessCancelView.as_view(), name="process-cancel"),
    path("processes/<int:pk>/note/", views.ProcessNoteView.as_view(), name="process-note"),
    path("processes/task/<int:pk>/complete/", views.CompleteTaskView.as_view(), name="task-complete"),
    path("templates/", views.OnboardingTemplateLibraryView.as_view(), name="template-library"),
    path("templates/new/", views.OnboardingTemplateFormView.as_view(), name="template-create"),
    path("templates/<slug:slug>/", views.OnboardingTemplateDetailView.as_view(), name="template-detail"),
    path("templates/<slug:slug>/edit/", views.OnboardingTemplateFormView.as_view(), name="template-edit"),
    path("templates/<slug:slug>/duplicate/", views.TemplateDuplicateView.as_view(), name="template-duplicate"),
    path("templates/<slug:slug>/delete/", views.TemplateDeleteView.as_view(), name="template-delete"),
]
