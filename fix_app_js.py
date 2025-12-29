"""Direct fix: Read app.js and escape literal newlines in TEMPLATES section"""
import re

# Read app.js
with open('app/static/js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the TEMPLATES section
start_marker = 'const TEMPLATES = {'
end_marker = '\n};'

start_idx = content.find(start_marker)
if start_idx == -1:
    print("ERROR: Could not find TEMPLATES")
    exit(1)

end_idx = content.find(end_marker, start_idx)
if end_idx == -1:
    print("ERROR: Could not find end of TEMPLATES")
    exit(1)

# Extract the TEMPLATES section
before = content[:start_idx]
templates_section = content[start_idx:end_idx + len(end_marker)]
after = content[end_idx + len(end_marker):]

# Fix the templates section by escaping literal newlines in string values
# Strategy: Find all "text": "..." patterns and escape newlines
fixed_section = templates_section

# Replace literal newlines and carriage returns in the entire TEMPLATES section
# But only within string values (between quotes)
in_string = False
result = []
i = 0
while i < len(fixed_section):
    char = fixed_section[i]
    
    if char == '"' and (i == 0 or fixed_section[i-1] != '\\'):
        # Toggle string state
        in_string = not in_string
        result.append(char)
    elif in_string and char == '\n':
        # Replace literal newline with escaped version
        result.append('\\n')
    elif in_string and char == '\r':
        # Skip carriage returns
        pass
    else:
        result.append(char)
    
    i += 1

fixed_section = ''.join(result)

# Reconstruct the file
new_content = before + fixed_section + after

# Write back
with open('app/static/js/app.js', 'w', encoding='utf-8', newline='\n') as f:
    f.write(new_content)

print('Successfully fixed app.js!')
print('Literal newlines in strings have been escaped as \\\\n')
print(f'File size: {len(new_content)} bytes')
