from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, HRFlowable
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "CircusCircusLimes_Project_Study_Guide.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

NAVY = HexColor("#17325C")
BLUE = HexColor("#2E74B5")
PALE = HexColor("#EAF1F8")
GREEN = HexColor("#E6F4EA")
GOLD = HexColor("#FFF4D6")
RED = HexColor("#FCE8E6")
INK = HexColor("#172033")
GRAY = HexColor("#5F6B7A")
LINE = HexColor("#C8D2DF")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=27, leading=31, textColor=NAVY, alignment=TA_CENTER, spaceAfter=12))
styles.add(ParagraphStyle(name="CoverSub", parent=styles["Normal"], fontSize=13, leading=18, textColor=GRAY, alignment=TA_CENTER, spaceAfter=10))
styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=18, leading=22, textColor=NAVY, spaceBefore=4, spaceAfter=10, keepWithNext=True))
styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=BLUE, spaceBefore=10, spaceAfter=5, keepWithNext=True))
styles.add(ParagraphStyle(name="H3x", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=NAVY, spaceBefore=7, spaceAfter=3, keepWithNext=True))
styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontName="Helvetica", fontSize=10.2, leading=14.2, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name="Smallx", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.5, leading=11.2, textColor=INK, spaceAfter=3))
styles.add(ParagraphStyle(name="Tinyx", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.6, leading=9.4, textColor=INK))
styles.add(ParagraphStyle(name="Codex", parent=styles["BodyText"], fontName="Courier", fontSize=8.4, leading=11.2, textColor=INK, leftIndent=10, rightIndent=10, spaceBefore=3, spaceAfter=6, backColor=HexColor("#F4F6F8"), borderPadding=6))
styles.add(ParagraphStyle(name="Question", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=10.3, leading=13.5, textColor=NAVY, spaceBefore=5, spaceAfter=2))
styles.add(ParagraphStyle(name="Callout", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.6, leading=13, textColor=INK, leftIndent=10, rightIndent=10, spaceBefore=4, spaceAfter=8, borderPadding=8, borderWidth=.6, borderColor=LINE, backColor=PALE))
styles.add(ParagraphStyle(name="Bulletx", parent=styles["BodyText"], fontName="Helvetica", fontSize=10, leading=13.5, leftIndent=17, firstLineIndent=-9, bulletIndent=4, spaceAfter=3, textColor=INK))

story = []

def P(text, style="Bodyx"): story.append(Paragraph(text, styles[style]))
def H1(text): story.append(Paragraph(text, styles["H1x"]))
def H2(text): story.append(Paragraph(text, styles["H2x"]))
def H3(text): story.append(Paragraph(text, styles["H3x"]))
def bullet(text): story.append(Paragraph("• " + text, styles["Bulletx"]))
def callout(label, text, color=None):
    s = ParagraphStyle("temp", parent=styles["Callout"], backColor=color or PALE)
    story.append(Paragraph(f"<b>{label}</b> {text}", s))
def qa(q, a):
    story.append(Paragraph(q, styles["Question"]))
    story.append(Paragraph(a, styles["Bodyx"]))
def table(rows, widths, header=True, tiny=False):
    data = [[Paragraph(str(c), styles["Tinyx" if tiny else "Smallx"]) for c in row] for row in rows]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    cmds = [("VALIGN", (0,0), (-1,-1), "TOP"), ("GRID", (0,0), (-1,-1), .45, LINE),
            ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
            ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5)]
    if header:
        cmds += [("BACKGROUND", (0,0), (-1,0), NAVY), ("TEXTCOLOR", (0,0), (-1,0), colors.white)]
    for i in range(1 if header else 0, len(rows)):
        if i % 2 == 0: cmds.append(("BACKGROUND", (0,i), (-1,i), HexColor("#F7F9FC")))
    t.setStyle(TableStyle(cmds)); story.append(t); story.append(Spacer(1,8))

# Cover
story += [Spacer(1, 0.7*inch), Paragraph("CIRCUSCIRCUSLIMES", styles["CoverTitle"]),
          Paragraph("Project Study Guide", styles["CoverSub"]), Spacer(1, 8),
          HRFlowable(width="72%", thickness=2, color=BLUE, hAlign="CENTER"), Spacer(1, 18)]
P("A plain-language, printable guide to the DishCourse Flask forum: startup, routing, models, templates, MySQL persistence, direct messages, profile updates, and the request-response mental model.", "CoverSub")
story += [Spacer(1, 24)]
callout("CURRENT CODE VS. TARGET DESIGN", "This guide treats the files in the repository as the source of truth for what works now. The supplied target UML is used to explain the intended direction. Any mismatch is labeled explicitly.", GREEN)
story += [Spacer(1, 18)]
P("Prepared from the project snapshot on August 21, 2026", "CoverSub")
P("Best use: read one section, cover the answer, and explain it aloud in your own words.", "CoverSub")
story.append(PageBreak())

