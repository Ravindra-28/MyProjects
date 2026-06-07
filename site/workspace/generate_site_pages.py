from pathlib import Path
import re

root = Path('site')
template_path = root / 'campussync-erp.html'
text = template_path.read_text(encoding='utf-8')

pages = {
    'Dashboard': {
        'file': 'dashboard.html',
        'title': 'Welcome back, <span id="greetingName">Student</span>',
        'description': 'Campus ERP updated automatically in smart AI mode.',
        'attendanceRate': 92,
        'studentCount': 5230,
        'classCount': 12,
        'dailyStatus': 'Dashboard view active',
        'announcements': [
            'Assignment Reminder: Submit lab report by 6 PM today.',
            'Cultural Fest registration open until Friday.',
            'Library hours updated from Monday.',
        ],
        'logText': 'Viewing the Dashboard section in CampusSync.',
    },
    'Students': {
        'file': 'students.html',
        'title': 'Student directory overview',
        'description': 'Review student profiles, class progress, and campus engagement.',
        'attendanceRate': 94,
        'studentCount': 5280,
        'classCount': 14,
        'dailyStatus': 'Students view active',
        'announcements': [
            'New student registrations processed successfully.',
            'Top performers recognized in the monthly leaderboard.',
            'Mentorship sessions scheduled for this week.',
        ],
        'logText': 'Viewing the Students section in CampusSync.',
    },
    'Attendance': {
        'file': 'attendance.html',
        'title': 'Attendance analytics',
        'description': 'Track daily attendance and improve classroom participation.',
        'attendanceRate': 96,
        'studentCount': 5230,
        'classCount': 13,
        'dailyStatus': 'Attendance view active',
        'announcements': [
            'Attendance report generated for today.',
            'Absent alerts sent to parents and counselors.',
            'Attendance trend improved by 3% this week.',
        ],
        'logText': 'Viewing the Attendance section in CampusSync.',
    },
    'Exams': {
        'file': 'exams.html',
        'title': 'Exam schedule and results',
        'description': 'View upcoming exams, results, and preparation alerts.',
        'attendanceRate': 91,
        'studentCount': 5230,
        'classCount': 12,
        'dailyStatus': 'Exams view active',
        'announcements': [
            'Midterm schedule finalized for next Monday.',
            'Exam hall assignments published to students.',
            'Study resources available in the AI assistant.',
        ],
        'logText': 'Viewing the Exams section in CampusSync.',
    },
    'Fees': {
        'file': 'fees.html',
        'title': 'Fees dashboard',
        'description': 'Check fee statuses, dues, and secure payment reminders.',
        'attendanceRate': 92,
        'studentCount': 5230,
        'classCount': 12,
        'dailyStatus': 'Fees view active',
        'announcements': [
            'Fee due reminders sent to students with pending balances.',
            'Online payment portal is now faster and secure.',
            'Scholarship updates are available in the finance panel.',
        ],
        'logText': 'Viewing the Fees section in CampusSync.',
    },
    'Library': {
        'file': 'library.html',
        'title': 'Library resources',
        'description': 'Explore library hours, new arrivals, and book requests.',
        'attendanceRate': 92,
        'studentCount': 5230,
        'classCount': 12,
        'dailyStatus': 'Library view active',
        'announcements': [
            'New AI and data science books added to the library.',
            'Library hours extended during exam week.',
            'Digital resource access has been updated.',
        ],
        'logText': 'Viewing the Library section in CampusSync.',
    },
    'Placement': {
        'file': 'placement.html',
        'title': 'Placement activity',
        'description': 'Monitor placement drives, offers, and candidate readiness.',
        'attendanceRate': 92,
        'studentCount': 5230,
        'classCount': 12,
        'dailyStatus': 'Placement view active',
        'announcements': [
            'Placement drive registrations are now open.',
            'Top companies are scheduled for next month.',
            'Interview preparation sessions are live.',
        ],
        'logText': 'Viewing the Placement section in CampusSync.',
    },
    'Support': {
        'file': 'support.html',
        'title': 'Campus support',
        'description': 'Access campus support, helpdesk, and student services.',
        'attendanceRate': 92,
        'studentCount': 5230,
        'classCount': 12,
        'dailyStatus': 'Support view active',
        'announcements': [
            'Support tickets are being handled within 24 hours.',
            'Live chat is available for urgent campus needs.',
            'Student service feedback is now easier to submit.',
        ],
        'logText': 'Viewing the Support section in CampusSync.',
    },
}
nav_template = '\n      <ul class="nav-list">\n'
for section, data in pages.items():
    active = ' class="active"' if section == 'Dashboard' else ''
    nav_template += f'          <li{active}><a href="{data["file"]}">{section}</a></li>\n'
