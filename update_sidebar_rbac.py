"""
Script to add RBAC permissions to sidebar.html
Automatically wraps menu sections with permission checks
"""
import re

# Read the sidebar file
with open(r'C:\lahiyeler\q360\q360_project\templates\base\sidebar.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add load tag at the top (after existing loads)
if '{% load sidebar_filters %}' not in content:
    content = content.replace(
        '{% load navigation_filters %}',
        '{% load navigation_filters %}\n{% load sidebar_filters %}'
    )

# Define sections and their permission keys
sections = [
    # (section_title, permission_key, start_pattern, end_pattern)
    ('Panel və Analitika', 'dashboard', 'Panel və Analitika', None),
    ('Qiymətləndirmə və Rəylər', 'evaluations', 'Qiymətləndirmə və Rəylər', None),
    ('Kompetensiya və Təlim', 'competencies', 'Kompetensiya və Təlim', None),
    ('İnkişaf və Strategiya', 'development', 'İnkişaf və Strategiya', None),
    ('HR İdarəetməsi', 'hr_management', 'HR İdarəetməsi', None),
    ('Sağlamlıq və Wellness', 'wellness', 'Sağlamlıq və Wellness', None),
    ('İşçi Mənsubiyyəti', 'engagement', 'İşçi Mənsubiyyəti', None),
    ('Bildirişlər və Ünsiyyət', 'notifications', 'Bildirişlər və Ünsiyyət', None),
]

# Function to wrap a section with RBAC check
def wrap_section(content, title, permission_key):
    # Find the section div that contains the title
    pattern = rf'(<div class="space-y-1" x-data="{{[^}}]*}}">[\s\S]*?<span>{{%\s*trans\s*["\']' + re.escape(title) + r'["\']'

    matches = list(re.finditer(pattern, content))

    if not matches:
        print(f"Warning: Could not find section '{title}'")
        return content

    for match in matches:
        start_pos = match.start()

        # Find the closing </div> for this section
        # Count opening and closing divs to find the matching one
        section_start = content[start_pos:]
        div_count = 0
        pos = 0
        found_end = False

        for i, char in enumerate(section_start):
            if section_start[i:i+4] == '<div':
                div_count += 1
            elif section_start[i:i+6] == '</div>':
                div_count -= 1
                if div_count == 0:
                    end_pos = start_pos + i + 6
                    found_end = True
                    break

        if not found_end:
            print(f"Warning: Could not find closing div for section '{title}'")
            continue

        # Extract the section
        section = content[start_pos:end_pos]

        # Check if already wrapped
        if f"can_view_menu '{permission_key}'" in section:
            print(f"Section '{title}' already has RBAC check")
            continue

        # Wrap the section
        wrapped = f"""{{% can_view_menu '{permission_key}' as can_view_{permission_key} %}}
            {{% if can_view_{permission_key} %}}
            {section}
            {{% endif %}}"""

        # Replace in content
        content = content[:start_pos] + wrapped + content[end_pos:]
        print(f"Wrapped section '{title}' with permission check '{permission_key}'")

        # Only wrap the first match
        break

    return content

# Wrap each section
for title, permission_key, start_pattern, _ in sections:
    content = wrap_section(content, title, permission_key)

# Write back to file
with open(r'C:\lahiyeler\q360\q360_project\templates\base\sidebar.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nSidebar RBAC update complete!")
print("Added permission checks for all major menu sections.")