H1("How to use this guide")
P("Do not try to memorize every line. Learn the path a request takes, the job of each module, and the database relationships. Once that mental map is stable, individual functions become much easier to understand.")
H2("The two-layer reading method")
table([
    ["Layer", "Question to ask", "CircusCircusLimes answer"],
    ["1. Purpose", "What does this thing do?", "It is a Flask discussion forum branded as DishCourse. People can create accounts, browse subforums, publish posts, comment, react, send direct messages, and manage profile details."],
    ["2. Parts", "What are the main pieces and how do they connect?", "Flask receives requests; blueprints route them to controller functions; SQLAlchemy reads/writes MySQL; Jinja templates and CSS build the response; Flask-Login tracks the current user."],
], [0.8*inch, 1.55*inch, 4.15*inch])
H2("Fast mental model")
P("Browser → Flask app → matching route/controller → validation and business logic → SQLAlchemy/MySQL → Jinja template or redirect → browser", "Codex")
callout("ONE-SENTENCE EXPLANATION", "CircusCircusLimes is a server-rendered Flask forum organized into feature blueprints, backed by MySQL through SQLAlchemy, with HTML generated from Jinja templates.")
H2("Reading map")
table([
 ["If you want to understand...", "Start here"],
 ["How the app boots", "<font name='Courier'>forum/app.py</font>, then <font name='Courier'>forum/__init__.py</font>, then <font name='Courier'>config.py</font>"],
 ["URLs and actions", "The seven blueprint files plus the <font name='Courier'>/</font> route in <font name='Courier'>forum/app.py</font>"],
 ["Stored information", "<font name='Courier'>forum/models.py</font>"],
 ["Validation", "<font name='Courier'>forum/user.py</font> and validators at the bottom of <font name='Courier'>forum/models.py</font>"],
 ["What users see", "<font name='Courier'>forum/templates/</font> and <font name='Courier'>forum/static/</font>"],
 ["Containers and MySQL", "<font name='Courier'>compose.yaml</font>, <font name='Courier'>Dockerfile</font>, <font name='Courier'>config.py</font>"],
], [2.25*inch, 4.25*inch])
story.append(PageBreak())

H1("1. Startup: how the application comes alive")
H2("Startup components")
bullet("<b>Dockerfile</b> builds a Python 3.11 image, installs requirements, copies the project, exposes port 5000, and starts Gunicorn.")
bullet("<b>compose.yaml</b> starts two services: the web application and MySQL 8.4. It passes database environment variables to the web container.")
bullet("<b>forum/app.py</b> imports and calls <font name='Courier'>create_app()</font>, creates the Flask-Login manager, defines the home route, and seeds starter subforums if the database is empty.")
bullet("<b>forum/__init__.py</b> contains the app factory, applies configuration, registers seven blueprints, connects SQLAlchemy, and creates tables.")
bullet("<b>config.py</b> builds the MySQL connection URL from <font name='Courier'>DB_USER</font>, <font name='Courier'>DB_PASSWORD</font>, <font name='Courier'>DB_HOST</font>, and <font name='Courier'>DB_NAME</font>.")
H2("Exact startup sequence")
for i, txt in enumerate([
 "Gunicorn imports the object named <font name='Courier'>app</font> from <font name='Courier'>forum.app</font>.",
 "Importing <font name='Courier'>forum/app.py</font> runs <font name='Courier'>app = create_app()</font>.",
 "<font name='Courier'>create_app()</font> constructs Flask, loads <font name='Courier'>config.Config</font>, and registers the posts, comments, reactions, messages, settings, profile, and routes blueprints.",
 "<font name='Courier'>db.init_app(app)</font> connects the SQLAlchemy extension to this Flask app.",
 "Inside an application context, <font name='Courier'>db.create_all()</font> creates any missing tables, then the app object is returned.",
 "Back in <font name='Courier'>forum/app.py</font>, Flask-Login is attached. <font name='Courier'>load_user()</font> tells Flask-Login how to reload a user by ID.",
 "A second app context runs table creation again and seeds five initial subforums if none exist.",
 "Gunicorn listens on <font name='Courier'>0.0.0.0:5000</font> inside the web container; Docker maps the host's <font name='Courier'>APP_PORT</font> to that port.",
], 1): P(f"<b>{i}.</b> {txt}")
callout("WATCH OUT", "<font name='Courier'>db.create_all()</font> appears twice. It is normally harmless because it creates missing tables rather than recreating existing ones, but it is redundant. It also is not a migration system: schema changes should eventually use a migration tool.", GOLD)
qa("How does Flask start?", "In production-style container startup, Gunicorn imports <font name='Courier'>forum.app:app</font>. During that import, Python executes <font name='Courier'>app = create_app()</font>. For local development, the Flask command uses <font name='Courier'>FLASK_APP = 'forum.app'</font> and finds the same app object.")
qa("How does create_app() execute?", "It executes as a normal Python function call during module import. It builds and returns the configured Flask object.")
qa("How are blueprints registered?", "Each feature file creates a <font name='Courier'>Blueprint</font> object. <font name='Courier'>create_app()</font> imports those objects and calls <font name='Courier'>app.register_blueprint(...)</font> for each one.")
story.append(PageBreak())

