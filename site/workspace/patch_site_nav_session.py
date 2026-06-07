from pathlib import Path
import re

root = Path('site')
files = list(root.glob('*.html'))
if not files:
    raise SystemExit('No site HTML files found')

for path in files:
    text = path.read_text(encoding='utf-8')
    updated = text

    # Extend login/session helpers to accept URL params fallback.
    updated, c1 = re.subn(
        r"function isLoggedIn\(\) \{\n      return localStorage\.getItem\(sessionKey\) === 'true';\n    \}",
        "function isLoggedIn() {\n      if (localStorage.getItem(sessionKey) === 'true') return true;\n      const params = new URLSearchParams(location.search);\n      return params.get('loggedIn') === 'true';\n    }",
        updated,
        count=1
    )

    updated, c2 = re.subn(
        r"function getSavedUser\(\) \{\n      return localStorage\.getItem\(userKey\) \|\| 'Student';\n    \}",
        "function getSavedUser() {\n      const stored = localStorage.getItem(userKey);\n      if (stored) return stored;\n      const params = new URLSearchParams(location.search);\n      return params.get('user') || 'Student';\n    }",
        updated,
        count=1
    )

    updated, c3 = re.subn(
        r"function setSession\(user\) \{\n      localStorage\.setItem\(sessionKey, 'true'\);\n      localStorage\.setItem\(userKey, user\);\n    \}",
        "function setSession(user) {\n      localStorage.setItem(sessionKey, 'true');\n      localStorage.setItem(userKey, user);\n      const params = new URLSearchParams();\n      params.set('loggedIn', 'true');\n      params.set('user', user);\n      history.replaceState(null, '', location.pathname + '?' + params.toString());\n    }",
        updated,
        count=1
    )

    updated, c4 = re.subn(
        r"function attachNavHandlers\(\) \{\n      document\.querySelectorAll\('\.nav-list li'\)\.forEach\(\(item\) => \{\n        item\.style\.cursor = 'pointer';\n        item\.addEventListener\('click', \(\) => updateSection\(item\.textContent\.trim\(\)\)\);\n      \});\n    \}",
        "function attachNavHandlers() {\n      document.querySelectorAll('.nav-list li a').forEach((link) => {\n        const base = link.getAttribute('href').split('?')[0];\n        if (isLoggedIn()) {\n          const params = new URLSearchParams();\n          params.set('loggedIn', 'true');\n          params.set('user', state.userName);\n          link.setAttribute('href', `${base}?${params.toString()}`);\n        } else {\n          link.setAttribute('href', base);\n        }\n      });\n      document.querySelectorAll('.nav-list li').forEach((item) => {\n        item.style.cursor = 'pointer';\n        item.addEventListener('click', () => updateSection(item.textContent.trim()));\n      });\n    }",
        updated,
        count=1
    )

    if c1 + c2 + c3 + c4 != 4:
        print(f'SKIP {path.name}: counts={c1},{c2},{c3},{c4}')
    else:
        path.write_text(updated, encoding='utf-8')
        print(f'patched {path.name}')
