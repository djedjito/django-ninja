from ninja import NinjaAPI
from ninja.security import HttpBearer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from users.models import UserPermission
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from typing import List, Dict
from users.models import Profile, MenuItem



api = NinjaAPI()

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            access_token = AccessToken(token)
            user = get_user_model().objects.get(id=access_token['user_id'])
            return user
        except:
            return None
@api.post("/login")
def get_token(request, email: str, password: str):
    User = get_user_model()
    user = get_object_or_404(User, email=email)
    
    if not check_password(password, user.password):
        raise HttpError(401, "Senha incorrecta")
    
    refresh = RefreshToken.for_user(user)
    
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }
    
@api.post('/register', auth=None)
def register (request, email: str, full_name: str, password: str):
    User = get_user_model()
    if User.objects.filter(email=email).exists:
        raise HttpError(408, "Email já está em uso.")
    
    user = User.objects.create_user(
        email=email,
        full_name=full_name,
        password=password
    )
    
    refresh = RefreshToken.for_user(user)
    
    
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
        }
    }
    
@api.get('/user', auth=AuthBearer())
def list_users(request):
    User = get_user_model()
    users = User.objects.all()
    return[
        {
            'id':u.id,
            'email': u.email,
            'full_name': u.full_name
        } for u in users
    ]

@api.get("/users/{user_id}", auth=AuthBearer())
def get_user (request, user_id:int):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    return {'id': user.id, 'email':user.email, 'full_name': user.full_name, }

@api.put("/users/{user_id}", auth=AuthBearer())
def updat_user (request, user_id: int, full_name: str = None, password: str = None):
    User = get_user_model()
    user = get_object_or_404(User, id = user_id)
    
    if full_name:
        user.full_name = full_name
    if password:
        user.password = make_password(password)
        
    user.gave()
    return {"success": True}

@api.delete("/users/{user_id}", auth=AuthBearer())
def delete_user(request, user_id:int):
    User = get_user_model()
    user = get_object_or_404(User, id = user_id)
    user.delete()
    return{"success": True}


@api.post('/permissions', auth=AuthBearer())
def create_permission(request, name: str, codename: str, description: str = ''):
    permission = UserPermission.objects.create(
        name = name,
        codename = codename,
        description = description
    )
    return {'id': permission.id, "name": permission.name}

@api.get("/permissions", auth=AuthBearer())
def list_permissions(request):
    permissions = UserPermission.objects.all()
    return [{'id': p.id, 'name': p.name, 'codename': p.codename} for p in permissions]
@api.post('/users/{user_id}/permissions/{permission_id}', auth=AuthBearer())
def assign_permission(request, user_id: int, permission_id: int):
    # Verifica se o usuário que está fazendo a requisição é admin
    if not request.user.is_admin:
        raise HttpError(403, "Apenas administradores podem atribuir permissões")
    
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    permission = get_object_or_404(UserPermission, id=permission_id)
    
    # Verifica restrições baseadas no perfil atual
    if user.is_admin and permission.codename.startswith('guest_'):
        raise HttpError(400, "Não pode atribuir permissões de guest a um admin")
    
    # Adiciona a permissão ao usuário
    user.user_permissions.add(permission)
    
    return {
        'success': True,
        'message': f'Permissão {permission.name} atribuída com sucesso',
        'user': user.email,
        'current_profile': user.profile.name
    }

@api.get('/profile/menu', response=List[Dict])
def get_user_menu(request):
    """A ideia é de retornar menu de acordo com perfil do utilizador"""
    if not request.user.is_authenticated:
        raise HttpError(401, 'Não autenticado')
    
    menu_items = MenuItem.objects.filter(profiles=request.user.profile).order_by('order')
    return [
        {
            'name': item.name,
            'url':item.url,
            'icon': item.icon,
            'order': item.order
        }
        for item in menu_items
    ]
    
@api.get("/profiles", response=List[Dict])
def list_profiles (request):
    """ Lista de todos os perfis disponiveís"""
    profiles = Profile.objects.all()
    return [
        {
            'name': profile.name,
            'description': profile.description
        }
        for profile in profiles
    ]
@api.post("/users/{user_id}/change-profile")
def change_user_profile(request, user_id: int, new_profile: str):
    """ A ideia desta função é de alterar o perfil de um utilizador """
    
    if not request.user.is_admin:
        raise HttpError(403, "Apenas administradores podem alterar os perfís")
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    
    try:
        new_profile_obj = Profile.objects.get(name = new_profile)
    except Profile.DoesNotExist:
        raise HttpError(400, "Perfil inválido")
    
    if user.is_anfitriao and new_profile == "guest":
        pass
    elif user.is_guest and new_profile == 'anfitriao':
        pass
    elif new_profile == 'admin':
        raise HttpError(403, "Apenas adminstradores podem criar outros administradores")
    
    user.profile = new_profile_obj
    user.save()
    
    return {'sucess': True, 'new_profile': new_profile}

@api.get('/users/profile', response=Dict)
def get_current_user_profile (request):
    """Retorna o perfil do actual utilizador """
    if not request.user.is_authenticated:
        raise HttpError(401, "Não autenticado")
    
    return {
        'profile': request.user.profile.name,
        'is_admin': request.user.is_admin,
        'is_anfitriao': request.user.is_anfitriao,
        'is_guest': request.user.is_guest
    }

@api.post('/request-anfitriao')
def request_anfitriao(request):
    """ Permite que um guest solicite tornar-se anfitrião"""
    if not request.user.is_authenticated:
        raise HttpError(401, 'Não autenicado')
   
    anfitriao_profile = Profile.objects.get(name = 'anfitriao')
    request.user.profile = anfitriao_profile
    request.user.save()
    return {
        "success": True,
        "message": "Agora você é um anfitrião!"
    }
   
    
    
    
    