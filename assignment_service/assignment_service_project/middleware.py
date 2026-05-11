import sqlite3
from django.conf import settings


class MicroserviceAuthMiddleware:
    """
    Identifies the logged-in user for non-auth services.
    With shared SECRET_KEY + shared DB, Django's SessionMiddleware can decode
    the session created by auth_service. We then read _auth_user_id from the
    session and look up the user directly in the accounts_user table.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Check for explicit headers (gateway / proxy case)
        user_id = request.headers.get('X-User-Id')
        role = request.headers.get('X-User-Role')
        username = request.headers.get('X-User-Name')

        # 2. Fallback: read from Django session (shared DB + shared SECRET_KEY)
        if not user_id and hasattr(request, 'session'):
            auth_user_id = request.session.get('_auth_user_id')
            if auth_user_id:
                user_id, role, username = self._lookup_user(auth_user_id)

        if user_id:
            request.user = _MockUser(int(user_id), role, username)

        return self.get_response(request)

    # ------------------------------------------------------------------
    @staticmethod
    def _lookup_user(user_id):
        db_path = settings.DATABASES['default']['NAME']
        try:
            conn = sqlite3.connect(str(db_path))
            cur = conn.cursor()
            cur.execute(
                "SELECT id, role, username FROM accounts_user WHERE id = ?",
                (user_id,),
            )
            row = cur.fetchone()
            conn.close()
            if row:
                return row[0], row[1], row[2]
        except Exception:
            pass
        return None, None, None


class _MockUser:
    """Lightweight stand-in for the real User model."""

    def __init__(self, id, role, username):
        self.id = id
        self.pk = id
        self.role = role
        self.username = username
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def __str__(self):
        return self.username or ''
