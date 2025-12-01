import pytest
from app import app, db, bcrypt
from models import User


@pytest.fixture
def client():
    # Configure app for testing
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)
            db.create_all()
            # Create a test user
            u = User(
                username='tester',
                email='t@t.com',
                password_hash=bcrypt.generate_password_hash('Password123').decode()
            )
            db.session.add(u)
            db.session.commit()
        yield client  # test runs here
        # Cleanup
        with app.app_context():
            db.drop_all()


def test_login_success(client):
    """Test successful login with valid credentials"""
    rv = client.post(
        '/login',
        data={'username': 'tester', 'password': 'Password123'},
        follow_redirects=True
    )
    assert b'Welcome' in rv.data
