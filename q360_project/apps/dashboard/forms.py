from django import forms
from django.utils.translation import gettext_lazy as _
from .models import SystemKPI, DashboardWidget, AnalyticsReport


class DashboardWidgetForm(forms.ModelForm):
    """
    Dashboard widget konfiqurasiyası forması
    """
    class Meta:
        model = DashboardWidget
        fields = ['name', 'widget_type', 'title', 'description', 'order', 'is_active', 'config']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'widget_type': forms.Select(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'config': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'name': _('Widget Adı'),
            'widget_type': _('Widget Növü'),
            'title': _('Başlıq'),
            'description': _('Təsvir'),
            'order': _('Göstərmə Sırası'),
            'is_active': _('Aktivdir'),
            'config': _('Konfiqurasiya'),
        }


class AnalyticsReportForm(forms.ModelForm):
    """
    Analitik hesabat forması
    """
    class Meta:
        model = AnalyticsReport
        fields = ['name', 'report_type', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'report_type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'name': _('Hesabat Adı'),
            'report_type': _('Hesabat Növü'),
            'start_date': _('Başlama Tarixi'),
            'end_date': _('Bitmə Tarixi'),
        }


class KPICreationForm(forms.ModelForm):
    """
    KPI yaratma forması
    """
    class Meta:
        model = SystemKPI
        fields = ['name', 'kpi_type', 'value', 'target', 'unit', 'period_start', 'period_end']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'kpi_type': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
            'target': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'period_start': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'period_end': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
        labels = {
            'name': _('KPI Adı'),
            'kpi_type': _('KPI Növü'),
            'value': _('Dəyər'),
            'target': _('Hədəf'),
            'unit': _('Vahid'),
            'period_start': _('Dövr Başlanğıcı'),
            'period_end': _('Dövr Sonu'),
        }