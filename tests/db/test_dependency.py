from sqlalchemy.orm import Session
from backend.db.dependency import get_db


def test_get_db(app):
    # Backup and clear override
    original_override = app.dependency_overrides.get(get_db)
    # Temporarily remove the override
    app.dependency_overrides.pop(get_db, None)
    from backend.db.dependency import get_db
    db = next(get_db())
    assert isinstance(db, Session)
    # Close the session
    db.close()
    # Restore the original override
    if original_override is not None:
        app.dependency_overrides[get_db] = original_override
