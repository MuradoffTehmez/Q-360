"""Template views for training app."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def my_trainings(request):
    return render(request, 'training/my_trainings.html')

@login_required
def catalog(request):
    return render(request, 'training/catalog.html')

@login_required
def training_detail(request, pk):
    return render(request, 'training/training_detail.html', {'training_id': pk})

@login_required
def training_manage(request):
    if not request.user.is_admin():
        return render(request, '403.html', status=403)
    return render(request, 'training/catalog.html')
