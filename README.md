# Tarım ve Hayvancılık Takip Sistemi

Bu proje, çiftçilerin tarım ve hayvancılık faaliyetlerini takip etmelerine yardımcı olmak amacıyla geliştirilmiş bir web uygulamasıdır. Kullanıcılar, arazi bilgilerini, ekimlerini, ürünlerini, hayvanlarını ve bunlarla ilgili tüm faaliyetleri sistem üzerinden yönetebilir ve takip edebilirler.

## Özellikler

### Hayvan Takibi
- Hayvan kayıtları oluşturma ve düzenleme
- Hayvan grupları oluşturma
- Sağlık kayıtları ve aşılama takibi
- Süt üretimi ve et üretimi takibi

### Arazi Takibi
- Arazi kayıtları oluşturma ve düzenleme
- Parsellere bölme ve parsel yönetimi
- Arazi haritaları ve koordinat bilgileri

### Üretim Takibi
- Ürün kayıtları oluşturma
- Tohum envanteri yönetimi
- Ekim planlama ve takibi
- Hasat kayıtları ve verim analizi

### Genel Özellikler
- Kullanıcı dostu arayüz
- Mobil uyumlu tasarım
- Kapsamlı raporlama ve istatistikler
- Çoklu dil desteği

## Kurulum

### Gereksinimler
- Python 3.8+
- Django 4.2+
- PostgreSQL veya SQLite
- Diğer gereksinimler için `requirements.txt` dosyasına bakınız

### Adımlar

1. Repoyu klonlayın:
```
git clone https://github.com/kullanici/tarim-hay-takip.git
cd tarim-hay-takip
```

2. Sanal ortam oluşturun ve aktif edin:
```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Gereksinimleri yükleyin:
```
pip install -r requirements.txt
```

4. Veritabanı migrasyonlarını uygulayın:
```
python manage.py migrate
```

5. Superuser oluşturun:
```
python manage.py createsuperuser
```

6. Geliştirme sunucusunu başlatın:
```
python manage.py runserver
```

7. Tarayıcınızda `http://127.0.0.1:8000/` adresine giderek uygulamayı kullanmaya başlayabilirsiniz.

## Modüller

### Kullanıcı Modülü
- Kullanıcı kaydı ve profil yönetimi
- Rol tabanlı yetkilendirme sistemi
- Oturum yönetimi

### Hayvan Modülü
- Hayvan kayıtları
- Sağlık takibi
- Üretim takibi

### Arazi Modülü
- Arazi kayıtları
- Parsel yönetimi
- Koordinat bilgileri

### Üretim Modülü
- Ürün kayıtları
- Tohum yönetimi
- Ekim planları
- Hasat kayıtları

## Katkıda Bulunma

1. Bu repoyu fork edin
2. Yeni bir özellik branch'i oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.

## İletişim

Proje Sahibi - [E-posta adresi]

Proje Linki: [https://github.com/kullanici/tarim-hay-takip](https://github.com/kullanici/tarim-hay-takip) 