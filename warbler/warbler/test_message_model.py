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


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()
    
    def test_create_and_retrieve_message(self):
        user = User(username='john_doe', email='john@example.com', password='test123')
        db.session.add(user)
        db.session.commit()

        # Create a new message
        message_text = 'Test message'
        message = Message(text=message_text, user=user)
        db.session.add(message)
        db.session.commit()

        # Retrieve the message from the database
        retrieved_message = Message.query.filter_by(text=message_text).first()

        # Test if the retrieved message matches the created message
        self.assertEqual(message, retrieved_message)
        self.assertEqual(message.text, retrieved_message.text)
        self.assertEqual(message.timestamp, retrieved_message.timestamp)
        self.assertEqual(message.user, retrieved_message.user)
    
    def test_repr_method(self):
        user = User(username='john_doe', email='john@example.com', password='test123')
        db.session.add(user)
        db.session.commit()
        message = Message(text='Test message', user=user)
        db.session.add(message)
        db.session.commit()
        self.assertEqual(str(message), "<Message #1: Test message, by john_doe>")

    def test_message_timestamp(self):
        user = User(username='john_doe', email='john@example.com', password='test123')
        db.session.add(user)
        db.session.commit()
        message1 = Message(text='Test message 1', user=user)
        db.session.add(message1)
        db.session.commit()
        message2 = Message(text='Test message 2', user=user)
        db.session.add(message2)
        db.session.commit()

        self.assertTrue(message1.timestamp < message2.timestamp)