H1("2. Routing: URL to controller function")
P("A route connects an HTTP method and URL pattern to a Python function. Flask checks its URL map, selects the matching function, and calls it. In this app, route functions are the controllers: they interpret input, apply business rules, use models, and choose a response.")
H2("Complete live route inventory")
routes = [
 ["Method / URL", "Endpoint function", "Module", "Login?"],
 ["GET /", "index", "app.py", "No"],
 ["POST /action_login", "action_login", "routes.py", "No"],
 ["GET /action_logout", "action_logout", "routes.py", "Intended yes*"],
 ["POST /action_createaccount", "action_createaccount", "routes.py", "No"],
 ["GET /subforum?sub=ID", "subforum", "routes.py", "No"],
 ["GET /loginform", "loginform", "routes.py", "No"],
 ["GET /about | /contact | /house-rules", "about / contact / house_rules", "routes.py", "No"],
 ["GET /addpost?sub=ID", "addpost", "posts.py", "Yes"],
 ["GET /viewpost?post=ID", "viewpost", "posts.py", "No; private posts require login"],
 ["POST /action_post?sub=ID", "action_post", "posts.py", "Yes"],
 ["POST /action_comment?post=ID", "comment", "comments.py", "Yes"],
 ["POST /action_reaction", "react", "reactions.py", "Yes"],
 ["GET /messages", "inbox", "messages.py", "Yes"],
 ["GET /messages/&lt;username&gt;", "conversation", "messages.py", "Yes"],
 ["POST /action_send_message", "send_message", "messages.py", "Yes"],
 ["GET /settings", "settings_page", "settings.py", "Yes"],
 ["POST /action_change_password", "change_password", "settings.py", "Yes"],
 ["GET /profile", "profile_page", "profile.py", "Yes"],
 ["POST /action_update_username", "update_username", "profile.py", "Yes"],
 ["POST /action_update_email", "update_email", "profile.py", "Yes"],
 ["POST /action_update_avatar", "update_avatar", "profile.py", "Yes"],
 ]
table(routes, [2.2*inch, 1.65*inch, 1.35*inch, 1.3*inch], tiny=True)
P("* In <font name='Courier'>routes.py</font>, <font name='Courier'>@login_required</font> is placed above <font name='Courier'>@rt.route</font> for logout. Decorator order matters; the conventional and clearly protected form places <font name='Courier'>@rt.route</font> first and <font name='Courier'>@login_required</font> directly above the function.", "Smallx")
H2("How HTTP requests are routed")
P("Example: a browser submits a heart reaction. The form sends <font name='Courier'>POST /action_reaction</font>. Flask's URL map points that request to <font name='Courier'>reactions.react</font>. The controller validates the reaction, queries the post and existing reaction, mutates the database, commits, then returns a redirect to the post page.")
callout("DIAGRAM CORRECTION", "The supplied target UML shows <font name='Courier'>/action_react?post=&lt;id&gt;</font>. The current code actually uses <font name='Courier'>POST /action_reaction</font> and receives <font name='Courier'>post_id</font> plus <font name='Courier'>reaction_type</font> from form data.", RED)

H1("3. Data model: what is stored and how it connects")
P("A SQLAlchemy model is a Python class mapped to a database table. A model object represents one row. Columns store values, foreign keys connect rows, and relationships let Python navigate those connections.")
table([
 ["Model", "Important fields", "Relationships / behavior"],
 ["User", "id, username, password_hash, email, admin, avatar_filename", "Has posts, comments, reactions, sent_messages, received_messages. Passwords are hashed; <font name='Courier'>check_password</font> verifies them."],
 ["Post", "id, title, content, postdate, user_id, subforum_id, is_public", "Belongs to one user and one subforum; has many comments and reactions. Computes a cached relative-time string."],
 ["Comment", "id, content, postdate, user_id, post_id", "Belongs to one user and one post. Also computes relative time."],
 ["Subforum", "id, title, description, parent_id, hidden", "Can have child subforums and many posts. <font name='Courier'>parent_id</font> makes the hierarchy self-referential."],
 ["Reaction", "id, reaction_type, user_id, post_id", "Belongs to one user and one post. A unique constraint permits only one reaction per user/post pair."],
 ["Message", "id, content, sentdate, is_read, sender_id, recipient_id", "Has two separate relationships to User: sender and recipient. Backrefs expose sent and received messages."],
], [0.85*inch, 2.35*inch, 3.3*inch], tiny=True)
H2("Relationship map")
P("User 1 → many Posts\nUser 1 → many Comments\nUser 1 → many Reactions\nSubforum 1 → many Posts\nPost 1 → many Comments\nPost 1 → many Reactions\nUser 1 → many sent Messages; User 1 → many received Messages", "Codex")
H2("What SQLAlchemy does here")
bullet("<font name='Courier'>Model.query.filter(...)</font> builds and executes SELECT queries.")
bullet("<font name='Courier'>db.session.add(object)</font> stages a new row; appending through a relationship can also associate new objects.")
bullet("<font name='Courier'>db.session.delete(object)</font> stages deletion.")
bullet("<font name='Courier'>db.session.commit()</font> completes the transaction and makes changes persistent.")
bullet("A <font name='Courier'>ForeignKey</font> stores the linked row's ID. A <font name='Courier'>relationship</font>/<font name='Courier'>backref</font> gives convenient Python attribute access.")
callout("TARGET UML MISMATCHES", "There is no live <font name='Courier'>UserSettings</font> class. Theme and email-notification fields are planned, not implemented. Post <font name='Courier'>format</font> and <font name='Courier'>media_url</font> are also absent. The live Message field is named <font name='Courier'>content</font>, not <font name='Courier'>body</font>. The live Reaction field is <font name='Courier'>reaction_type</font>, not <font name='Courier'>type</font>.", GOLD)
qa("What are the classes and where are they?", "The six database model classes—User, Post, Subforum, Comment, Reaction, and Message—are all in <font name='Courier'>forum/models.py</font>. Flask itself is a class instantiated in <font name='Courier'>create_app()</font>; each Blueprint is also an object created in its feature module.")
story.append(PageBreak())

