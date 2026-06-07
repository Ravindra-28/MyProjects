from pathlib import Path
import re

root = Path('site')
base = (root / 'dashboard.html').read_text(encoding='utf-8')
page = base
page = page.replace('<title>CampusSync AI | College ERP</title>', '<title>CampusSync AI | Logs</title>')
page = page.replace('<h2>Welcome back, <span id="greetingName">Student</span></h2>', '<h2>Login & System Logs</h2>')
page = page.replace('<p>Campus ERP updated automatically in smart AI mode.</p>', '<p>Review login history, audit events, and system access details across CampusSync.</p>')
page = page.replace('id="dailyStatus">Dashboard view active</span>', 'id="dailyStatus">Logs view active</span>')
page = page.replace('id="logText">Viewing the Dashboard section in CampusSync.</p>', 'id="logText">Viewing the Logs section in CampusSync.</p>')
page = page.replace('<li class="active"><a href="dashboard.html">Dashboard</a></li>', '<li><a href="dashboard.html">Dashboard</a></li>')
if '<a href="logs.html">Logs</a>' not in page:
    page = page.replace('<li><a href="support.html">Support</a></li>', '<li><a href="support.html">Support</a></li>\n        <li class="active"><a href="logs.html">Logs</a></li>')

cards_html = '''          <article class="card">
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
            <span>Login Activity</span>
            <strong id="nextRefresh">Auto refresh in 00:15</strong>
            <div class="mini-metrics">
              <div class="metric">
                <span>Status</span>
                <span class="chip" id="autoModeChip">Enabled</span>
              </div>
            </div>
          </article>'''
page = re.sub(r'<section class="cards">[\s\S]*?<\/section>', f'<section class="cards">\n{cards_html}\n        </section>', page, count=1)

log_list = '''            <div class="list-card" id="announcementList">
              <div class="list-item">
                <strong>Login success — Ravindra19</strong>
                <span class="chip">Today</span>
              </div>
              <div class="list-item">
                <strong>System audit completed</strong>
                <span class="chip">Security</span>
              </div>
              <div class="list-item">
                <strong>Unauthorized access block logged</strong>
                <span class="chip">Alert</span>
              </div>
            </div>'''
page = re.sub(r'<div class="list-card" id="announcementList">[\s\S]*?<\/div>\s*<\/div>', f'{log_list}\n          </div>', page, count=1)
page = page.replace('Ask Nova anything about your campus schedule, attendance, fees, or exams.', 'Ask Nova about login history, campus security, or recent access events.')
page = page.replace('NovaAI is ready to help with daily updates.', 'NovaAI is ready to help with login and security questions.')

(logs := root / 'logs.html').write_text(page, encoding='utf-8')
print('Fixed logs.html')
