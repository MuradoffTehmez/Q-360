"""Forms for notification preferences in the notifications app."""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import UserNotificationPreference


class NotificationPreferenceForm(forms.ModelForm):
    """
    Form for user notification preferences.
    """
    class Meta:
        model = UserNotificationPreference
        fields = [
            # Email preferences
            'email_notifications', 'email_assignment', 'email_reminder', 
            'email_announcement', 'email_security',
            # SMS preferences
            'sms_notifications', 'sms_important_only', 'sms_assignment', 
            'sms_reminder', 'sms_security',
            # Push preferences
            'push_notifications', 'push_assignment', 'push_reminder', 'push_announcement',
            # Schedule preferences
            'dnd_start_time', 'dnd_end_time', 'weekend_notifications',
            'weekday_start', 'weekday_end'
        ]
        widgets = {
            'dnd_start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'dnd_end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'weekday_start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'weekday_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add CSS classes to all fields
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
        
        # Set custom labels in Azerbaijani
        self.fields['email_notifications'].label = _("E-poçt Bildirişləri")
        self.fields['email_assignment'].label = _("Tapşırıq Bildirişləri")
        self.fields['email_reminder'].label = _("Xatırlatma Bildirişləri")
        self.fields['email_announcement'].label = _("Elan Bildirişləri")
        self.fields['email_security'].label = _("Təhlükəsizlik Bildirişləri")
        
        self.fields['sms_notifications'].label = _("SMS Bildirişləri")
        self.fields['sms_important_only'].label = _("Yalnız Vacib Bildirişlər")
        self.fields['sms_assignment'].label = _("Tapşırıq Bildirişləri")
        self.fields['sms_reminder'].label = _("Xatırlatma Bildirişləri")
        self.fields['sms_security'].label = _("Təhlükəsizlik Bildirişləri")
        
        self.fields['push_notifications'].label = _("Push Bildirişləri")
        self.fields['push_assignment'].label = _("Tapşırıq Bildirişləri")
        self.fields['push_reminder'].label = _("Xatırlatma Bildirişləri")
        self.fields['push_announcement'].label = _("Elan Bildirişləri")
        
        self.fields['dnd_start_time'].label = _("Sakitlik Rejimi - Başlama Saatı")
        self.fields['dnd_end_time'].label = _("Sakitlik Rejimi - Bitmə Saatı")
        self.fields['weekend_notifications'].label = _("Həftə Sonu Bildirişləri")
        self.fields['weekday_start'].label = _("İş Günü Bildirişləri - Başlama")
        self.fields['weekday_end'].label = _("İş Günü Bildirişləri - Bitmə")


class SMSProviderForm(forms.Form):
    """
    Form for SMS provider configuration.
    """
    PROVIDER_CHOICES = [
        ('twilio', _('Twilio')),
        ('aws_sns', _('AWS SNS')),
        ('clickatell', _('Clickatell')),
        ('custom', _('Fərdi')),
    ]
    
    provider = forms.ChoiceField(
        choices=PROVIDER_CHOICES,
        label=_("Təchizatçı"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    name = forms.CharField(
        max_length=100,
        label=_("Ad"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    # Twilio-specific fields
    account_sid = forms.CharField(
        max_length=100,
        required=False,
        label=_("Account SID"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    auth_token = forms.CharField(
        max_length=100,
        required=False,
        label=_("Auth Token"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    from_number = forms.CharField(
        max_length=20,
        required=False,
        label=_("Göndərən Nömrə"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    # AWS SNS-specific fields
    aws_access_key_id = forms.CharField(
        max_length=100,
        required=False,
        label=_("AWS Access Key ID"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    aws_secret_access_key = forms.CharField(
        max_length=100,
        required=False,
        label=_("AWS Secret Access Key"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    aws_region = forms.CharField(
        max_length=50,
        required=False,
        label=_("AWS Region"),
        initial="us-east-1",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    # Clickatell-specific fields
    clickatell_api_key = forms.CharField(
        max_length=100,
        required=False,
        label=_("API Açarı"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    # Custom provider fields
    custom_url = forms.URLField(
        required=False,
        label=_("Fərdi URL"),
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )
    custom_token = forms.CharField(
        max_length=100,
        required=False,
        label=_("Fərdi Token"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        provider = cleaned_data.get('provider')
        
        # Validate required fields based on provider
        if provider == 'twilio':
            account_sid = cleaned_data.get('account_sid')
            auth_token = cleaned_data.get('auth_token')
            from_number = cleaned_data.get('from_number')
            
            if not all([account_sid, auth_token, from_number]):
                raise forms.ValidationError(
                    _("Twilio təchizatçısı üçün bütün sahələr tələb olunur.")
                )
        
        elif provider == 'aws_sns':
            aws_access_key_id = cleaned_data.get('aws_access_key_id')
            aws_secret_access_key = cleaned_data.get('aws_secret_access_key')
            
            if not all([aws_access_key_id, aws_secret_access_key]):
                raise forms.ValidationError(
                    _("AWS SNS təchizatçısı üçün giriş məlumatları tələb olunur.")
                )
        
        elif provider == 'clickatell':
            api_key = cleaned_data.get('clickatell_api_key')
            
            if not api_key:
                raise forms.ValidationError(
                    _("Clickatell təchizatçısı üçün API açarı tələb olunur.")
                )
        
        elif provider == 'custom':
            custom_url = cleaned_data.get('custom_url')
            
            if not custom_url:
                raise forms.ValidationError(
                    _("Fərdi təchizatçı üçün URL tələb olunur.")
                )
        
        return cleaned_data


class NotificationTemplateForm(forms.Form):
    """
    Form for notification template configuration.
    """
    TRIGGER_CHOICES = [
        ('campaign_start', _('Qiymətləndirmə Kampaniyası Başlayır')),
        ('campaign_end', _('Qiymətləndirmə Kampaniyası Bitir')),
        ('evaluation_assigned', _('Qiymətləndirmə Tapşırılır')),
        ('evaluation_completed', _('Qiymətləndirmə Tamamlanır')),
        ('report_ready', _('Hesabat Hazırdır')),
        ('deadline_reminder', _('Bitmə Vaxtına Xatırlatma')),
        ('new_training', _('Yeni Təlim Təyin Edilir')),
        ('training_complete', _('Təlim Tamamlanır')),
        ('salary_change', _('Maaş Dəyişikliyi')),
        ('performance_result', _('Performans Nəticələri')),
        ('system_maintenance', _('Sistem Texniki Xidmət')),
        ('password_change', _('Şifrə Dəyişikliyi')),
        ('account_lock', _('Hesab Bloklanır')),
        ('security_alert', _('Təhlükəsizlik Xəbərdarlığı')),
        ('general_announcement', _('Ümumi Elan')),
    ]
    
    METHODS = [
        ('email', _('E-poçt')),
        ('sms', _('SMS')),
        ('push', _('Push Bildirişi')),
        ('in_app', _('Tətbiqdaxili')),
    ]
    
    name = forms.CharField(
        max_length=100,
        label=_("Şablon Adı"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    trigger = forms.ChoiceField(
        choices=TRIGGER_CHOICES,
        label=_("Tətik"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    subject = forms.CharField(
        max_length=200,
        label=_("Mövzu"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email_content = forms.CharField(
        label=_("E-poçt Məzmunu"),
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    
    sms_content = forms.CharField(
        max_length=160,
        label=_("SMS Məzmunu"),
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    
    push_content = forms.CharField(
        max_length=200,
        label=_("Push Məzmunu"),
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    
    inapp_content = forms.CharField(
        label=_("Tətbiqdaxili Məzmun"),
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    
    methods = forms.MultipleChoiceField(
        choices=METHODS,
        label=_("Bildiriş Metodları"),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    is_active = forms.BooleanField(
        label=_("Aktivdir"),
        required=False,
        initial=True
    )
