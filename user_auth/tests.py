from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user_auth.models import User


class UserApiTests(APITestCase):
    def test_register_user_uses_email_as_username_and_defaults_role(self):
        response = self.client.post(
            reverse("user-list"),
            {
                "email": "employee@example.com",
                "password": "strongpass123",
                "first_name": "Emp",
                "last_name": "Loyee",
                "role": User.Role.ADMIN,
                "phone_number": "1234567890",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="employee@example.com")
        self.assertEqual(user.role, User.Role.EMPLOYEE)
        self.assertTrue(user.check_password("strongpass123"))
        self.assertNotIn("password", response.data)

    def test_only_admin_role_can_list_users(self):
        User.objects.create_user(email="employee@example.com", password="strongpass123")
        manager = User.objects.create_user(
            email="manager@example.com",
            password="strongpass123",
            role=User.Role.MANAGER,
        )

        self.client.force_authenticate(user=manager)
        response = self.client.get(reverse("user-list"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_role_can_list_users(self):
        admin = User.objects.create_user(
            email="admin@example.com",
            password="strongpass123",
            role=User.Role.ADMIN,
        )
        User.objects.create_user(email="employee@example.com", password="strongpass123")

        self.client.force_authenticate(user=admin)
        response = self.client.get(reverse("user-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
