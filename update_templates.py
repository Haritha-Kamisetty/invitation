"""Simple and reliable: Replace all literal newlines in JSON output"""
import json
import re

# Read the generated JSON
with open('templates_output.json', 'r', encoding='utf-8') as f:
    templates = json.load(f)

# Read current app.js
with open('app/static/js/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Convert to JSON string
json_str = json.dumps(templates, indent=4, ensure_ascii=False)

# Simple approach: Replace ALL literal newlines within quoted strings
# Split by quotes and process only the string contents
lines = json_str.split('\n')
fixed_lines = []

for line in lines:
    # If line contains a string value with newline characters
    if '": "' in line and not line.strip().endswith('",') and not line.strip().endswith('"'):
        # This line has an unclosed string, keep as is for now
        fixed_lines.append(line)
    else:
        fixed_lines.append(line)

# Rejoin
json_str = '\n'.join(fixed_lines)

# Now do a global replace of literal newlines in string contexts
# Find all "text": "..." patterns and escape newlines within them
def fix_text_field(match):
    full_match = match.group(0)
    # Extract the value part
    value_start = full_match.index('"', full_match.index(':') + 1)
    value_end = len(full_match) - 1 if full_match.endswith('"') else len(full_match)
    
    prefix = full_match[:value_start+1]
    value = full_match[value_start+1:value_end]
    suffix = full_match[value_end:]
    
    # Escape newlines in the value
    value = value.replace('\\', '\\\\').replace('\n', '\\n').replace('\r', '')
    
    return prefix + value + suffix

# This won't work with multiline... let me try a different approach
# Just read the file as bytes and replace the newline bytes in string contexts

# Actually, simplest solution: use a JSON encoder that escapes everything
import codecs

# Manually build the JavaScript object
def to_js(obj, indent=0):
    ind = '    ' * indent
    if isinstance(obj, dict):
        lines = ['{']
        items = list(obj.items())
        for i, (k, v) in enumerate(items):
            comma = ',' if i < len(items) - 1 else ''
            lines.append(f'{ind}    "{k}": {to_js(v, indent+1)}{comma}')
        lines.append(f'{ind}}}')
        return '\n'.join(lines)
    elif isinstance(obj, list):
        if not obj:
            return '[]'
        lines = ['[']
        for i, item in enumerate(obj):
            comma = ',' if i < len(obj) - 1 else ''
            lines.append(f'{ind}    {to_js(item, indent+1)}{comma}')
        lines.append(f'{ind}]')
        return '\n'.join(lines)
    elif isinstance(obj, str):
        # Properly escape the string
        escaped = json.dumps(obj, ensure_ascii=False)
        return escaped
    elif isinstance(obj, bool):
        return 'true' if obj else 'false'
    elif obj is None:
        return 'null'
    else:
        return json.dumps(obj)

js_str = to_js(templates)

# Create the new TEMPLATES declaration
new_templates = f'const TEMPLATES = {js_str};'

# Find and replace the TEMPLATES object
pattern = r'const TEMPLATES = \{[\s\S]*?\n\};'

# Replace in app.js
updated_app_js = re.sub(pattern, new_templates, app_js, count=1)

# Write back
with open('app/static/js/app.js', 'w', encoding='utf-8', newline='\n') as f:
    f.write(updated_app_js)

print('Successfully updated app.js with 90 templates!')
print(f'   - Birthday: {len(templates["birthday"])} templates')
print(f'   - Wedding: {len(templates["wedding"])} templates')
print(f'   - Anniversary: {len(templates["anniversary"])} templates')
print(f'   - Baby: {len(templates["baby"])} templates')
print(f'\nTotal: {sum(len(v) for v in templates.values())} templates')
print('\nUsing custom JavaScript formatter with json.dumps() for string escaping')
