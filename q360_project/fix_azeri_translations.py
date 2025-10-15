#!/usr/bin/env python3
"""
Script to fix the django.po file by putting Azerbaijani text from msgid 
into empty msgstr entries (instead of English translations).
"""

import re


def process_po_file(file_path):
    """Process the .po file to fill empty msgstr entries with Azerbaijani text from msgid."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # First, handle all single-line msgid/msgstr pairs with empty msgstr
    # Pattern matches: msgid "text" followed by empty msgstr ""
    single_pattern = r'(msgid\s+"([^"]+)"\s*\nmsgstr\s+"")'
    
    def replace_empty_msgstr_with_azeri(match):
        full_match = match.group(1)
        msgid_text = match.group(2)
        
        # Replace empty msgstr with the same Azerbaijani text from msgid
        return f'msgid "{msgid_text}"\nmsgstr "{msgid_text}"'
        
        return full_match
    
    updated_content = re.sub(single_pattern, replace_empty_msgstr_with_azeri, content)
    
    # Now handle multiline msgid entries that have empty msgstr
    # These have the pattern: msgid "" followed by continuation lines, then empty msgstr ""
    multiline_pattern = r'(msgid\s+""\s*\n(?:^\s*"[^"]*"\s*\n)+msgstr\s+"")'
    
    def replace_empty_multiline_msgstr_with_azeri(match):
        full_match = match.group(1)
        
        # Extract the original Azerbaijani text content from the msgid
        lines = full_match.split('\n')
        original_text = ""
        
        # Process the lines to reconstruct the original text
        for line in lines:
            line = line.strip()
            if line.startswith('"') and line.endswith('"') and line != '""' and not line.startswith('msgstr'):
                # Remove the quotes and add to original_text
                actual_content = line[1:-1]  # Remove first and last quote
                if original_text:
                    original_text += actual_content  # For multiline, just concatenate
                else:
                    original_text = actual_content
    
        # Replace empty msgstr with the reconstructed Azerbaijani text
        result = 'msgid ""\n'
        # Add back the original msgid content lines
        for line in lines[1:-1]:  # Skip first line (msgid "") and last line (msgstr "")
            line = line.strip()
            if line.startswith('"') and line.endswith('"') and line != '""' and not line.startswith('msgstr'):
                result += f'{line}\n'
        result += f'msgstr "{original_text}"'
        return result
    
    # Apply the multiline pattern replacement
    updated_content = re.sub(multiline_pattern, replace_empty_multiline_msgstr_with_azeri, updated_content, flags=re.MULTILINE)
    
    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Updated {file_path} with Azerbaijani text for empty msgstr entries.")
    
    # Count remaining empty msgstr entries (excluding header at line 6 which should be empty)
    remaining_empty = len(re.findall(r'\nmsgid\s+"[^"]+"\s*\nmsgstr\s+""', updated_content))
    print(f"Remaining single-line empty msgstr entries: {remaining_empty}")
    
    # Check for multiline entries
    multiline_empty = len(re.findall(r'\nmsgid\s+""\s*\n(?:^\s*"[^"]*"\s*\n)+msgstr\s+""', updated_content, re.MULTILINE))
    print(f"Remaining multiline empty msgstr entries: {multiline_empty}")


if __name__ == "__main__":
    po_file_path = "C:/lahiyeler/q360/q360_project/locale/az/LC_MESSAGES/django.po"
    process_po_file(po_file_path)