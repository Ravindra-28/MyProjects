from pathlib import Path
from shutil import copyfile

root = Path('site')
files = [p for p in root.glob('*.html') if p.name not in ('index.html', 'login.html', 'logs.html')]

for path in files:
    text = path.read_text(encoding='utf-8')
    if 'Logs</a>' in text:
        continue
    nav_start = text.find('<ul class="nav-list">')
    if nav_start == -1:
        print('skip no nav', path.name)
        continue
    insert_pos = text.find('</ul>', nav_start)
    if insert_pos == -1:
        print('skip no end nav', path.name)
        continue
    new_nav_item = '        <li><a href="logs.html">Logs</a></li>\n'
    updated = text[:insert_pos] + new_nav_item + text[insert_pos:]
    path.write_text(updated, encoding='utf-8')
    print('updated nav', path.name)

# Create login page alias if it doesn't exist
login_src = root / 'campussync-erp.html'
login_dst = root / 'login.html'
if not login_dst.exists():
    copyfile(login_src, login_dst)
    txt = login_dst.read_text(encoding='utf-8')
    txt = txt.replace('<title>CampusSync AI | College ERP</title>', '<title>CampusSync AI | Login</title>')
    txt = txt.replace('<strong>Login</strong>', '<strong>Login</strong>')
    login_dst.write_text(txt, encoding='utf-8')
    print('created login.html')

# Create logs page from dashboard template
logs_path = root / 'logs.html'
if not logs_path.exists():
    template = (root / 'dashboard.html').read_text(encoding='utf-8')
    template = template.replace('<title>CampusSync AI | College ERP</title>', '<title>CampusSync AI | Logs</title>')
    template = template.replace('Dashboard</a>', 'Logs</a>')
    template = template.replace('<li class="active"><a href="dashboard.html">Dashboard</a></li>', '<li><a href="dashboard.html">Dashboard</a></li>')
    template = template.replace('<li><a href="students.html">Students</a></li>', '<li><a href="students.html">Students</a></li>')
    template = template.replace('<li><a href="support.html">Support</a></li>', '<li><a href="support.html">Support</a></li>')
    template = template.replace('<li><a href="logs.html">Logs</a></li>\n', '')
    template = template.replace('<li class="active"><a href="dashboard.html">Dashboard</a></li>', '<li class="active"><a href="logs.html">Logs</a></li>')
    template = template.replace('Welcome back, <span id="greetingName">Student</span>', 'Login & System Logs')
    template = template.replace('Campus ERP updated automatically in smart AI mode.', 'Review login history, audit events, and system activity across CampusSync.')
    template = template.replace('id="dailyStatus">Dashboard view active</span>', 'id="dailyStatus">Logs view active</span>')
    template = template.replace('id="logText">Viewing the Dashboard section in CampusSync.</p>', 'id="logText">Viewing the Logs section in CampusSync.</p>')
    template = template.replace('id="studentCount">5,230</strong>', 'id="studentCount">5,230</strong>')
    template = template.replace('id="attendanceRate">92%</strong>', 'id="attendanceRate">--</strong>')
    template = template.replace('id="classCount">12</strong>', 'id="classCount">--</strong>')
    template = template.replace('Auto update cycle', 'Activity log')
    template = template.replace('AI Update Cycle', 'Login Activity')
    template = template.replace('NovaAI is ready to help with daily updates.', 'The login log shows recent access and system events for CampusSync.')
    # Replace cards content with log entries
    log_cards = '''            <article class="card">
              <span>Recent Logins</span>
              <strong id="studentCount">12</strong>
              <div class="mini-metrics">
                <div class="metric">
                  <span>Today</span>
                  <strong>+3</strong>
                </div>
              </div>
            </article>
            <article class="card">
              <span>Security Events</span>
              <strong id="attendanceRate">5</strong>
              <div class="mini-metrics">
                <div class="metric">
                  <span>Alerts</span>
                  <strong>2</strong>
                </div>
              </div>
            </article>
            <article class="card">
              <span>Successful Logins</span>
              <strong id="classCount">11</strong>
              <div class="mini-metrics">
                <div class="metric">
                  <span>Verified</span>
                  <strong>Yes</strong>
                </div>
              </div>
            </article>
            <article class="card">
              <span>Recent Activity</span>
              <strong id="autoModeChip">Live</strong>
              <div class="mini-metrics">
                <div class="metric">
                  <span>Updates</span>
                  <strong>7</strong>
                </div>
              </div>
            </article>'''
    template = template.replace(template.split('<article class="card">')[1].split('</article>')[0] + '</article>', '', 1)
    # Insert log cards after first card section
    template = template.replace('        <section class="cards">\n          <article class="card">', '        <section class="cards">\n' + log_cards + '\n          <article class="card">', 1)
    logs_path.write_text(template, encoding='utf-8')
    print('created logs.html')
else:
    print('logs.html already exists')
