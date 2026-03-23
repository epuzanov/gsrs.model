import re
from pathlib import Path

def fix_element_property(file_path):
    content = file_path.read_text(encoding='utf-8')
    original = content
    
    # Pattern 1: Remove json_schema_extra line when it's in the middle
    # description='...'\n        json_schema_extra={'element_property': True},\n    )
    # -> description='...',\n    )
    content = re.sub(
        r"(description='[^']*')\n        json_schema_extra=\{'element_property': True\},",
        r"\1,",
        content
    )
    
    # Pattern 2: Also handle title/description without trailing newline
    content = re.sub(
        r"(description='[^']*'),\s*json_schema_extra=\{'element_property': True\},",
        r"\1,",
        content
    )
    
    if content != original:
        file_path.write_text(content, encoding='utf-8')
        return True
    return False

model_dir = Path('gsrs/model')
fixed_files = []
for py_file in model_dir.glob('*.py'):
    if fix_element_property(py_file):
        fixed_files.append(py_file.name)

print(f'Fixed {len(fixed_files)} files:')
for f in fixed_files:
    print(f'  - {f}')