H1("4. User utilities and validation")
P("Validation answers: “Is this input shaped correctly?” Account checks answer: “Does this value already exist?” These are helper functions because several controllers can reuse them.")
table([
 ["Helper", "Rule / result", "Used for"],
 ["valid_username", "4-40 characters; letters, numbers, ! @ # % &", "Account creation and username update"],
 ["valid_password", "6-40 characters; same allowed character set", "Password change (account creation currently does not enforce it)"],
 ["valid_email", "Simple pattern requiring text@text.domain", "Profile email update"],
 ["username_taken", "Queries User and returns a row or None", "Prevent duplicate usernames"],
 ["email_taken", "Queries User and returns a row or None", "Prevent duplicate emails"],
 ["valid_avatar_filename", "Allows png, jpg, jpeg, gif, webp", "Avatar upload"],
 ["avatar_extension", "Returns lower-case extension", "Build stored avatar filename"],
 ["valid_title / valid_content", "Title >4 and <140; content >10 and <5000", "New posts"],
 ["valid_comment", "Trimmed content 1-1000 characters", "New comments"],
 ["valid_message", "Trimmed content 1-2000 characters", "Direct messages"],
], [1.4*inch, 2.6*inch, 2.5*inch], tiny=True)
H2("Password handling")
P("The application never needs to store the original password. The User constructor calls Werkzeug's <font name='Courier'>generate_password_hash()</font>. Login and password change call <font name='Courier'>check_password_hash()</font>. A successful password change replaces the stored hash and commits.")
callout("IMPORTANT GAP", "Account creation currently has the <font name='Courier'>valid_password(password)</font> check commented out. A password that would be rejected on the settings page may still be accepted during signup.", RED)
H2("Avatar safety checks")
P("The controller cleans the original name with <font name='Courier'>secure_filename</font>, allows only selected extensions, checks that the stream is at most 2 MB, creates a random server-side filename, saves into <font name='Courier'>forum/static/images/avatars/</font>, commits that filename to User, and removes the old avatar file.")
P("The global <font name='Courier'>MAX_CONTENT_LENGTH</font> is about 2.5 MB, providing an earlier request-size backstop.")
story.append(PageBreak())

H1("5. Presentation: templates, shared layout, and CSS")
P("The app uses server-side rendering. A controller calls <font name='Courier'>render_template()</font>, Jinja fills placeholders using Python data, and Flask returns completed HTML to the browser.")
H2("How templates receive data")
table([
 ["Controller call", "Template receives"],
 ["<font name='Courier'>render_template('subforums.html', subforums=subforums)</font>", "A query result containing top-level subforums"],
 ["<font name='Courier'>render_template('viewpost.html', post=..., comments=..., like_count=...)</font>", "Post, breadcrumb path, comments, three counts, and the current user's reaction"],
 ["<font name='Courier'>render_template('conversation.html', other=..., thread_messages=...)</font>", "The conversation partner and ordered message history"],
], [3.45*inch, 3.05*inch])
H2("Shared presentation structure")
bullet("Feature templates use or extend <font name='Courier'>layout.html</font>.")
bullet("The layout includes <font name='Courier'>header.html</font>, <font name='Courier'>sidebar.html</font>, and <font name='Courier'>right_sidebar.html</font> so common UI is not duplicated.")
bullet("It loads local <font name='Courier'>bootstrap.min.css</font>, Bootstrap Icons from a CDN, and custom <font name='Courier'>style.css</font>.")
bullet("It displays ordinary validation errors and flashed success/error messages.")
bullet("The messages blueprint adds <font name='Courier'>unread_message_count</font> to every template through an app context processor.")
H2("Template vocabulary")
table([
 ["Jinja syntax", "Meaning"],
 ["<font name='Courier'>{{ value }}</font>", "Print a value into HTML (normally escaped)."],
 ["<font name='Courier'>{% if ... %}</font>", "Conditionally include markup."],
 ["<font name='Courier'>{% for ... %}</font>", "Repeat markup for each item."],
 ["<font name='Courier'>{% include 'header.html' %}</font>", "Insert a shared partial."],
 ["<font name='Courier'>{% block body %}</font>", "Define the region a child template fills."],
], [2.25*inch, 4.25*inch])
callout("PRESENTATION VS. BUSINESS LOGIC", "Templates should mainly display decisions already made. Rules such as “cannot message yourself,” “private posts require login,” and “one reaction per user/post” belong in controllers and models, not in CSS or HTML.")
story.append(PageBreak())