nav_template += '        </ul>'

def page_nav(section):
    nav = '      <ul class="nav-list">\n'
    for name, data in pages.items():
        active = ' class="active"' if name == section else ''
        nav += f'        <li{active}><a href="{data["file"]}">{name}</a></li>\n'
    nav += '      </ul>'
    return nav

nav_block = re.search(r'<ul class="nav-list">.*?</ul>', text, re.S)
if not nav_block:
    raise SystemExit('nav list not found')

for section, data in pages.items():
    page_text = re.sub(r'<ul class="nav-list">.*?</ul>', page_nav(section), text, count=1, flags=re.S)
    page_text = page_text.replace('Welcome back, <span id="greetingName">Student</span>', data['title'])
    page_text = page_text.replace('<p>Campus ERP updated automatically in smart AI mode.</p>', f'<p>{data["description"]}</p>')
    page_text = page_text.replace('id="studentCount">5,230</strong>', f'id="studentCount">{data["studentCount"]:,}</strong>')
    page_text = page_text.replace('id="attendanceRate">92%</strong>', f'id="attendanceRate">{data["attendanceRate"]}%</strong>')
    page_text = page_text.replace('id="classCount">12</strong>', f'id="classCount">{data["classCount"]}</strong>')
    page_text = page_text.replace('id="dailyStatus">Auto mode active</span>', f'id="dailyStatus">{data["dailyStatus"]}</span>')
    announcement_html = ''.join([f'              <div class="list-item">\n                <strong>{item}</strong>\n                <span class="chip">{section}</span>\n              </div>\n' for item in data['announcements']])
    page_text = re.sub(r'<div class="list-card" id="announcementList">.*?</div>\s*</div>', f'<div class="list-card" id="announcementList">\n{announcement_html}            </div>\n          </div>', page_text, count=1, flags=re.S)
    page_text = page_text.replace('id="logText">CampusSync is managing schedule and attendance updates automatically. Students see the latest information without manual refresh.</p>', f'id="logText">{data["logText"]}</p>')
    state_block = re.search(r'const state = \{.*?\};', page_text, re.S)
    if not state_block:
        raise SystemExit('state block not found')
    new_state = f"const state = {{\n      autoMode: true,\n      nextRefreshSeconds: 15,\n      attendanceRate: {data['attendanceRate']},\n      studentCount: {data['studentCount']},\n      classCount: {data['classCount']},\n      userName: 'Student',\n      role: 'Student',\n      announcements: [\n"
    for item in data['announcements']:
        new_state += f"        '{item}',\n"
    new_state += "      ],\n      logMessages: [\n        'Auto update started for daily attendance.',\n        'Assignment reminders synced with student profiles.',\n        'Library and placement notices refreshed.',\n      ],\n    };"
    page_text = page_text[:state_block.start()] + new_state + page_text[state_block.end():]
    out_path = root / data['file']
    out_path.write_text(page_text, encoding='utf-8')
    if section == 'Dashboard':
        (root / 'campussync-erp.html').write_text(page_text, encoding='utf-8')

print('Generated pages:')
for data in pages.values():
    print('-', data['file'])
print('- updated site/campussync-erp.html as dashboard alias')
