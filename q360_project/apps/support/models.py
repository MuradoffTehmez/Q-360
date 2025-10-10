"""Models for support/help desk system."""
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User


class SupportTicket(models.Model):
    """Support tickets for user issues and questions."""

    STATUS_CHOICES = [
        ('open', 'Açıq'),
        ('in_progress', 'İcrada'),
        ('resolved', 'Həll Edildi'),
        ('closed', 'Bağlandı'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Aşağı'),
        ('medium', 'Orta'),
        ('high', 'Yüksək'),
        ('urgent', 'Təcili'),
    ]

    title = models.CharField(max_length=200, verbose_name=_('Başlıq'))
    description = models.TextField(verbose_name=_('Təsvir'))
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open',
        verbose_name=_('Status')
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name=_('Prioritet')
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='support_tickets',
        verbose_name=_('Yaradan')
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets',
        verbose_name=_('Təyin Edildi')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaradılma Tarixi'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Yenilənmə Tarixi'))
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Həll Tarixi'))

    class Meta:
        verbose_name = _('Dəstək Sorğusu')
        verbose_name_plural = _('Dəstək Sorğuları')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"


class TicketComment(models.Model):
    """Comments on support tickets."""

    ticket = models.ForeignKey(
        SupportTicket,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Sorğu')
    )
    comment = models.TextField(verbose_name=_('Şərh'))
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Yaradan')
    )
    is_internal = models.BooleanField(
        default=False,
        verbose_name=_('Daxili Qeyd'),
        help_text=_('Yalnız support komandası üçün görünən')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaradılma Tarixi'))

    class Meta:
        verbose_name = _('Sorğu Şərhi')
        verbose_name_plural = _('Sorğu Şərhləri')
        ordering = ['created_at']

    def __str__(self):
        return f"{self.ticket.title} - Şərh"
