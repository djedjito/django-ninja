# tests/test_users_api.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import CustomUser, Profile, UserPermission

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_profiles():
    Profile.objects.get_or_create(name='guest', defaults={'description': 'Guest'})
    Profile.objects.get_or_create(name='anfitriao', defaults={'description': 'Host'})
    Profile.objects.get_or_create(name='admin', defaults={'description': 'Admin'})

@pytest.mark.django_db
def test_register_user(api_client, create_profiles):
    url = '/api/register'
    data = {
        'email': 'user@example.com',
        'full_name': 'User Example',
        'password': 'password123'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 200
    assert 'access' in response.data
    assert CustomUser.objects.filter(email='user@example.com').exists()

@pytest.mark.django_db
def test_login_user(api_client, create_profiles):
    user = CustomUser.objects.create_user(email='login@test.com', full_name='Login Test', password='test1234')
    url = '/api/login'
    data = {'email': 'login@test.com', 'password': 'test1234'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == 200
    assert 'access' in response.data

@pytest.mark.django_db
def test_get_profile_menu(api_client, create_profiles):
    user = CustomUser.objects.create_user(email='menu@test.com', full_name='Menu Test', password='test1234')
    token = APIClient().post('/api/login', {'email': user.email, 'password': 'test1234'}, format='json').data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = api_client.get('/api/profile/menu')
    assert response.status_code == 200
    assert isinstance(response.data, list)

@pytest.mark.django_db
def test_change_user_profile(api_client, create_profiles):
    admin_profile = Profile.objects.get(name='admin')
    admin = CustomUser.objects.create_user(email='admin@test.com', full_name='Admin', password='admin123', profile=admin_profile)
    user = CustomUser.objects.create_user(email='target@test.com', full_name='Target User', password='123456')
    token = APIClient().post('/api/login', {'email': admin.email, 'password': 'admin123'}, format='json').data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = api_client.post(f'/api/users/{user.id}/change-profile?new_profile=anfitriao')
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.profile.name == 'anfitriao'

@pytest.mark.django_db
def test_assign_permission(api_client, create_profiles):
    admin_profile = Profile.objects.get(name='admin')
    admin = CustomUser.objects.create_user(email='admin2@test.com', full_name='Admin 2', password='admin123', profile=admin_profile)
    target = CustomUser.objects.create_user(email='perm@test.com', full_name='Perm User', password='123456')
    permission = UserPermission.objects.create(name='Test Perm', codename='test_perm')
    token = APIClient().post('/api/login', {'email': admin.email, 'password': 'admin123'}, format='json').data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = api_client.post(f'/api/users/{target.id}/permissions/{permission.id}')
    assert response.status_code == 200

# docs.py
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI(title="User Auth API", description="API de Autenticação e Gestão de Usuários", version="1.0.0")

# No arquivo `urls.py`, adicione:
# from .docs import api as extra_api
# path("api/docs/", extra_api.get_openapi_view()),

# Certifique-se de instalar:
# pip install ninja-extra

# pytest.ini
# Crie um arquivo `pytest.ini` na raiz do projeto



