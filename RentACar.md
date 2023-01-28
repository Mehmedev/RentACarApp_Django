Bu projede bir rent a car app'i yapıyorum. User tarafını daha önce yaptığım flight app'ten  aldım. Kurallar Task.pdf'te belirli.
Önce standart kurulum aşamaları:
1. python -m venv env (env oluşturuyoruz)
2. .\env\Scripts\activate (env aktive ediyoruz)
3. pip install djangorestframework (ayrıca django yüklememize gerek kalmıyor)
   (python -m django --version)
4. django-admin startproject main . (main adı ile proje başlatıyoruz)
5. .gitignore dosyası oluşturup içine google'da django gitignore diye arattığımız sayfadan (www.toptal.com) gelen metni yapıştırıyoruz.(gitignore dosyası main ile aynı hizada olacak)
6. pip install python-decouple (SECRET KEY için)
7. .env dosyası oluşturuyoruz.
8. settings.py'dan secret key'i .env dosyasına kopyalıyoruz. '' işaretini siliyoruz.
   SECRET_KEY = django-insecure-)=b-%-w+0_^slb(exmy*mfiaj&wz6_fb4m&s=az-zs!#1^ui7j
9. settings.py'a gidip
   from decouple import config
   SECRET_KEY = config('SECRET_KEY')

10. pip freeze > requirements.txt (yüklediğimiz eklentileri requirements.txt dosyasına kaydediyoruz.)
11. terminale gidip:
   python manage.py migrate  (hazır olan tabloların database'e işlenmesi için)
   python manage.py runserver
   ctrl + basarak roketi görüyoruz.
   terminale gelip ctrl + c yapıp durduruyoruz.

12. python manage.py startapp users diye app kurmamız gerekirdi ama bu projede flight app'ten users klasörünü aldım. bu işleme gerek kalmadı.
13. user appsi tanıması için settings'e gelip users'ı ekledim
    # myapps (bu kısmı tercih, düzenli dursun diye)
    'users',
14. yüklediğimiz rest-framework'ü settings içinde app'lere ekliyoruz.
    # third party (bu kısmı tercih, düzenli dursun diye)
    'rest_framework',
15. yüklediğimiz users'da urls'de dj_rest_auth'un authentication kullanmışız. bundan dolayı install yapıyoruz. Terminalde:
    pip install dj-rest-auth
    akabinde tekrar pip freeze > requirements.txt
    settings'de third party içine ekliyoruz:
    # third party
    'rest_framework',
    'dj_rest_auth',
16. Authentication rest-framework ayarları yapmak için, hangi authentication kullanacaksak bunu belirtmek için settings sonuna:
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
ekledik.
17. bunu kullanmak için, tokenları tutacağım tablo oluşturması için settings'de app'lere:
    # third party
    'rest_framework',
    'dj_rest_auth',
    'rest_framework.authtoken', (ekledik)
18. main urls'e geliyorum. users ile başlayan bir istek geldiği zaman beni nereye yönlendirecek. onu ekliyorum, include'u import ediyorum ve users path'ini ekliyorum

    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('users/', include('users.urls')),

19. python manage.py migrate
20. Admin için superuser oluşturuyoruz. terminalde şunu yazıyorum:
    python manage.py createsuperuser
21. tekrardan runserver diyip, sonrasında /admin, /users, /register vb. diyerek kontrolleri yapabilirsin.
22. car app'ini oluşturuyorum ve settings.py'da apps içine ekliyorum
    python manage.py startapp car

    # myapps
    'users',
    'car',
23. Öncelikle car app'inin içinde models.py'a gelerek car modelimi oluşturuyorum:

class Car(models.Model):
    GEAR = (
        ('a', 'automatic'), ('a' database'de nasıl görünecek, 'automatic' kullanıcıya nasıl görünecek. bizim için önemli olan backende gönderirken 'a' göndermek, diğeri reactte değiştirilebilir)
        ('m', 'manuel')
    )
    plate_number = models.CharField(max_length=15, unique=True) (her plaka unique, en fazla 15 karakter)
    brand = models.CharField(max_length=15)
    model = models.CharField(max_length=20)
    year = models.SmallIntegerField() (smallinteger -32768 to 32767 arasını destekler, küçük rakamlarda db'de kullanım alanı için bunu tercih ederiz.)

    gear = models.CharField(max_length=1, choices=GEAR) (burada iki seçenek öngördüğüm için choices yazdım ve üstte tanımladım. db'de a yada m olarak kaydedeceğimden dolayı max=1 verdim. db perf. açısından önemli)

    rent_per_day = models.DecimalField(  (burada max toplam karakter, decimal da ,'den sonraki karakter sayısı)
        max_digits=7,   (yani virgül ile birlikte en fazla 99999,99 olabilir)
        decimal_places=2,
        validators=[MinValueValidator(1)] (girilecek min değeri belirtmek için kullandık) validator'ı kullanmak için :
        from django.core.validators import MinValueValidator'ı import ettim.
    )

    availability = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.model} - {self.brand} - {self.plate_number}' (tabloda nasıl görüneceğini belirttim)


24. adminde görebilmek için car app içindeki admin.py'a import ve register yapıyorum
    from .models import Car

    admin.site.register(Car)
25. python manage.py makemigrations (modeli create etti)
    python manage.py migrate
    admin panele gidip car app'inin geldiğini kontrol ediyorum ve araç girişleri yapıyorum.














