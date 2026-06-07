from pathlib import Path

root = Path('site')
files = list(root.glob('*.html'))
if not files:
    raise SystemExit('No site HTML files found')

old_is_logged_in = "function isLoggedIn() {\n      return localStorage.getItem(sessionKey) === 'true';\n    }"
new_is_logged_in = "function isLoggedIn() {\n      if (localStorage.getItem(sessionKey) === 'true') return true;\n      const params = new URLSearchParams(location.search);\n      return params.get('loggedIn') === 'true';\n    }"

old_get_saved_user = "function getSavedUser() {\n      return localStorage.getItem(userKey) || 'Student';\n    }"
new_get_saved_user = "function getSavedUser() {\n      const stored = localStorage.getItem(userKey);\n      if (stored) return stored;\n      const params = new URLSearchParams(location.search);\n      return params.get('user') || 'Student';\n    }"

old_set_session = "function setSession(user) {\n      localStorage.setItem(sessionKey, 'true');\n      localStorage.setItem(userKey, user);\n    }"
new_set_session = "function setSession(user) {\n      localStorage.setItem(sessionKey, 'true');\n      localStorage.setItem(userKey, user);\n      const params = new URLSearchParams();\n      params.set('loggedIn', 'true');\n      params.set('user', user);\n      history.replaceState(null, '', location.pathname + '?' + params.toString());\n    }"

old_attach_nav = "function attachNavHandlers() {\n      document.querySelectorAll('.nav-list li').forEach((item) => {\n        item.style.cursor = 'pointer';\n        item.addEventListener('click', () => updateSection(item.textContent.trim()));\n      });\n    }"
new_attach_nav = "function attachNavHandlers() {\n      document.querySelectorAll('.nav-list li a').forEach((link) => {\n        const base = link.getAttribute('href').split('?')[0];\n        if (isLoggedIn()) {\n          const params = new URLSearchParams();\n          params.set('loggedIn', 'true');\n          params.set('user', state.userName);\n          link.setAttribute('href', `${base}?${params.toString()}`);\n        } else {\n          link.setAttribute('href', base);\n        }\n      });\n      document.querySelectorAll('.nav-list li').forEach((item) => {\n        item.style.cursor = 'pointer';\n        item.addEventListener('click', () => updateSection(item.textContent.trim()));\n      });\n    }"

for path in files:
    text = path.read_text(encoding='utf-8')
    updated = text
    updated = updated.replace(old_is_logged_in, new_is_logged_in)
    updated = updated.replace(old_get_saved_user, new_get_saved_user)
    updated = updated.replace(old_set_session, new_set_session)
    updated = updated.replace(old_attach_nav, new_attach_nav)
    if updated != text:
        path.write_text(updated, encoding='utf-8')
        print(f'patched {path.name}')
    else:
        print(f'skip {path.name}')
