"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_repr_method(self):
        user = User(username='john_doe', email='john@example.com', password='test123')
        self.assertEqual(str(user), "<User #1: john_doe, john@example.com>")

    def test_is_following(self):
        user1 = User(username='user1', email='user1@example.com', password='test123')
        user2 = User(username='user2', email='user2@example.com', password='test456')
        db.session.add_all([user1, user2])
        db.session.commit()

        # Test when user 1 is following user 2
        user1.following.append(user2)
        db.session.commit()
        self.assertTrue(user1.is_following(user2))

        # Test when user1 is not following user2
        self.assertFalse(user2.is_following(user1))

    def test_is_followed_by(self):
        user1 = User(username='user1', email='user1@example.com', password='test123')
        user2 = User(username='user2', email='user2@example.com', password='test456')
        db.session.add_all([user1, user2])
        db.session.commit()

        # Test when user1 is followed by user2
        user1.followers.append(user2)
        db.session.commit()
        self.assertTrue(user1.is_followed_by(user2))

        # Test when user2 is followed by user1
        self.assertTrue(user2.is_followed_by(user1))

    def test_user_create(self):
        user= User(username='user', email='user@example.com', password='test123')


