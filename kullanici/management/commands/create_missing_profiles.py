from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from kullanici.models import UserProfile

class Command(BaseCommand):
    help = 'Eksik kullanıcı profillerini oluşturur'

    def handle(self, *args, **options):
        # Profili olmayan kullanıcıları bul
        users_without_profile = User.objects.filter(profile__isnull=True)
        
        if not users_without_profile.exists():
            self.stdout.write(self.style.SUCCESS('Tüm kullanıcıların profili mevcut.'))
            return
        
        # Eksik profilleri oluştur
        created_count = 0
        for user in users_without_profile:
            UserProfile.objects.create(user=user)
            created_count += 1
            self.stdout.write(f'Kullanıcı için profil oluşturuldu: {user.username}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Toplam {created_count} eksik profil oluşturuldu.')
        ) 