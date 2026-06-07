from pathlib import Path
import re

root = Path('site')
files = list(root.glob('*.html'))
if not files:
    raise SystemExit('No site HTML files found')

insert_session = '''    const sessionKey = 'campussync_logged_in';
    const userKey = 'campussync_user';

    function setSession(user) {
      localStorage.setItem(sessionKey, 'true');
      localStorage.setItem(userKey, user);
    }

    function clearSession() {
      localStorage.removeItem(sessionKey);
      localStorage.removeItem(userKey);
    }

    function isLoggedIn() {
      return localStorage.getItem(sessionKey) === 'true';
    }

    function getSavedUser() {
      return localStorage.getItem(userKey) || 'Student';
    }

    function showLoggedInUI() {
      state.userName = getSavedUser();
      document.getElementById('greetingName').textContent = state.userName;
      document.getElementById('loginPage').style.display = 'none';
      document.getElementById('dashboard').style.display = 'grid';
      updateUI();
    }

    function showLoginUI() {
      document.getElementById('loginPage').style.display = 'block';
      document.getElementById('dashboard').style.display = 'none';
      const alertBox = document.getElementById('loginAlert');
      if (alertBox) alertBox.textContent = '';
    }
'''

login_replacement = '''    function login() {
      const userInput = document.getElementById('loginUser').value.trim();
      const passInput = document.getElementById('loginPass').value.trim();
      const robotChecked = document.getElementById('robotCheck').checked;
      const alertBox = document.getElementById('loginAlert');

      if (!userInput) {
        alertBox.textContent = 'Please enter your name to continue.';
        return;
      }
      if (!passInput) {
        alertBox.textContent = 'Please enter your password.';
        return;
      }
      if (!robotChecked) {
        alertBox.textContent = 'Please confirm you are not a robot.';
        return;
      }
      if (userInput !== state.credentials.username || passInput !== state.credentials.password) {
        alertBox.textContent = 'Invalid credentials. Use Ravindra19 / 12345678.';
        return;
      }
      alertBox.textContent = '';
      state.userName = userInput;
      setSession(state.userName);
      showLoggedInUI();
    }
'''

for path in files:
    text = path.read_text(encoding='utf-8')
    updated = text

    # insert session helpers after state object
    updated, count_state = re.subn(
        r"(const state = \{[\s\S]*?\};\s*\n\n)    function setRole",
        lambda m: m.group(1) + insert_session + '    function setRole',
        updated,
        count=1
    )

    # replace login function content
    updated, count_login = re.subn(
        r"function login\(\) \{[\s\S]*?\n    function formatTimer\(",
        lambda m: login_replacement + '\n    function formatTimer(',
        updated,
        count=1
    )

    # update DOMContentLoaded session check
    updated, count_dom = re.subn(
        r"window\.addEventListener\('DOMContentLoaded', \(\) => \{\n      setRole\('Student'\);\n      updateUI\(\);\n      attachNavHandlers\(\);\n      setInterval\(tickTimer, 1000\);\n    \}\);",
        "window.addEventListener('DOMContentLoaded', () => {\n      setRole('Student');\n      attachNavHandlers();\n      if (isLoggedIn()) {\n        showLoggedInUI();\n      } else {\n        showLoginUI();\n      }\n      setInterval(tickTimer, 1000);\n    });",
        updated,
        count=1
    )

    if count_state == 0 or count_login == 0 or count_dom == 0:
        print(f'SKIP {path.name}: state_insert={count_state}, login_replace={count_login}, dom_replace={count_dom}')
    else:
        path.write_text(updated, encoding='utf-8')
        print(f'patched {path.name}')
