import os
import sys
import django

# Setup Django
sys.path.insert(0, 'q360_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Test fitness_programs template loading
try:
    from django.template.loader import get_template
    template = get_template('wellness/fitness_programs.html')
    print("✅ wellness/fitness_programs.html template yükləndi və compile olundu")
except Exception as e:
    print(f"❌ Template load error: {e}")
    import traceback
    traceback.print_exc()