H1("6. Database and persistence")
qa("What are the database components?", "MySQL 8.4 is the database server; PyMySQL is the Python driver; SQLAlchemy maps Python models to SQL; Flask-SQLAlchemy connects that mapping to Flask; <font name='Courier'>config.py</font> builds the connection URL; and Docker Compose supplies credentials and persistent storage.")
qa("Where does persistence occur?", "Application code commits through <font name='Courier'>db.session.commit()</font>. MySQL writes data files under <font name='Courier'>/var/lib/mysql</font> inside the database container, backed by the named Docker volume <font name='Courier'>dishcourse_mysql_data</font>. The volume lets data survive replacement of an individual container.")
H2("Database environment variables")
table([
 ["Application variable", "Compose source", "Meaning"],
 ["DB_USER", "MYSQL_USER", "MySQL account used by Flask"],
 ["DB_PASSWORD", "MYSQL_PASSWORD", "That account's password"],
 ["DB_HOST", "db", "Compose service hostname for MySQL"],
 ["DB_NAME", "MYSQL_DATABASE", "Database/schema name"],
 ["APP_PORT", "Host .env / shell", "Host port mapped to container port 5000"],
 ["DB_PORT", "Host .env / shell", "Optional host-only mapping to MySQL port 3306"],
], [1.35*inch, 1.55*inch, 3.6*inch])
H2("How the database is created")
P("Compose starts MySQL with <font name='Courier'>MYSQL_DATABASE</font>. When the Flask app starts, <font name='Courier'>db.create_all()</font> sends CREATE TABLE statements for missing model tables. If the Subforum table is empty, <font name='Courier'>init_site()</font> inserts the default categories and commits them.")
callout("CURRENT, NOT OLD README", "The README still contains historical SQLite notes, but the current <font name='Courier'>config.py</font> uses <font name='Courier'>mysql+pymysql</font> and <font name='Courier'>compose.yaml</font> defines MySQL. For the current code, MySQL is the correct answer.", GREEN)
H2("Transaction pattern")
P("validate input → create or change model objects → <font name='Courier'>db.session.add()</font> if needed → <font name='Courier'>db.session.commit()</font> → redirect", "Codex")
story.append(PageBreak())

H1("7. Direct messages: complete feature walkthrough")
H2("Where is the messages blueprint?")
P("It is created in <font name='Courier'>forum/messages.py</font> as <font name='Courier'>messages = Blueprint('messages', __name__)</font> and registered in <font name='Courier'>forum/__init__.py</font>.")
H2("What changed for direct messages?")
bullet("Registered the new messages blueprint in the app factory.")
bullet("Added the Message model, its sender/recipient foreign keys and relationships, read status, timestamp, and relative-time method.")
bullet("Added message-content validation.")
bullet("Added inbox, conversation, and send-message controller routes.")
bullet("Added <font name='Courier'>messages_inbox.html</font> and <font name='Courier'>conversation.html</font>.")
bullet("Added navigation and unread-count UI, plus a “message this author” entry point on post pages.")
bullet("Added message styling to <font name='Courier'>style.css</font>.")
H2("Routes")
table([
 ["Route", "Purpose"],
 ["GET /messages", "Query all messages involving the current user, collapse them into one summary per conversation partner, sort by newest, and render the inbox."],
 ["GET /messages/&lt;username&gt;", "Load the two-way thread, reject nonexistent/self conversations, mark received unread messages as read, and render the conversation."],
 ["POST /action_send_message", "Validate recipient and content, create Message, attach sender and recipient, commit, and redirect to the conversation."],
], [2.1*inch, 4.4*inch])
H2("Request-response flow for sending a DM")
for i, txt in enumerate([
 "A logged-in user submits the conversation form with <font name='Courier'>recipient</font> and <font name='Courier'>content</font>.",
 "Flask matches <font name='Courier'>POST /action_send_message</font> to <font name='Courier'>messages.send_message</font>. The login decorator blocks anonymous access.",
 "The controller trims values and queries User by username.",
 "It rejects a missing recipient, a self-message, or content outside 1-2000 characters.",
 "It creates <font name='Courier'>Message(content, now)</font>, sets <font name='Courier'>sender</font> and <font name='Courier'>recipient</font>, adds it, and commits.",
 "It redirects to <font name='Courier'>/messages/&lt;username&gt;</font>. The browser follows with a GET.",
 "The conversation controller reloads the ordered thread and renders <font name='Courier'>conversation.html</font>.",
], 1): P(f"<b>{i}.</b> {txt}")
callout("WHY TWO USER FOREIGN KEYS?", "A message points to User twice for different roles. Explicit <font name='Courier'>foreign_keys</font> arguments remove ambiguity and let SQLAlchemy expose <font name='Courier'>message.sender</font> and <font name='Courier'>message.recipient</font>.")
story.append(PageBreak())

