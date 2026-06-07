from pathlib import Path

root = Path('site')
files = list(root.glob('*.html'))
if not files:
    raise SystemExit('No site HTML files found')

old_show_logged_in = "function showLoggedInUI() {\n      state.userName = getSavedUser();\n      document.getElementById('greetingName').textContent = state.userName;\n      document.getElementById('loginPage').style.display = 'none';\n      document.getElementById('dashboard').style.display = 'grid';\n      updateUI();\n    }"
new_show_logged_in = "function showLoggedInUI() {\n      state.userName = getSavedUser();\n      document.getElementById('greetingName').textContent = state.userName;\n      document.getElementById('loginPage').style.display = 'none';\n      document.getElementById('dashboard').style.display = 'grid';\n      updateUI();\n      updateNavLinks();\n    }"

old_attach_nav = "function attachNavHandlers() {\n      document.querySelectorAll('.nav-list li a').forEach((link) => {\n        const base = link.getAttribute('href').split('?')[0];\n        if (isLoggedIn()) {\n          const params = new URLSearchParams();\n          params.set('loggedIn', 'true');\n          params.set('user', state.userName);\n          link.setAttribute('href', `${base}?${params.toString()}`);\n        } else {\n          link.setAttribute('href', base);\n        }\n      });\n      document.querySelectorAll('.nav-list li').forEach((item) => {\n        item.style.cursor = 'pointer';\n        item.addEventListener('click', () => updateSection(item.textContent.trim()));\n      });\n    }"
new_attach_nav = "function updateNavLinks() {\n      document.querySelectorAll('.nav-list li a').forEach((link) => {\n        const base = link.getAttribute('href').split('?')[0];\n        if (isLoggedIn()) {\n          const params = new URLSearchParams();\n          params.set('loggedIn', 'true');\n          params.set('user', state.userName);\n          link.setAttribute('href', `${base}?${params.toString()}`);\n        } else {\n          link.setAttribute('href', base);\n        }\n      });\n    }\n\n    function attachNavHandlers() {\n      updateNavLinks();\n      document.querySelectorAll('.nav-list li').forEach((item) => {\n        item.style.cursor = 'pointer';\n        item.addEventListener('click', () => updateSection(item.textContent.trim()));\n      });\n    }"

for path in files:
    text = path.read_text(encoding='utf-8')
    updated = text.replace(old_show_logged_in, new_show_logged_in).replace(old_attach_nav, new_attach_nav)
    if updated != text:
        path.write_text(updated, encoding='utf-8')
        print(f'patched {path.name}')
    else:
        print(f'skip {path.name}')
