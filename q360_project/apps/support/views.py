"""
Support/Help Desk Views.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import SupportTicket, TicketComment


# ========================================
# Template-Based Views
# ========================================

@login_required
def support_dashboard(request):
    """Support dashboard - ticket list."""
    user = request.user
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    search_query = request.GET.get('search', '')

    # Base queryset
    if user.is_superadmin() or user.is_admin():
        tickets = SupportTicket.objects.all()
    else:
        tickets = SupportTicket.objects.filter(created_by=user)

    # Apply filters
    if status_filter:
        tickets = tickets.filter(status=status_filter)
    if priority_filter:
        tickets = tickets.filter(priority=priority_filter)
    if search_query:
        tickets = tickets.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    tickets = tickets.select_related('created_by', 'assigned_to').order_by('-created_at')
    paginator = Paginator(tickets, 20)
    tickets_page = paginator.get_page(request.GET.get('page'))

    # Statistics
    user_filter = {} if user.is_admin() else {'created_by': user}
    stats = {
        'total': SupportTicket.objects.filter(**user_filter).count(),
        'open': SupportTicket.objects.filter(status='open', **user_filter).count(),
        'in_progress': SupportTicket.objects.filter(status='in_progress', **user_filter).count(),
        'resolved': SupportTicket.objects.filter(status='resolved', **user_filter).count(),
    }

    return render(request, 'support/dashboard.html', {
        'tickets': tickets_page,
        'stats': stats,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'search_query': search_query,
    })


@login_required
def ticket_create(request):
    """Create new support ticket."""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority', 'medium')

        ticket = SupportTicket.objects.create(
            title=title,
            description=description,
            priority=priority,
            created_by=request.user
        )

        messages.success(request, 'Dəstək sorğusu yaradıldı.')
        return redirect('support:ticket_detail', pk=ticket.pk)

    return render(request, 'support/ticket_form.html')


@login_required
def ticket_detail(request, pk):
    """View ticket details."""
    ticket = get_object_or_404(SupportTicket, pk=pk)

    if not (request.user.is_admin() or ticket.created_by == request.user or ticket.assigned_to == request.user):
        messages.error(request, 'Bu ticketə baxmaq icazəniz yoxdur.')
        return redirect('support:dashboard')

    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            TicketComment.objects.create(
                ticket=ticket,
                user=request.user,
                comment=comment_text
            )
            messages.success(request, 'Şərh əlavə edildi.')
            return redirect('support:ticket_detail', pk=pk)

    comments = ticket.comments.select_related('user').order_by('created_at')

    return render(request, 'support/ticket_detail.html', {
        'ticket': ticket,
        'comments': comments,
    })


@login_required
def ticket_close(request, pk):
    """Close ticket."""
    ticket = get_object_or_404(SupportTicket, pk=pk)

    if request.user.is_admin() or ticket.created_by == request.user:
        ticket.status = 'closed'
        ticket.save()
        messages.success(request, 'Ticket bağlandı.')
    else:
        messages.error(request, 'İcazəniz yoxdur.')

    return redirect('support:ticket_detail', pk=pk)
