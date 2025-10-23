from pathlib import Path
missing = [
    ('apps/audit/template_views.py', '403.html'),
    ('apps/audit/views.py', 'audit/log_search.html'),
    ('apps/competencies/template_views.py', '403.html'),
    ('apps/dashboard/views.py', 'dashboard/ai_management.html'),
    ('apps/evaluations/template_views.py', 'evaluations/results.html'),
    ('apps/notifications/template_views.py', 'notifications/notification_detail.html'),
    ('apps/notifications/views.py', 'notifications/bulk_send.html'),
    ('apps/notifications/views.py', 'notifications/delivery_logs.html'),
    ('apps/notifications/views.py', 'notifications/statistics.html'),
    ('apps/notifications/views.py', 'notifications/template_preview.html'),
    ('apps/reports/admin.py', 'admin/reports/users_report.html'),
    ('apps/reports/template_views.py', 'reports/comparison_report.html'),
    ('apps/reports/template_views.py', 'reports/comparison_select.html'),
    ('apps/sentiment_analysis/views.py', 'sentiment_analysis/dashboard.html'),
    ('apps/sentiment_analysis/views.py', 'sentiment_analysis/feedback_detail.html'),
    ('apps/training/template_views.py', '403.html'),
]
base = Path('C:/lahiyeler/q360/q360_project')
for rel, tmpl in missing:
    path = base / rel
    text = path.read_text(encoding='utf-8', errors='ignore').splitlines()
    line_no = next((idx for idx, line in enumerate(text, 1) if tmpl in line), None)
    print(f"{rel}:{line_no}")
