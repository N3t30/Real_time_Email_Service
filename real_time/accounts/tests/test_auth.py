from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import CustomUser

class AuthTests(APITestCase):
    def setUp(self):
        # Defina dados padrão para os testes
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123"
        }

    def test_register_user(self):
        # Testa o registro de um novo usuário
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)  # Verifica se o usuário foi criado no banco de dados
        self.assertEqual(CustomUser.objects.get().username, self.user_data["username"])

    def test_register_user_missing_fields(self):
        # Testa o registro com campos ausentes
        incomplete_data = {
            "username": "incompleteuser",
            "password": "incompletepass"
        }
        response = self.client.post(self.register_url, incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_login_user(self):
        # Primeiro, crie o usuário
        self.client.post(self.register_url, self.user_data, format='json')
        # Em seguida, tente fazer o login com os dados corretos
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)  # Verifica se o token de acesso foi retornado

    def test_login_invalid_credentials(self):
        # Testa login com credenciais inválidas
        invalid_login_data = {
            "username": "invaliduser",
            "password": "wrongpass"
        }
        response = self.client.post(self.login_url, invalid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
