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
23. Öncelikle car app'inin içinde models.py'a gelerek **car modelimi** oluşturuyorum:

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

    **RESERVATION MODEL**
    Bu modelde hangi araç, hangi kullanıcı tarafından, hangi tarih aralıklarında tutulmuş, bunu göreceğim.
26. models.py'da:

    class Reservation(models.Model):
        customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')  (Bir customerın birden fazla res olabilir. Bundan dolayı foreign key kullanıyoruz. Nerede foreing key olacak? User tablosunda. User Tablosunu da model'ın üst tarafına import ediyoruz!!!!)
            (from django.contrib.auth.models import User)
            (user silinirse res de silinsin dedik. Cascade kullandık!)

        car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='cars') (reverse relationshipte yani Car modelinden res'e ulaşırken related name ile ulaşıyoruz. sen belirlemezsen django otomatik olarak belirler!!!)

        start_date = models.DateField() (Tarih aralığı olarak tutuyorum)
        end_date = models.DateField()

        def __str__(self):
            return f"Customer {self.customer} reserved {self.car}" (admin panelde bu şekilde görünecek)

    ***admin.py'a ekliyoruz:
        from .models import Car, Reservation
        admin.site.register(Reservation)
    ***
        class Meta:    (bir user'ın aynı start ve end datelerde tek bir res. olmalı!!!aşağıdaki 3'lü uniquelik oluşturuyor)
            constraints = [
                models.UniqueConstraint( 
                    fields=['customer', 'start_date', 'end_date'], name='user_rent_date' (django bu name'i istiyor, istediğin ismi verebilirsin)
            )
        ]

    ***************************
    eğer ikili/üçlü fieldlarda unuiqlik oluşturmak istiyorsak UniqueConstraint kullanıyoruz,
    #? müşteri- aynı tarihler arasında başka araç kiralayamaz bu durumda,
    #? mehmet - mercedes - 15 - 18  ilk rezervasyon
    #? mehmet - mercedes - 18 - 19  olur 
    #? mehmet - audi     - 15 - 18  olmaz araç farklı ama müşteri ve tarihler aynı
    #? ayşe - mercedes  - 15 - 18  olur, müşteri farklı
    #? mehmet - audi     - 15 - 18  olmaz çünkü araca bakmıyor

    Eğer bizden hiçbir şekilde çakışma olmasın istenseydi bu işimizi görmezdi. view'de user start ve end'i süzüp ona göre kontrol edip izin vermezdik.
    ***************************

27. migrate işlemi yapıp db'de kontrol ediyoruz.
28. şimdi öncelikle yaptığım car modeli için car içerisinde **seralizer** oluşturacağım:

from rest_framework import serializers
from .models import Car, Reservation


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            'id',
            'plate_number',
            'brand',
            'model',
            'year',
            'gear',
            'rent_per_day',
            'availability'
        )

29. Car serializerı için view yazıyorum:

from rest_framework.viewsets import ModelViewSet

from .models import Car, Reservation
from .serializers import CarSerializer
from .permissions import IsStaffOrReadOnly

from django.db.models import Q


class CarView(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsStaffOrReadOnly,)  # [IsStaffOrReadOnly] (ikisi de olabilir)
    (***car içerisinde permissions.py dosyası oluşturdum ve bu viewin altına yapıştırdığım kodları yazdım.***)

    def get_queryset(self): 
(**get isteği olduğunda döneceğimiz queryset bu. bunu conditionlara bağlıyoruz. staff ise tüm araçları görsün, değilse sadece available olanlar görünsün**)
        if self.request.user.is_staff:
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(availability=True)
        start = self.request.query_params.get('start')
(**requestin içinden gelen parametreden istediğim keyi .get ile çekerim**)
        end = self.request.query_params.get('end') 
(**params urlden sonra ? ile gelen keyler. db'ye query, filtre atmak için query_params kullanıyoruz.**)
**start ve end tarihleri arasında available olan araçları göster**
(***endpointleri oluşturmak için car içerisinde urls.py dosyası oluşturdum ve main içine include ekledim***)

**conditionları ayrı ayrı kullanabilmek için Q'yu import ettik**
        cond1 = Q(start_date__lt=end) (lt=less than, gt=greater than)
        cond2 = Q(end_date__gt=start)
        # not_available = Reservation.objects.filter(
        #     start_date__lt=end, end_date__gt=start (cond1 & cond2 ile aynı anlama geliyor)
        # ).values_list('car_id', flat=True)  # [1, 2]

        not_available = Reservation.objects.filter(
            cond1 & cond2
        ).values_list('car_id', flat=True)  # [1, 2] 
(**flat_True list olarak dönmesini sağlıyor, available olmayanları döndürecek**)
        print(not_available)

        queryset = queryset.exclude(id__in=not_available) (available olmayanları dahil etme)

        return queryset

**BİLGİ NOTU**
Django, filter() metodunda birçok kıyaslama operatörü sunmaktadır. Örnek olarak:
exact: esitliği kontrol eder.
iexact: case-insensitive esitliği kontrol eder.
contains: bir string içinde arama yapar.
icontains: case-insensitive bir string içinde arama yapar.
gt: büyüklük karşılaştırması yapar.
gte: büyüklük veya eşitlik karşılaştırması yapar.
lt: küçüklük karşılaştırması yapar.
lte: küçüklük veya eşitlik karşılaştırması yapar.
in: belirli bir liste içinde arama yapar.
**BİLGİ NOTU SON**

***permissions.py***

from rest_framework import permissions


class IsStaffOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: 
            return True     (**get, head, options gibi safe metotlardaysa herkese izin ver.**)
        return bool(request.user and request.user.is_staff)

***urls.py(main)***

urlpatterns = [
    path('api/', include('car.urls'))
]

***urls.py(car)***
from django.urls import path

from rest_framework import routers

from .views import CarView

router = routers.DefaultRouter()
router.register('car', CarView)

urlpatterns = [  (buraya include ile de dahil edebilirdim, aşağıdaki gibi yaptım)
]

urlpatterns += router.urls

**get_fields serializerda fieldların isimlerini döndüren bir metot. Yani fieldları istediğim gibi saklayabilirim. fieldların dönüş şeklini role bağlayabilirim. Örn user eğer normal ise şunları çıkar gibi. Her rol için ayrı serializer da yazabilirdik(staffserializer, userserializer) ama burada gerek yok. Sadece bir fieldı çıkarmak istiyorum.**

**Car içerisinde Serializer.py**
    def get_fields(self):
        fields = super().get_fields() 
**(super ile return eden herşeyi alıyorum, dönen bütün fieldları değişkene atadım)**
        request = self.context.get('request')
**context ile request objesine ulaşıyorum ve requesti yapanın kim olduğunu(user,staff?) anlıyorum**

        if request.user and not request.user.is_staff: 
**(request user var ve staff değilse)**
            fields.pop('availability')
            fields.pop('plate_number')
**availability ve plate_number'ı çıkar**
        return fields
**değilse hepsini dön**

**Şimdi ReservationSerializer yazmaya başlıyorum**

class ReservationSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = (
            'id',
            'customer',
            'car',
            'start_date',
            'end_date',
            'total_price'
        )
**db'ye gelmeden önce customer, start ve end datelerin validation işlemini yapmam gerekiyor. validators gönderilen bütün datayı validate ediyor.**
        validators = [
            serializers.UniqueTogetherValidator(
**unique'liği hangi tabloda arayacağım? Bütün reservation tablosuna git**
                queryset=Reservation.objects.all(),
**hangi fieldlar unique olacak?**
                fields=('customer', 'start_date', 'end_date'),
**validation sonrası dönmesini istediğim mesaj**
                message=('You already have a reservation between these dates...')
            )
        ]

    def get_total_price(self, obj):
        return obj.car.rent_per_day * (obj.end_date - obj.start_date).days

**viewde concrete view kullanacağım**

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import CarSerializer, ReservationSerializer

**ListCreateAPIView'den inherit ediyorum**
class ReservationView(ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(customer=self.request.user)

class ReservationDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    # lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        end = serializer.validated_data.get('end_date')
        car = serializer.validated_data.get('car')
        start = instance.start_date
        today = timezone.now().date()
        if Reservation.objects.filter(car=car).exists():
            # a = Reservation.objects.filter(car=car, start_date__gte=today)
            # print(len(a))
            for res in Reservation.objects.filter(car=car, end_date__gte=today):
                if start < res.start_date < end:
                    return Response({'message': 'Car is not available...'})

        return super().update(request, *args, **kwargs)

**url'de endpointleri yazıyorum**
from .views import CarView, ReservationView, ReservationDetailView
**bu modelviewset olmadığı için path yazıyorum**
urlpatterns = [
**classbased view olduğu için as_view yazıyorum**
    path('reservation/', ReservationView.as_view()),
    path('reservation/<int:pk>/', ReservationDetailView.as_view())
]

       















