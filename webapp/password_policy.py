"""
Password requirements per OWASP Proactive Controls C7 (Secure Digital
Identities), Level 1 -- backed by OWASP ASVS V2.1:
  - 2.1.1 / 2.1.2: length between MIN_LENGTH and MAX_LENGTH
  - 2.1.7: reject passwords found in a known breached/common password list
  - 2.1.9: deliberately no composition rules (no forced upper/lower/digit/
    symbol mix) -- composition rules are no longer recommended, so none
    are enforced here.
"""

MIN_LENGTH = 12
MAX_LENGTH = 128


def is_valid_length(password: str) -> bool:
    return MIN_LENGTH <= len(password) <= MAX_LENGTH


def is_valid_password(password: str, conn) -> bool:
    """Authoritative check: length plus breached/common password lookup."""
    if not is_valid_length(password):
        return False
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM common_passwords WHERE password = %s", (password,))
        return cur.fetchone() is None
