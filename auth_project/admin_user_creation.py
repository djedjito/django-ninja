from users.models import Profile

Profile.objects.get_or_create(name='admin', defaults={'description': 'Administrador'})
Profile.objects.get_or_create(name='anfitriao', defaults={'description': 'Anfitrião'})
Profile.objects.get_or_create(name='guest', defaults={'description': 'Convidado'})