H1("8. Profile and settings: complete feature walkthrough")
H2("What is the profile blueprint?")
P("<font name='Courier'>forum/profile.py</font> owns the page and three independent update actions: username, email, and avatar. It is registered in <font name='Courier'>create_app()</font>; every profile route requires login.")
H2("What changed for profile?")
bullet("Added <font name='Courier'>avatar_filename</font> to User. The database stores only the generated filename; the image itself lives in the static avatar directory.")
bullet("Added the profile blueprint and its four routes.")
bullet("Added email and avatar validation helpers plus a 2 MB avatar limit.")
bullet("Added <font name='Courier'>profile.html</font>, adjusted the settings page so it focuses on password, and updated header/sidebar links.")
bullet("Added avatar rendering and profile styles; updated request-size configuration.")
H2("Profile routes")
table([
 ["Route", "Purpose"],
 ["GET /profile", "Render the current user's editable profile."],
 ["POST /action_update_username", "Validate format and uniqueness, update User.username, commit, flash result."],
 ["POST /action_update_email", "Validate format and uniqueness, update User.email, commit, flash result."],
 ["POST /action_update_avatar", "Validate and save image, update User.avatar_filename, commit, then remove the previous file."],
], [2.35*inch, 4.15*inch])
H2("Request-response flow: changing profile data")
P("The page deliberately uses separate forms. That means the server receives one focused change at a time.")
P("Browser form → matching POST route → <font name='Courier'>@login_required</font> → read form/file input → validate → update current User (and possibly save file) → commit → flash message → redirect to GET /profile → render updated values", "Codex")
H2("Profile vs. settings")
P("Profile owns avatar, username, and email. Settings currently owns only password change. The target UML's separate UserSettings record is future architecture, not current behavior.")
callout("FILE/DB CONSISTENCY NOTE", "The avatar controller commits the new filename before deleting the old file. This avoids losing the old file before the database update succeeds, though a filesystem failure after commit could leave an unused old file.", GOLD)
story.append(PageBreak())

H1("9. Core concepts in plain English")
concepts = [
 ("Flask", "A lightweight Python web framework. It receives HTTP requests, maps them to Python functions, and returns responses."),
 ("Server", "A program that listens for requests and sends responses. Here, Gunicorn runs the Flask app; MySQL is a separate database server."),
 ("Tech stack", "Python 3.11, Flask, Gunicorn, Flask-Login, Flask-SQLAlchemy/SQLAlchemy, PyMySQL, MySQL 8.4, Jinja2, HTML/CSS, Bootstrap, Docker and Docker Compose."),
 ("Blueprint", "A package of related Flask routes and behavior. It keeps one large application organized by feature."),
 ("Controller", "The route function that coordinates a request: read input, apply rules, call models, and choose a template or redirect."),
 ("Business logic", "Rules that make the forum behave correctly—for example validation, privacy checks, reaction toggling, and preventing self-messages. It mostly lives in route functions and reusable validators; the uniqueness constraint is in the model."),
 ("Decorator", "A wrapper written with <font name='Courier'>@</font> that changes function behavior. <font name='Courier'>@route</font> registers a URL; <font name='Courier'>@login_required</font> blocks anonymous users."),
 ("API", "A defined way for software parts to communicate. Flask's functions are an API for building web apps; the browser also interacts with URL endpoints."),
 ("REST API", "An HTTP API organized around resources and standard methods, often returning JSON. This project is mainly a server-rendered web app with action-style form routes, not a strict REST API."),
 ("rt in rt.route", "<font name='Courier'>rt</font> is the variable holding the blueprint named <font name='Courier'>routes</font>. <font name='Courier'>rt.route(...)</font> registers a function on that blueprint."),
 ("Module", "A Python file that can be imported. Examples: posts.py, messages.py, models.py, and user.py."),
 ("Template", "An HTML file with Jinja placeholders and control statements. Flask combines it with data to produce final HTML."),
 ("Persistence", "Data continues to exist after a request or process ends. MySQL plus its Docker volume provide persistence."),
 ("Virtual environment", "An isolated set of Python packages for one project, preventing dependency conflicts with other projects."),
 ("Port", "A numbered network doorway. Port 5000 is where the web process listens inside its container."),
 ("localhost", "The current computer. <font name='Courier'>http://localhost:5000</font> asks your own machine for an HTTP response on port 5000."),
 ("Docker", "A tool that packages applications and dependencies into containers. Compose describes how the web and database containers run together."),
]
for term, definition in concepts:
    story.append(KeepTogether([Paragraph(term, styles["H3x"]), Paragraph(definition, styles["Bodyx"])]))

