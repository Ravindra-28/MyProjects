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
else:
    page = page.replace('<li><a href="logs.html">Logs</a></li>', '<li class="active"><a href="logs.html">Logs</a></li>')

logs_content = '''        <section class="cards">
          <article class="card">
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
          </article>
        </section>

        <section class="grid panel-grid">
          <div class="panel">
            <h3>Login History</h3>
            <p>Track secure access events and recent sign-ins for CampusSync Campus ERP.</p>
            <div class="list-card" id="announcementList">
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
            </div>
          </div>

          <div class="panel ai-panel">
            <div class="toggle-row">
              <div>
                <h3>AI Assistant</h3>
                <p>Ask Nova about login history, campus security, or recent access events.</p>
              </div>
              <label class="toggle">
                <input type="checkbox" id="autoModeToggle" checked onchange="toggleAutoMode()">
                <span class="slider"></span>
              </label>
            </div>

            <div class="input-group">
              <input type="text" id="question" placeholder="Ask your AI assistant anything..." />
              <div style="display:flex; gap:10px; flex-wrap: wrap;">
                <button type="button" onclick="setQuickPrompt('Show today\'s login history')">Login</button>
                <button type="button" onclick="setQuickPrompt('What are the latest security events?')">Security</button>
                <button type="button" onclick="setQuickPrompt('How many logins were successful today?')">Activity</button>
              </div>
              <button type="button" onclick="askAI()">Send to Nova</button>
            </div>

            <div class="response-box" id="response">NovaAI is ready to help with login and security questions.</div>
          </div>
        </section>
'''

page = re.sub(r'<section class="cards">[\s\S]*?<section class="panel">', logs_content + '<section class="panel">', page, count=1)

(logs := root / 'logs.html').write_text(page, encoding='utf-8')
print('Rebuilt logs.html cleanly')
