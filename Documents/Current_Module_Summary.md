# CircusCircusLimes — Module Summary

This is a small Flask forum app ("Schooner"). Modules:

## `config.py`
Flask config class: secret key, SQLite DB URI (`circuscircus.db`), SQLAlchemy settings. Note: secret key is hardcoded (`'kristofer'`), not loaded from env despite the commented-out `load_dotenv`.

## `forum/__init__.py`
App factory (`create_app`). Builds the Flask app, loads config, registers the `comments` and `routes` blueprints, initializes SQLAlchemy, and creates tables. Comment notes more blueprints (post/subforum routes) may be split out later.

## `forum/app.py`
Entrypoint. Creates the app via `create_app()`, sets site name/description, wires up `flask_login`'s `LoginManager` with a `user_loader`, seeds default subforums (Forum, Announcements, Bug Reports, General Discussion, Other) on first run via `init_site()`/`add_subforum()`, and defines the `/` index route listing top-level subforums.

## `forum/models.py`
SQLAlchemy models and shared helpers:

- **`User`** (UserMixin): username/email/password hash, admin flag, relations to posts/comments, password hashing via werkzeug.
- **`Post`**: title/content/postdate, tied to a user and subforum, has a relative-time cache (`get_time_string`) recalculated every 30s.
- **`Subforum`**: title/description, self-referential parent/children, list of posts, `hidden` flag.
- **`Comment`**: content/postdate tied to a user and post, same relative-time caching pattern as `Post`.
- **Helpers**: `error()` (renders a red-text HTML error string — not escaped, potential XSS if fed user input), `generateLinkPath()` (builds breadcrumb HTML for a subforum chain), and `valid_title`/`valid_content` length validators.

## `forum/routes.py`
Main blueprint (`rt`) with the bulk of the app's routes: login/logout, account creation, viewing a subforum, the "add post" form, viewing a post with comments, and submitting a new post. Explicit comment in the file flags it as needing to be split into smaller route modules (`post_routes`, `subforum_routes`, etc.).

## `forum/comments.py`
`comments` blueprint with a single route, `/action_comment`, for posting a comment on a post (login required).

## `forum/user.py`
Account utility functions: username/password regex validation, and `username_taken`/`email_taken` lookups against the `User` table.

---

**Worth flagging:** the hardcoded `SECRET_KEY`, the unescaped HTML in `error()`, and the author's own TODO to split `routes.py` into per-feature blueprints.
