# LITREVIEW

Minimal Goodreads-style app to review books and follow other users.

## Project structure

Apps:
- `reviews`: Book and Review models, views, and templates
- `users`: Custom User model, authentication, profile, and follow system

Key pages:
- Home feed (recent/following)
- Search (users and books)
- Book detail and review CRUD
- User profiles with follow/unfollow and reviews list

## Quickstart (macOS, zsh)

1) Create and activate a virtualenv
- python3 -m venv .venv
- source .venv/bin/activate

2) Install dependencies
- pip install -r requirements.txt

3) Configure environment (optional)
- Copy .env.example to .env and adjust if present; by default SQLite is used.

4) Initialize database
- python manage.py migrate
- python manage.py createsuperuser  # follow prompts

5) Run the server
- python manage.py runserver

6) Open the app
- http://127.0.0.1:8000/

## Using the app

- Sign up or log in with your superuser.
- Use the search bar to find users or books by title.
- Create a book if it does not exist, then write a review (rating + text).
- Follow users to see their reviews in your Following feed.

## Media and static files

- Book covers are uploaded to the local filesystem during development.
- The code guards against missing images and shows placeholders.
- Do not commit media files to Git. The `.gitignore` excludes images and SQLite DB by default.

## Development notes

- Code style: PEP8; views have lightweight docstrings. Run tools like flake8/black if you prefer.
- Query performance: feeds and detail pages use select_related to avoid N+1 queries.
- Deletion UX: review deletions use a confirm() dialog with POST; a server-side fallback page exists for noscript.
- SVG icons are inline for search/home/back; no FontAwesome dependency for icons.

## Common tasks

- Load example data (optional): python manage.py loaddata database.json
- Create a test user quickly:
	- python manage.py shell
	- from users.models import User; User.objects.create_user('demo', password='demo')

Note: The provided `database.json` fixture is sanitized to include ONLY users, books, and reviews (no admin logs, permissions, sessions, or media filenames). Fixture user passwords are placeholder values and not valid for login. After loading, set a password via the admin or shell, e.g. (Django shell): `u = User.objects.get(username='jasohal2'); u.set_password('demo'); u.save()`.

## Cleaning up tracked artifacts

If `db.sqlite3` or image files were committed before `.gitignore` rules were added, untrack them without deleting local copies:
- git rm -r --cached db.sqlite3 media/ *.jpg *.jpeg
- git commit -m "chore: stop tracking sqlite and media files"

## Requirements

See `requirements.txt`. Tested with:
- Django 4.0.x
- Pillow 9.x

## Troubleshooting

- If you see template errors about image `.url`, ensure you pulled latest templates with image guards.
- If styles look off, clear your browser cache or check for stray CSS braces.

## License

For educational use as part of OpenClassrooms project work.