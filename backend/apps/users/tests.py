import logging
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from .views import UserViewSet

logger = logging.Logger(__name__)


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="normaluser@example.com", password="password"
        )
        self.assertEqual(user.email, "normaluser@example.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(AttributeError):
            user.username
        with self.assertRaises(ValueError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="password")

    def test_create_superuser(self):
        User = get_user_model()
        superuser = User.objects.create_superuser(
            email="superuser@example.com", password="password"
        )
        self.assertEqual(superuser.email, "superuser@example.com")
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

        with self.assertRaises(AttributeError):
            superuser.username
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="superuser@example.com", password="password", is_superuser=False
            )


class UserViewSetListTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(
            email="test_user@focave.com", password="User123@"
        )
        self.superuser = get_user_model().objects.create_superuser(
            email="test_superuser@focave.com", password="Admin123@"
        )
        self.view = UserViewSet.as_view({"get": "list"})
        self.request = self.factory.get("/users/")

    def test_unauthenticated_user(self):
        response = self.view(self.request)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.UNAUTHORIZED)

    def test_user(self):
        force_authenticate(self.request, user=self.user)
        response = self.view(self.request)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.FORBIDDEN)

    def test_superuser(self):
        force_authenticate(self.request, user=self.superuser)
        response = self.view(self.request)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.OK)


class UserViewSetCreateTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(
            email="test_user@focave.com", password="User123@"
        )
        self.superuser = get_user_model().objects.create_superuser(
            email="test_superuser@focave.com", password="Admin123@"
        )
        self.view = UserViewSet.as_view({"post": "create"})
        self.request = self.factory.post(
            "/users/", {"email": "test_create@focave.com", "password": "User123@"}
        )

    def test_unauthenticated_user(self):
        response = self.view(self.request)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.CREATED)
        self.assertTrue(
            get_user_model().objects.filter(email="test_create@focave.com").exists()
        )

    def test_user(self):
        force_authenticate(self.request, user=self.user)
        response = self.view(self.request)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.CREATED)
        self.assertTrue(
            get_user_model().objects.filter(email="test_create@focave.com").exists()
        )

    def test_superuser(self):
        force_authenticate(self.request, user=self.superuser)
        response = self.view(self.request)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.CREATED)
        self.assertTrue(
            get_user_model().objects.filter(email="test_create@focave.com").exists()
        )

    def test_no_password(self):
        request = self.factory.post("/users/", {"email": "test_create@focave.com"})
        response = self.view(request)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.BAD_REQUEST)
        self.assertFalse(
            get_user_model().objects.filter(email="test_create@focave.com").exists()
        )

    def test_bad_email(self):
        request = self.factory.post(
            "/users/", {"email": "test_create@focave", "password": "User123@"}
        )
        response = self.view(request)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.BAD_REQUEST)
        self.assertFalse(
            get_user_model().objects.filter(email="test_create@focave").exists()
        )


class UserViewSetUpdateTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.diffrent_user = get_user_model().objects.create_user(
            email="test_user@focave.com", password="User123@"
        )
        self.superuser = get_user_model().objects.create_superuser(
            email="test_superuser@focave.com", password="Admin123@"
        )
        self.view = UserViewSet.as_view({"put": "update"})
        self.user = get_user_model().objects.create_user(
            email="test_update@focave.com", password="User123@"
        )
        self.request = self.factory.put(
            "/users/", {"email": "test_update2@focave.com", "password": "User123@2"}
        )

    def test_unauthenticated_user(self):
        response = self.view(self.request, pk=self.user.id)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.UNAUTHORIZED)
        self.assertFalse(
            get_user_model().objects.filter(email="test_update2@focave.com").exists()
        )

    def test_diffrent_user(self):
        force_authenticate(self.request, self.diffrent_user)
        response = self.view(self.request, pk=self.user.id)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.NOT_FOUND)
        self.assertFalse(
            get_user_model().objects.filter(email="test_update2@focave.com").exists()
        )

    def test_owner(self):
        force_authenticate(self.request, self.user)
        response = self.view(self.request, pk=self.user.id)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.OK)
        self.assertEqual(response.data["email"], "test_update2@focave.com")
        self.assertTrue(
            get_user_model().objects.filter(email="test_update2@focave.com").exists()
        )

    def test_superuser(self):
        force_authenticate(self.request, self.superuser)
        response = self.view(self.request, pk=self.user.id)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.OK)
        self.assertEqual(response.data["email"], "test_update2@focave.com")
        self.assertTrue(
            get_user_model().objects.filter(email="test_update2@focave.com").exists()
        )

    def test_no_password(self):
        request = self.factory.put("/users/", {"email": "test_update2@focave.com"})
        force_authenticate(request, self.superuser)
        response = self.view(request, pk=self.user.id)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.BAD_REQUEST)
        self.assertFalse(
            get_user_model().objects.filter(email="test_update2@focave.com").exists()
        )

    def test_bad_email(self):
        request = self.factory.put(
            "/users/", {"email": "test_update2@focave", "password": "User123@"}
        )
        force_authenticate(request, self.superuser)
        response = self.view(request, pk=self.user.id)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.BAD_REQUEST)
        self.assertFalse(
            get_user_model().objects.filter(email="test_update2@focave").exists()
        )


class UserViewSetPartialUpdateTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.diffrent_user = get_user_model().objects.create_user(
            email="test_user@focave.com", password="User123@"
        )
        self.superuser = get_user_model().objects.create_superuser(
            email="test_superuser@focave.com", password="Admin123@"
        )
        self.view = UserViewSet.as_view({"patch": "partial_update"})
        self.user = get_user_model().objects.create_user(
            email="test_partial_update@focave.com", password="User123@"
        )
        self.request = self.factory.patch(
            "/users/",
            {"email": "test_partial_update2@focave.com"},
        )

    def test_unauthenticated_user(self):
        response = self.view(self.request, pk=self.user.id)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.UNAUTHORIZED)
        self.assertFalse(
            get_user_model()
            .objects.filter(email="test_partial_update2@focave.com")
            .exists()
        )

    def test_diffrent_user(self):
        force_authenticate(self.request, self.diffrent_user)
        response = self.view(self.request, pk=self.user.id)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.NOT_FOUND)
        self.assertFalse(
            get_user_model()
            .objects.filter(email="test_partial_update2@focave.com")
            .exists()
        )

    def test_owner(self):
        force_authenticate(self.request, self.user)
        response = self.view(self.request, pk=self.user.id)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.OK)
        self.assertEqual(response.data["email"], "test_partial_update2@focave.com")
        self.assertTrue(
            get_user_model()
            .objects.filter(email="test_partial_update2@focave.com")
            .exists()
        )

    def test_superuser(self):
        force_authenticate(self.request, self.superuser)
        response = self.view(self.request, pk=self.user.id)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.OK)
        self.assertEqual(response.data["email"], "test_partial_update2@focave.com")
        self.assertTrue(
            get_user_model()
            .objects.filter(email="test_partial_update2@focave.com")
            .exists()
        )

    def test_no_password(self):
        request = self.factory.patch(
            "/users/", {"email": "test_partial_update2@focave.com"}
        )
        force_authenticate(request, self.superuser)
        response = self.view(request, pk=self.user.id)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.OK)
        self.assertTrue(
            get_user_model()
            .objects.filter(email="test_partial_update2@focave.com")
            .exists()
        )

    def test_bad_email(self):
        request = self.factory.patch(
            "/users/", {"email": "test_partial_update2@focave", "password": "User123@"}
        )
        force_authenticate(request, self.superuser)
        response = self.view(request, pk=self.user.id)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.BAD_REQUEST)
        self.assertFalse(
            get_user_model()
            .objects.filter(email="test_partial_update2@focave")
            .exists()
        )


class UserViewSetDestroyTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.diffrent_user = get_user_model().objects.create_user(
            email="test_user@focave.com", password="User123@"
        )
        self.superuser = get_user_model().objects.create_superuser(
            email="test_superuser@focave.com", password="Admin123@"
        )
        self.view = UserViewSet.as_view({"delete": "destroy"})
        self.user = get_user_model().objects.create_user(
            email="test_destroy@focave.com", password="User123@"
        )
        self.request = self.factory.delete("/users/")

    def test_unauthenticated_user(self):
        response = self.view(self.request, pk=self.user.id)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.UNAUTHORIZED)
        self.assertTrue(
            get_user_model().objects.filter(email="test_destroy@focave.com").exists()
        )

    def test_diffrent_user(self):
        force_authenticate(self.request, self.diffrent_user)
        response = self.view(self.request, pk=self.user.id)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.NOT_FOUND)
        self.assertTrue(
            get_user_model().objects.filter(email="test_destroy@focave.com").exists()
        )

    def test_owner(self):
        force_authenticate(self.request, self.user)
        response = self.view(self.request, pk=self.user.id)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.NO_CONTENT)
        self.assertFalse(
            get_user_model().objects.filter(email="test_destroy@focave.com").exists()
        )

    def test_superuser(self):
        force_authenticate(self.request, self.superuser)
        response = self.view(self.request, pk=self.user.id)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.NO_CONTENT)
        self.assertFalse(
            get_user_model().objects.filter(email="test_destroy@focave.com").exists()
        )


class UserViewSetRetrieveTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.diffrent_user = get_user_model().objects.create_user(
            email="test_user@focave.com", password="User123@"
        )
        self.superuser = get_user_model().objects.create_superuser(
            email="test_superuser@focave.com", password="Admin123@"
        )
        self.view = UserViewSet.as_view({"get": "retrieve"})
        self.user = get_user_model().objects.create_user(
            email="test_retrieve@focave.com", password="User123@"
        )
        self.request = self.factory.get("/users/")

    def test_unauthenticated_user(self):
        response = self.view(self.request, pk=self.user.id)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.UNAUTHORIZED)

    def test_diffrent_user(self):
        force_authenticate(self.request, self.diffrent_user)
        response = self.view(self.request, pk=self.user.id)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.NOT_FOUND)

    def test_owner(self):
        force_authenticate(self.request, self.user)
        response = self.view(self.request, pk=self.user.id)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_superuser(self):
        force_authenticate(self.request, self.superuser)
        response = self.view(self.request, pk=self.user.id)
        self.assertEqual(HTTPStatus(response.status_code), HTTPStatus.OK)
        self.assertEqual(response.data["email"], self.user.email)
