from pathlib import Path
import re

root = Path('site')
for path in root.glob('*.html'):
    text = path.read_text(encoding='utf-8')
    if 'credentials:' in text:
        continue
    new_text, count = re.subn(r"(role:\s*'Student',\s*\n)(\s*announcements:\s*\[)",
                             r"\1      credentials: { username: 'Ravindra19', password: '12345678' },\n\2",
                             text)
    if count == 1:
        path.write_text(new_text, encoding='utf-8')
        print('patched', path.name)
    else:
        if 'role:' in text:
            print('skip', path.name, 'count', count)