H1("10. Feature flow charts and request-response sequences")
H2("Login")
P("POST form → routes.action_login → query User by username → verify hash → login_user(user) → redirect / → render subforums", "Codex")
H2("Create post")
P("GET /addpost?sub=ID → login check → render form → POST /action_post?sub=ID → validate title/content → create Post → connect User + Subforum → commit → redirect /viewpost?post=ID", "Codex")
H2("View a post")
P("GET /viewpost?post=ID → find Post → enforce private-post rule → load breadcrumb, comments, counts, user's reaction → render viewpost.html", "Codex")
H2("Comment")
P("POST /action_comment?post=ID → login check → validate ID and content → create Comment → connect User + Post → commit → redirect to post", "Codex")
H2("Reaction toggle")
P("POST /action_reaction → login check → validate type → find Post → find user's existing Reaction → same type: delete | different type: update | none: create → commit → redirect", "Codex")
H2("Password change")
P("POST /action_change_password → login check → verify current password → validate and compare new password → hash new password → commit → flash success → redirect settings", "Codex")
H2("General request-response sequence")
table([
 ["Stage", "What happens"],
 ["1. Request", "The browser sends method, URL, query string, form fields, cookies, and possibly a file."],
 ["2. Routing", "Flask finds the route whose method and URL pattern match."],
 ["3. Authentication", "If present, <font name='Courier'>login_required</font> checks session state before the controller proceeds."],
 ["4. Controller", "The route function parses and validates input and applies business rules."],
 ["5. Model/database", "SQLAlchemy queries or changes mapped objects; commit makes writes persistent."],
 ["6. Response", "The controller renders HTML, redirects, or returns an error string."],
 ["7. Browser", "The browser displays HTML or follows the redirect with another request."],
], [1.2*inch, 5.3*inch])
story.append(PageBreak())

H1("11. Current architecture vs. target architecture")
P("The target diagram is useful as a roadmap, but the current repository has moved partway toward it. Use this page to avoid blending present facts with planned work.")
table([
 ["Area", "Current repository", "Target / planned"],
 ["Blueprints", "7 registered: posts, comments, reactions, messages, settings, profile, routes", "Target labels the legacy routes blueprint as auth.py; the current file is still routes.py and also owns subforum/static-page routes."],
 ["Database", "MySQL through PyMySQL and SQLAlchemy", "Achieved."],
 ["Comments", "Many comments per post", "Achieved."],
 ["Reactions", "Like/dislike/heart with one reaction per user/post", "Achieved, but diagram route/name details differ."],
 ["Messages", "Direct messages, inbox, threads, read status", "Achieved; model uses content/sentdate naming."],
 ["Profile", "Avatar, username, email updates", "Achieved."],
 ["Settings", "Password change only; no UserSettings table", "Theme/email notifications via UserSettings are planned."],
 ["Visibility", "Post.is_public; private view blocked for guests", "Mostly achieved. Subforum listings should also be reviewed to ensure private titles/content are not exposed."],
 ["Rich content", "Plain text content; media/markdown fields absent", "Post format and media_url planned."],
 ["UI", "Shared layout, logo, footer, Bootstrap/custom CSS", "Largely achieved."],
], [1.05*inch, 2.7*inch, 2.75*inch], tiny=True)
H2("Important files and their jobs")
table([
 ["File/folder", "Job"],
 ["forum/app.py", "Runtime entry point, login manager, home page, seed data"],
 ["forum/__init__.py", "Application factory and blueprint/SQLAlchemy registration"],
 ["config.py", "MySQL URL and Flask configuration"],
 ["forum/models.py", "Database models and content validators/helpers"],
 ["forum/user.py", "Account and avatar validators/checks"],
 ["forum/*.py feature modules", "Controllers grouped by feature"],
 ["forum/templates/", "Jinja presentation files"],
 ["forum/static/", "CSS, Bootstrap, logo, uploaded avatars"],
 ["compose.yaml / Dockerfile", "Container startup and web/database wiring"],
], [2.2*inch, 4.3*inch])
story.append(PageBreak())

H1("12. Comprehension check")
P("Try these without looking back. Then use the answer key on the next page.")
questions = [
 "1. What line causes the Flask application factory to execute?",
 "2. Name all seven registered blueprints.",
 "3. What is the difference between a foreign key and a relationship?",
 "4. Which route creates a reaction, and what three reaction values are accepted?",
 "5. Why does Message need two foreign keys to User?",
 "6. What makes a database change persistent?",
 "7. Where do avatar bytes live, and what does the User table store?",
 "8. Which file supplies shared page layout and which file supplies custom styling?",
 "9. Explain the complete request path for sending a direct message.",
 "10. Which target-UML model does not exist in the current code?",
 "11. Is this project primarily a strict REST API? Why or why not?",
 "12. What does Docker's named MySQL volume protect against?",
 "13. What does <font name='Courier'>@login_required</font> do?",
 "14. Which current signup validation rule is commented out?",
 "15. Explain <font name='Courier'>http://localhost:5000</font> word by word.",
]
for q in questions: P(q)
P("Notes:")
for _ in range(9):
    story.append(HRFlowable(width="100%", thickness=.35, color=LINE, spaceBefore=8, spaceAfter=5))
