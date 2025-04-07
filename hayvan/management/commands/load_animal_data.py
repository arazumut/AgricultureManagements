from django.core.management.base import BaseCommand
from hayvan.models import AnimalType, AnimalBreed

class Command(BaseCommand):
    help = 'Hayvan türleri ve ırkları için örnek veriler yükler'

    def handle(self, *args, **kwargs):
        # Hayvan türleri
        animal_types = [
            ('Sığır', 'Büyükbaş hayvan türü'),
            ('Koyun', 'Küçükbaş hayvan türü'),
            ('Keçi', 'Küçükbaş hayvan türü'),
            ('Tavuk', 'Kanatlı hayvan türü'),
            ('Hindi', 'Kanatlı hayvan türü'),
        ]

        # Hayvan ırkları
        animal_breeds = {
            'Sığır': [
                ('Holstein', 'Süt verimi yüksek, siyah-beyaz renkli'),
                ('Simmental', 'Et ve süt verimi dengeli'),
                ('Angus', 'Et verimi yüksek, siyah renkli'),
                ('Jersey', 'Süt verimi yüksek, kahverengi'),
                ('Limousin', 'Et verimi yüksek, açık kahverengi'),
            ],
            'Koyun': [
                ('Merinos', 'Yün verimi yüksek'),
                ('Kıvırcık', 'Et verimi yüksek'),
                ('Akkaraman', 'Yerli ırk'),
                ('Morkaraman', 'Yerli ırk'),
                ('İvesi', 'Süt verimi yüksek'),
            ],
            'Keçi': [
                ('Saanen', 'Süt verimi yüksek, beyaz'),
                ('Alpin', 'Süt verimi yüksek'),
                ('Kıl Keçisi', 'Yerli ırk'),
                ('Tiftik Keçisi', 'Tiftik verimi yüksek'),
                ('Boer', 'Et verimi yüksek'),
            ],
            'Tavuk': [
                ('Lohman Brown', 'Yumurta verimi yüksek'),
                ('Ataks', 'Et verimi yüksek'),
                ('Hubbard', 'Et verimi yüksek'),
                ('Ross', 'Et verimi yüksek'),
                ('Beyaz Leghorn', 'Yumurta verimi yüksek'),
            ],
            'Hindi': [
                ('Bronze', 'Geleneksel hindi ırkı'),
                ('Beyaz', 'Modern hindi ırkı'),
                ('Narragansett', 'Çift amaçlı hindi ırkı'),
                ('Royal Palm', 'Süs hindi ırkı'),
                ('Bourbon Red', 'Et verimi yüksek'),
            ],
        }

        # Hayvan türlerini oluştur
        for type_name, description in animal_types:
            animal_type, created = AnimalType.objects.get_or_create(
                name=type_name,
                defaults={'description': description}
            )
            self.stdout.write(self.style.SUCCESS(f'Hayvan türü oluşturuldu: {type_name}'))

            # Her tür için ırkları oluştur
            for breed_name, characteristics in animal_breeds[type_name]:
                breed, created = AnimalBreed.objects.get_or_create(
                    animal_type=animal_type,
                    name=breed_name,
                    defaults={
                        'characteristics': characteristics,
                        'description': f'{type_name} türüne ait {breed_name} ırkı'
                    }
                )
                self.stdout.write(self.style.SUCCESS(f'Irk oluşturuldu: {type_name} - {breed_name}'))

        self.stdout.write(self.style.SUCCESS('Tüm hayvan türleri ve ırkları başarıyla yüklendi.')) 