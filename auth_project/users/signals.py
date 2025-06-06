from django.db.models.signals import post_migrate
from django.dispatch import receiver
from users.models import Profile, MenuItem

@receiver
def  create_initial_data (sender, **kwargs):
    if sender.name == 'users':
        admin_profile, _ = Profile.objects.get_or_create (
            name = 'admin',
            defaults= {'description' : 'Administrador do sistema com todos o previlegios'}
            
        )
        
        anfitriao_profile, _ =  Profile.objects.get_or_create (
            name = "anfitriao",
            defaults= {'description': 'Anfitrião que pode gerir toda ala de propriedades'}
        )
        
        guest_profile, _ = Profile.objects.get_or_create (
            name = 'guest',
            defaults= { 'description': 'Utilizador conviadado com acesso básico'}
        )
        
        MenuItem.objects.get_or_create (
            name = "Dashboard Admin",
            url = '/admin/dashboard',
            icon = 'fa-tachometer-alt',
            order=1
        )[0].profiles.add(admin_profile)
        
        MenuItem.objects.get_or_create(
            name = 'Gestão de Utilizador',
            url = '/admin/users',
            icon = 'fa-users',
            order = 2
            
        )[0].profiles.add(admin_profile)
        
        MenuItem.objects.get_or_create(
            name = 'Gestão de Perfís',
            url = '/admin/change-profiles',
            icon = 'fa-user-cog',
            order = 3
        )
        
        MenuItem.objects.get_or_create(
            name = 'Minhas Propriedade',
            url = '/anfitriao/property',
            icon = 'fa-home',
            order = 1
        )[0].profiles.add(anfitriao_profile)
        
        MenuItem.objects.get_or_create(
            name = 'Adicionar Propriedade',
            url = '/anfitriao/add-property',
            icon = 'fa-plus-circle',
            order = 2
        )[0].profiles.add(anfitriao_profile)
        
        MenuItem.objects.get_or_create(
            name = 'Minha Conta',
            url = '/guest/account',
            icon = 'fa-user',
            order = 1
        )[0].profiles.add(guest_profile)
        
        MenuItem.objects.get_or_create(
            name = 'Tornar-se Anfitrião',
            url = '/guest/become-anfitriao',
            icon = 'fa-user-plus',
            order = 2
        )[0].profiles.add(guest_profile)