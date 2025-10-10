"""
Test all Q360 pages for errors.
"""
import requests
from urllib.parse import urljoin

BASE_URL = "http://127.0.0.1:8000"

# Pages to test (URL, Expected Status, Requires Auth)
PAGES = [
    # Public pages
    ('/', 200, False),
    ('/accounts/login/', 200, False),
    ('/accounts/register/', 302, False),  # Disabled, redirects to login

    # Auth required pages (will redirect to login if not authenticated)
    ('/dashboard/', [200, 302], True),
    ('/accounts/profile/', [200, 302], True),
    ('/accounts/logout/', [200, 302], True),

    # Evaluations
    ('/evaluations/campaigns/', [200, 302], True),
    ('/evaluations/my-assignments/', [200, 302], True),
    ('/evaluations/questions/', [200, 302], True),
    ('/evaluations/categories/', [200, 302], True),

    # Reports
    ('/reports/my-reports/', [200, 302], True),
    ('/reports/team-reports/', [200, 302], True),

    # Notifications
    ('/notifications/inbox/', [200, 302], True),

    # Development Plans
    ('/development-plans/my-goals/', [200, 302], True),

    # Departments
    ('/departments/', [200, 302], True),
    ('/departments/structure/', [200, 302], True),

    # Admin
    ('/admin/', [200, 302], True),
    ('/admin/login/', 200, False),
]

def test_pages():
    """Test all pages."""
    print("="*70)
    print("Q360 SƏHIFƏLƏR TESTİ".center(70))
    print("="*70)
    print()

    results = {
        'success': [],
        'failed': [],
        'total': 0
    }

    session = requests.Session()

    for url, expected_status, requires_auth in PAGES:
        results['total'] += 1
        full_url = urljoin(BASE_URL, url)

        try:
            response = session.get(full_url, allow_redirects=False, timeout=5)
            status = response.status_code

            # Check if status matches expected
            if isinstance(expected_status, list):
                success = status in expected_status
            else:
                success = status == expected_status

            if success:
                results['success'].append((url, status))
                icon = "✅"
                status_text = f"{status}"
            else:
                results['failed'].append((url, status, expected_status))
                icon = "❌"
                status_text = f"{status} (gözlənilən: {expected_status})"

            print(f"{icon} {url:50} {status_text}")

        except requests.exceptions.RequestException as e:
            results['failed'].append((url, 'ERROR', str(e)))
            print(f"❌ {url:50} ERROR: {str(e)[:30]}")

    # Print summary
    print()
    print("="*70)
    print("NƏTICƏ".center(70))
    print("="*70)
    print(f"Ümumi: {results['total']}")
    print(f"✅ Uğurlu: {len(results['success'])}")
    print(f"❌ Uğursuz: {len(results['failed'])}")
    print()

    if results['failed']:
        print("UĞURSUZ SƏHİFƏLƏR:")
        for item in results['failed']:
            if len(item) == 3:
                url, status, expected = item
                print(f"  • {url}: {status} (gözlənilən: {expected})")
            else:
                url, status, error = item
                print(f"  • {url}: {status} - {error}")

    return len(results['failed']) == 0

if __name__ == '__main__':
    success = test_pages()
    exit(0 if success else 1)
