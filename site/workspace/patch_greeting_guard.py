from pathlib import Path

root = Path('..') / 'site'
files = list(root.glob('*.html'))
files += list((root / 'login').glob('*.html'))
files += list((root / 'logs').glob('*.html'))
pattern = "document.getElementById('greetingName').textContent = state.userName;"
replacement = "const greetingEl = document.getElementById('greetingName');\n      if (greetingEl) greetingEl.textContent = state.userName;"
for path in files:
    text = path.read_text(encoding='utf-8')
    if pattern in text:
        text = text.replace(pattern, replacement)
        path.write_text(text, encoding='utf-8')
        print(f'patched {path}')
