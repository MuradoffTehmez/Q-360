"""Template views for audit app."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def security_dashboard(request):
    if not request.user.is_admin():
        return render(request, '403.html', status=403)
    return render(request, 'audit/security_dashboard.html')
