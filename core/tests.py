from django.contrib.auth import get_user_model
from django.test import TestCase

from core.builder import Builder

User = get_user_model()


class BuilderSetupTestCase(TestCase):
    def setUp(self) -> None:
        self.builder = Builder()

    def test_user_wo_faker(self):
        user = self.builder.user(faker=False)
        self.assertEqual(user.first_name, "FirstName0")
        self.assertEqual(user.last_name, "LastName0")
        self.assertEqual(user.email, "user0@leavingwell.test")

    def test_user_with_faker(self):
        user = self.builder.user()
        self.assertEqual(user.first_name, "Jacob")
        self.assertEqual(user.last_name, "Nicholls")
        self.assertEqual(user.email, "dianaleach@example.com")

    def test_user_with_params(self):
        user = self.builder.user(first_name="John")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Nicholls")
        self.assertEqual(user.email, "dianaleach@example.com")

    def test_young_person(self):
        yp = self.builder.young_person()
        self.assertEqual(yp.user.first_name, "Jacob")
        self.assertEqual(yp.user.last_name, "Nicholls")
        self.assertEqual(yp.user.email, "dianaleach@example.com")

    def test_personal_advisor(self):
        pa = self.builder.personal_advisor()
        self.assertEqual(pa.user.first_name, "Jacob")
        self.assertEqual(pa.user.last_name, "Nicholls")
        self.assertEqual(pa.user.email, "dianaleach@example.com")

    def test_manager(self):
        pa = self.builder.personal_advisor()
        self.assertEqual(pa.user.first_name, "Jacob")
        self.assertEqual(pa.user.last_name, "Nicholls")
        self.assertEqual(pa.user.email, "dianaleach@example.com")

    def test_all_users(self):
        yp = self.builder.young_person(
            user__faker=False,
            pa=True,
            pa__user__faker=False,
            pa__manager=True,
            pa__manager__user__faker=False,
        )

        self.assertEqual(User.objects.count(), 3)

        self.assertIsNotNone(yp)
        self.assertEqual(yp.user.first_name, "FirstName0")

        pa = yp.personal_advisors.first()
        self.assertEqual(pa.user.first_name, "FirstName1")

        manager = pa.manager
        self.assertEqual(manager.user.first_name, "FirstName2")
