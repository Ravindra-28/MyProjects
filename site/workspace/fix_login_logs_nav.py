from pathlib import Path

root = Path('site')

# Update root pages to include folder-based login link
for page in root.glob('*.html'):
    text = page.read_text(encoding='utf-8')
    if 'href="login/"' not in text:
        if 'href="logs/"' in text:
            text = text.replace('        <li><a href="logs/">Logs</a></li>', '        <li><a href="login/">Login</a></li>\n        <li><a href="logs/">Logs</a></li>')
            page.write_text(text, encoding='utf-8')
            print(f'added login nav to {page.name}')
        else:
            print(f'skipped {page.name} no logs link')
    else:
        print(f'already has login nav {page.name}')

# Update moved page navs
login_page = root / 'login' / 'index.html'
logs_page = root / 'logs' / 'index.html'
for page, login_href in [(login_page, '../login/'), (logs_page, '../login/')]:
    text = page.read_text(encoding='utf-8')
    if 'href="../login/"' not in text:
        if 'href="../logs/"' in text:
            active = ' class="active"' if page.name == 'index.html' and page.parent.name == 'login' else ''
            login_line = f'        <li{active}><a href="../login/">Login</a></li>\n'
            text = text.replace('        <li><a href="../logs/">Logs</a></li>', login_line + '        <li><a href="../logs/">Logs</a></li>')
            page.write_text(text, encoding='utf-8')
            print(f'added folder login nav to {page}')
        else:
            print(f'skipped {page} no logs link')
    else:
        print(f'already has login nav {page}')
