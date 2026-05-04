from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='testuser', password='pass1234')
        self.assertEqual(user.username, 'testuser')
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password('pass1234'))

    def test_user_str(self):
        user = User.objects.create_user(username='alice', password='pass1234')
        self.assertEqual(str(user), 'alice')

    def test_user_bio_blank_by_default(self):
        user = User.objects.create_user(username='bob', password='pass1234')
        self.assertFalse(user.bio)
