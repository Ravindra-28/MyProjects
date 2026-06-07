from pathlib import Path
import shutil

root = Path('site')

folders = {
    'login.html': root / 'login' / 'index.html',
    'logs.html': root / 'logs' / 'index.html',
}

for src_name, dest_path in folders.items():
    src = root / src_name
    dest_dir = dest_path.parent
    dest_dir.mkdir(parents=True, exist_ok=True)
    if src.exists():
        shutil.move(str(src), str(dest_path))
        print(f'moved {src_name} -> {dest_path}')
    else:
        print(f'source missing {src_name}')

# update all root-level html pages
for page in root.glob('*.html'):
    text = page.read_text(encoding='utf-8')
    updated = text.replace('href="logs.html"', 'href="logs/"')
    updated = updated.replace('href="login.html"', 'href="login/"')
    if updated != text:
        page.write_text(updated, encoding='utf-8')
        print(f'updated links in {page.name}')

# update moved pages paths
moved_pages = [dest_path for dest_path in folders.values() if dest_path.exists()]
for page in moved_pages:
    text = page.read_text(encoding='utf-8')
    # relative paths from folder to root
    text = text.replace('href="styles.css"', 'href="../styles.css"')
    for link in ['dashboard.html', 'students.html', 'attendance.html', 'exams.html', 'fees.html', 'library.html', 'placement.html', 'support.html']:
        text = text.replace(f'href="{link}"', f'href="../{link}"')
    text = text.replace('href="logs.html"', 'href="../logs/"')
    text = text.replace('href="login.html"', 'href="../login/"')
    page.write_text(text, encoding='utf-8')
    print(f'updated moved page {page}')

# fix possible nav item active class on logs page
logs_index = root / 'logs' / 'index.html'
if logs_index.exists():
    text = logs_index.read_text(encoding='utf-8')
    text = text.replace('<li class="active"><a href="logs.html">Logs</a></li>', '<li class="active"><a href="../logs/">Logs</a></li>')
    logs_index.write_text(text, encoding='utf-8')

print('done')