story.append(PageBreak())

H1("Answer key")
answers = [
 ("1", "<font name='Courier'>app = create_app()</font> in <font name='Courier'>forum/app.py</font>."),
 ("2", "posts, comments, reactions, messages, settings, profile, and routes."),
 ("3", "A foreign key is the stored ID that enforces a database link. A relationship gives convenient Python navigation between linked objects."),
 ("4", "<font name='Courier'>POST /action_reaction</font>; like, dislike, and heart."),
 ("5", "Each message has two User roles: sender and recipient."),
 ("6", "A successful <font name='Courier'>db.session.commit()</font> completes the transaction."),
 ("7", "Bytes live in <font name='Courier'>forum/static/images/avatars/</font>; User stores only <font name='Courier'>avatar_filename</font>."),
 ("8", "<font name='Courier'>forum/templates/layout.html</font> and <font name='Courier'>forum/static/style.css</font>."),
 ("9", "Form POST → matching route/login check → recipient/content validation → create and link Message → add/commit → redirect → conversation GET/query/render."),
 ("10", "UserSettings."),
 ("11", "No. It is mainly a server-rendered HTML app with action-style form endpoints and redirects, not a resource-oriented JSON API."),
 ("12", "It keeps MySQL data when the database container itself is replaced or recreated."),
 ("13", "It requires an authenticated Flask-Login user or redirects to the configured login view."),
 ("14", "The password-format check in account creation."),
 ("15", "http = protocol; localhost = this computer; 5000 = the network port; / = the root path."),
]
for n, a in answers: P(f"<b>{n}.</b> {a}")
H2("Teach-back prompts")
bullet("Draw the request-response sequence from memory and label where authentication, validation, database work, and rendering occur.")
bullet("Pick one blueprint and explain its routes, input, business rules, models, and output.")
bullet("Explain one current-vs-target mismatch without looking at the guide.")
bullet("Describe how one user can own posts, comments, reactions, sent messages, and received messages.")
story.append(PageBreak())

H1("Source notes and accuracy boundaries")
P("This guide was built from the live repository files, the supplied comprehension-questions PDF, the supplied updated target-architecture image, and recent project history for the direct-message and profile feature commits.")
H2("Primary project evidence")
for item in [
 "Startup/configuration: <font name='Courier'>forum/app.py</font>, <font name='Courier'>forum/__init__.py</font>, <font name='Courier'>config.py</font>, <font name='Courier'>Dockerfile</font>, <font name='Courier'>compose.yaml</font>, <font name='Courier'>requirements.txt</font>.",
 "Routing/business logic: <font name='Courier'>forum/routes.py</font>, <font name='Courier'>posts.py</font>, <font name='Courier'>comments.py</font>, <font name='Courier'>reactions.py</font>, <font name='Courier'>messages.py</font>, <font name='Courier'>settings.py</font>, and <font name='Courier'>profile.py</font>.",
 "Models/helpers: <font name='Courier'>forum/models.py</font> and <font name='Courier'>forum/user.py</font>.",
 "Presentation: <font name='Courier'>forum/templates/</font> and <font name='Courier'>forum/static/</font>.",
 "Feature history: commits <font name='Courier'>750b831</font> (direct messages), <font name='Courier'>762aaf1</font> (settings), and <font name='Courier'>1db9ff1</font> (profile).",
]: bullet(item)
callout("BOUNDARY", "“Current” means visible in this repository snapshot, not necessarily fully tested in a running environment. “Target” means shown or implied in the updated architecture diagram/README feature list. Where names or behavior disagree, the current code is described first.", GOLD)
H2("Five facts worth memorizing")
for fact in [
 "The app factory is <font name='Courier'>create_app()</font> in <font name='Courier'>forum/__init__.py</font>.",
 "Routes are controllers grouped into seven blueprints, plus the root route in <font name='Courier'>app.py</font>.",
 "Six current SQLAlchemy models live in <font name='Courier'>models.py</font>; UserSettings is planned only.",
 "MySQL persistence happens through SQLAlchemy commits and the Docker named volume.",
 "A request usually ends by rendering a Jinja template or redirecting the browser to another GET.",
]: bullet(fact)

def footer(canvas, doc):
    canvas.saveState()
    w, h = letter
    canvas.setStrokeColor(LINE); canvas.setLineWidth(.4)
    canvas.line(0.72*inch, 0.55*inch, w-0.72*inch, 0.55*inch)
    canvas.setFont("Helvetica", 8); canvas.setFillColor(GRAY)
    canvas.drawString(0.72*inch, 0.35*inch, "CircusCircusLimes Project Study Guide")
    canvas.drawRightString(w-0.72*inch, 0.35*inch, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(str(OUT), pagesize=letter, rightMargin=.72*inch, leftMargin=.72*inch,
                        topMargin=.68*inch, bottomMargin=.7*inch,
                        title="CircusCircusLimes Project Study Guide",
                        author="Prepared for the CircusCircusLimes project")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
