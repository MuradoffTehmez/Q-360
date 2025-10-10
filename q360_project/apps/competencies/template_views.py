"""Template views for competencies app."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def competency_list(request):
    return render(request, 'competencies/competency_list.html')

@login_required
def my_skills(request):
    return render(request, 'competencies/my_skills.html')

@login_required
def competency_detail(request, pk):
    return render(request, 'competencies/competency_detail.html', {'competency_id': pk})

@login_required
def competency_manage(request):
    if not request.user.is_admin():
        return render(request, '403.html', status=403)
    return render(request, 'competencies/competency_list.html')
