
```bash
- py -m venv env
# - python3.10 -m venv env
- ./env/Scripts/activate
- source env/bin/activate (mac)
- source env/Scripts/Activate (bash)
- pip install djangorestframework
- pip install python-decouple
- pip freeze > requirements.txt
- (pip install -r requirements.txt)
- django-admin startproject main .
```


- go to settings.py and add rest_framework;

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    # my_apps
    
    # 3rd_party_packages
    'rest_framework',
]
```

- create .env and .gitignore files, hidden to SECRET_KEY.
  
- Create .env file on root directory. We will collect our variables in this file.
- 
```py
from decouple import config

SECRET_KEY = config('SECRET_KEY')
```

```py
SECRET_KEY = o5o9...
```

- create app

```powershell
- py manage.py startapp blog
```

- go to settings.py and add our app;

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    # my_apps
    'blog',
    # 3rd_party_packages
    'rest_framework',
]
```

- Migrate dbs:
```powershell
- python manage.py migrate
- py manage.py runserver
```

- Create superuser:
```powershell
- python manage.py createsuperuser
```


- Artık blog projesindeki modellerimizi/tablolarımız tasarlayarak modelimizi oluşturacağız.
- code first / db first
- Burada code first yazıyoruz.

- Modelimizi oluşturuyoruz;
models.py
```py
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    
    def __str__(self):
        return self.name
    
class Post(models.Model):
    # CHOICES= (
    #     ('p', 'Published'),
    #     ('d', 'Draft'),
    # )
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField(blank=True)
    # category = models.ForeignKey(Category, related_name="category", on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, related_name="category", on_delete=models.PROTECT)
    # status = models.CharField(max_length=2, choices=CHOICES, default="d")
    is_published = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

```

admin.py
```py
from django.contrib import admin
from .models import Category, Post

# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
```

### faker

```py
- pip install Faker
```

- create a Faker file as blog/faker_data.py
```py
from .models import Category, Post
from faker import Faker

def run():
    fake = Faker(['tr-TR'])
    categories = (
        "Life",
        "Science",
        "Politics",
        "Sports"
    )

    for category in categories:
        new_category = Category.objects.create(name = category)
        for _ in range(30):  # neden _? normalde i yazıyorduk? döngünün içinde i'yi kullanmadığımız zamanlarda _ kullanırız, i yazmış olsaydık döngünün içinde i'yi kullanmamız gerekirdi.
            Post.objects.create(category = new_category, title = fake.name(), content = fake.text())
    
    print('Finished')
```

```powershell
- py manage.py shell
- from blog.faker_data import run
- run()
- exit()
```


/////////////////////////////////////////
created_date ve updated_date fieldlarını -> 
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()
bu şekilde yazarsak faker ile tarih verebiliyoruz. Daha sonra düzeltebiliriz.
```py
from .models import Category, Post
from faker import Faker

def run():
    fake = Faker(['tr-TR'])
    categories = (
        "Life",
        "Science",
        "Politics",
        "Sports"
    )

    for category in categories:
        new_category = Category.objects.create(name=category)
        for _ in range(5):
            Post.objects.create(category=new_category, title=fake.name(), content=fake.text(), is_published=fake.pybool(), created_date=fake.date_time_between(start_date='-5y', end_date='-3y'), updated_date=fake.date_time_between(start_date='-2y', end_date='-1y'))
    
    print('Finished')

```
/////////////////////////////////////////////////

- blog app imizin modelleri için endpoint yazıyoruz,
- home page yazmayacağız,
- blog app te urls i oluşturup proj. urls inden include ediyoruz,

main urls.py ->
```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('blog.urls')),
]
```

- blog app içerisinde urls.py oluşturup, category/ path i belirleyip, hemen views.py a gidip ModelViwSet ten Category modelinin view ini yazıyoruz,
  
blog urls.py ->
```py
from django.urls import path

urlpatterns = [
    # path('category/', todo_home, name='home' ),
]

```

- category modelinin bütün işlemlerini (create, read, delete, update) yapacağız. Default CRUD işlemleri için en basiti Concrete Views ler (biri listing ve creating için, diğeri de retreve, update, delete için) iki ayrı view yazılabilir. Ya da Model View Set ile hepsini tek bir view de halledebiliriz. Biz ekstra çetrefilli bir işlem yapmayacağımız için bir methodu override etmek gibi bir işlem yapmayacağımız için ModelViewSet ile yolumuza devam ediyoruz.

blog views.py
```py
from rest_framework.viewsets import ModelViewSet
from .models import Category

class Category(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = None
```

- tabi bir de category modelimiz için bir de serializers oluşturmamız gerekiyor,
- blog ap imizin altına serializers.py create edip serializer dosyamızı yazıyoruz.
- rest_framework ten serializers ı import ediyoruz,
- modelSerializer kullanacağımız için modelimizi de import ediyoruz,

blog/serializers.py
```py
from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
        )
```

blog/views.py
```py
from rest_framework.viewsets import ModelViewSet

from .models import Category
from .serializers import CategorySerializer

class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
```

- ModelViewSet kullandığımızda urls.py da path yazmak yerine bir router tanımlıyorduk, şimdi onu yapalım,
- rest_framework den routers import ediyoruz,
- routers.DefaultRouter() ile bir router instance ı create ediyoruz,
- create ettiğimiz router instance ımıza category ismi ile bir endpoint belirleyip, bu endpoint ile CategoryView ini tetiklemesini register ediyoruz,
- urlpatterns ine de router.urls i include ediyoruz,
blog/urls.py
```py 
from django.urls import path, include

from .views import CategoryView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('category', CategoryView)

urlpatterns = [
    path('', include(router.urls)),
]
``` 

- Test ettik, Category modelimiz çalışıyor get, post , put delete yaptık çalışıyor,
- Şimdi  aynısını Post modelimiz için de yapalım,
- views.py a gidip view imizi yazalım,

blog/views.py
```py
from rest_framework.viewsets import ModelViewSet

from .models import Category, Post
from .serializers import CategorySerializer, PostSerializer

class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostView(ModelViewSet):
    queryset = Post.objects.all()
    # queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
```

- tabi bir de Post modelimiz için bir de serializers oluşturmamız gerekiyor,

blog/serializers.py
```py
from rest_framework import serializers
from .models import Category, Post

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
        )

class PostSerializer(serializers.ModelSerializer):
    
    category = serializers.StringRelatedField() # Read only, create için kullanılamıyor,
    category_id = serializers.IntegerField(write_only=True) # create için id lazım, ayrıca write only ile sadece create ederken göster bu field ı, listelerken gösterme!
    
    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'category_id',
            'category',
            'content',
            'is_published',
            'created_date',
        )
```

- post modelimizin view ve serializer ını yazdık, urls de endpointini router a ekliyoruz,
  
blog/urls.py
```py
from django.urls import path, include

from .views import CategoryView, PostView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('category', CategoryView)
router.register('post', PostView)

urlpatterns = [
    path('', include(router.urls)),
]
```

#### pagination - filter- search (Global)

- Bu projede pagination, filter, search global tanımlayacağız. View de sadece fieldları tanımlayacağız.
- Başka derslerde custom pagination yapılmıştı, oralara bakılabilir.
- cursorpagination çok kullanılan birşey değil!
- En çok kullanılan limitoffset daha sonra page dir.

##### pagination->

- Global tanımlarken settings.py da tanımladığımızda, tüm endpointlerimizde PageNumberPagination olacak ve Page_Size da 100 olacak
settings.py ->
```py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

##### filter->

- Aynı şekilde filter ı da globalde tanımlayacağız, bunun için bir pakete yüklüyorduk, 
- custom filter ı bir sonraki derste göreceğiz,
- default filter backend i şu şekilde tanımlıyoruz, settings.py içerisindeki REST_FRAMEWORK içerisine şu kodları yazıyoruz.

```py
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}
```

- Tabi bunun çalışması için django-filter paketini yüklememiz gerekiyor, 

```powershell
- pip install django-filter
- pip freeze > requirements.txt
```

- eklediğimiz third party package i settings.py da INSTALLED_APPS e ekliyoruz,
settings.py
```py 
INSTALLED_APPS=[
    # 3rd_party_packages
    'rest_framework',
    'django_filters',
]
``` 

- Artık view de hangi field a göre filter etmek istiyorsak onu belirtiyoruz,

```py
class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['name']

class PostView(ModelViewSet):
    queryset = Post.objects.all()
    # queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    # filterset_fields = ['category'] # id ile işlem yapabiliyoruz
    filterset_fields = ['category__name'] # name i ile işlem yapabiliyoruz.
```

- CategoryView view inde name field ına göre, PostView view inde category field ına göre filtrelesin. Ancak category field ı bize id dönüyor biz onun name i ile işle yapmak istersek __name eklememiz gerekiyor.
- Yani Post ta bir category e tıkladığımızda o category nin altındaki post lar gelsin bize...  

- views.py da filter ile ilgili bir import yapmadık çünkü, settings.py da global olarak tanımladık, artık herhangib ir view imizde filterset_fields tanımladığımız zaman o fieldlara göre filter yapacak.

##### search->

- Aynı şekilde search ı da globalde tanımlayacağız, 
- custom search de yapılabiliyor.
- default serach ü şu şekilde tanımlıyoruz, settings.py içerisindeki REST_FRAMEWORK içerisine şu kodları yazıyoruz.

```py
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter'
    ]
}
```

- view de hangi fieldlara göre search etmek istiyorsak onları belirtiyoruz,
- globalde tanımladığımız için view de herhangi bir import yapmadık,

```py
class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['name']
    search_fields = ['name']

class PostView(ModelViewSet):
    queryset = Post.objects.all()
    # queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    # filterset_fields = ['category'] # id ile işlem yapabiliyoruz
    filterset_fields = ['category__name'] # name i ile işlem yapabiliyoruz.
    search_fields = ['title', 'content']
```


##### ordering->

- Aynı şekilde ordering ı da globalde tanımlayacağız, 
- custom search de yapılabiliyor.
- default serach ü şu şekilde tanımlıyoruz, settings.py içerisindeki REST_FRAMEWORK içerisine şu kodları yazıyoruz.

```py
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.OrderingFilter'
    ]
}
```

- view de hangi fieldlara göre ordering etmek istiyorsak onları belirtiyoruz,
- globalde tanımladığımız için view de herhangi bir import yapmadık,

```py
class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']

class PostView(ModelViewSet):
    queryset = Post.objects.all()
    # queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    # filterset_fields = ['category'] # id ile işlem yapabiliyoruz
    filterset_fields = ['category__name'] # name i ile işlem yapabiliyoruz.
    search_fields = ['title', 'content']
    ordering_fields = ['category__name']
```


#### Authentication

- Authentication için farklı bir app yapacağız, neden? bu app sadece authentication işlemi yapacak.
- create user app ->
```powershell
- py manage.py startapp user
```

- add to INSTALLED_APPS in the settings.py

- Ayrıca settings.py da nasıl bir aıthentication oluşturacağımızı djangoya belirtmemiz gerekiyor, BasicAuthentication mı, TokenAuthentication mı bunu global olarak belirtmemiz gerekiyor,
- Biz TokenAuthentication kullanacağız,
settings.py ->
```py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
```

- TokenAuthentication bize otomatik olarak bir token üretmiyor, 
- Burada token generate etmek için signals kullanmayacağız, daha basit bir yöntem olan, bizim için django rest framework ün hazırlamış olduğu  obtain_auth_token viewini kullanarak token generate edeceğiz.
- obtain_auth_token view ne işe yarıyordu; kullanıcı kayıt olduktan sonra login işlemi yaptığında eğer db de bir token ı varsa onu response olarak frontend e dönüyor, token ı yoksa da otomatik olarak bir token oluşturuyor loginden sonra o token ı dönüyor.
- Bu projede (views kısmında user register içerisinde bir token create etme işine girmeyeceğiz) kullanıcıyı sadece register edip, login olduğunda obtain_auth_token view i bizim için db de bir token create edecek.
  
- settings.py daki INSTALLED_APPS e 'rest_framework.authtoken' ı ekliyoruz.
```py
    'django.contrib.staticfiles',
    # my_apps
    'blog',
    'user',
    # 3rd_party_packages
    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',
```

- migrate işlemi yapıyoruz, 

```powershell
- py manage.py migrate
```

- rest_framework.authtoken ile db de artık bizim bir token tablomuz oluştu, bunu admin.py da register etmemize gerek yok, zaten app içerinde otomatik geldiği için register etmemize gerek yok.
- Şu anda hiçbir user ımızın token ı yok, 
- admin panelden Tokens tablomuzdan userlarımız için token oluşturuyoruz, 
- admin ve umit adlı iki tane user ımız için tken create ettik.
- Biz bunun otomatik olmasını istiyoruz, bunun birkaç tane yöntemi var, geçenki athentication dersinde;
    - Register aşamasında, register olduğunda Create view inde def create i override nasıl token oluşturacağınızı göstermiştik.
    - Bir de obtain_auth_token ile login olunca otomatik olarak token create etmesini göstermiştik, burada onu kullanacağız.
    - Login olunca eğer token ı yoksa bize otomatik olarak bir token oluşturacak, varsa olan token ı bize dönecek.

- Signal oluşturmayı göstercekler, for ile dönüp herkes için token create etmek kullanılan bir yöntem değil, 
  
- Bir de endpoint ile mesela login/ endpointi ile views.obtain_auth_token ile login işleminde bize token create ediyor eğer token yok ise.  
 
- user app imiz için urls.py oluşturduğumuzda bu views.obtain_auth_token i kullanacağız, (730. satırlarda ....)

- Bunun için ilk önce registerımızdan sonra login işlemi yapacağımız için register ımızı yazıyoruz,

- Bu register için de bir serializer hazırlayacağız, bu serializer ile de bir view oluşturup, user ı POST ile create edeceğiz.


- RegistrationSerializer ımızı ModelSerializer dan inherit ederek oluşturuyoruz, modelimizi ise djangonun bize verdiği default User modelini kullanıyoruz,
- User model imizde hangi fieldları kullanmak istiyorsak onları yazıyoruz, 

serializers.py oluşturuyoruz ->
```py
from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2',
                  'email', 'first_name', 'last_name')
```

- burada email field ına specific özellikler vermek istiyoruz, register olurken email girilsin istiyoruz, bunu serializers da sağlayabiliriz, db de zorunlu olup olmamasına gerek yok, çünkü gelen datayı db ye göndermeden önce serializers da biz validation kontrolü yapabiliyoruz, email field dolu gelsin diye required_TRue diyoruz, bir de email in unique olmasını istiyoruz, default olarak unique değildir. django da default User modelinde unique olan username dir. Ancak biz email lerin de unique olmasını istiyorum, bunun için default validator lardan UniqueValidator kullanıyoruz ve içerisine de parametre olarak hangi modelde unique olarak arayacağını da queryset parametresiyle belirtiyoruz. validators=[UniqueValidator(queryset=User.objects.all())]
- rest_framework.validators den UniqueValidator ı import ediyoruz,

serializers.py oluşturmaya devam ->
```py
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2',
                  'email', 'first_name', 'last_name')
```

- password, ve password2 yu sadece create için kullanılması için  write_only olarak belirtmek için yazıyoruz, password2 yu da check için kullanacağımızdan dolayı required True olarak yazıyoruz,
- Ayrıca first_name de zorunlu alan değil ama biz required True yazarak zorunlu alan yapıyoruz. 

serializers.py oluşturmaya devam ->
```py
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2',
                  'email', 'first_name', 'last_name')
```

- Bir de validate yapma işlemi var, neye göre? password ve password2 ya göre validation yapıyoruz, eğer bunlar birbirine uymazsa validation error dön diyoruz,
- serializers ın validate diye bir methodu var, ve biz o methodu override ediyoruz o yüzden isim önemli def validate diyoruz,
- içerisine parametre olarak -> self, attrs  alıyor, bu attrs data -> frontend den post yapıldığında serializersda bize gelen data, gelen dataya bu attrs parametresiyle ulaşabiliyoruz. attrs parametresiyle gelen data dictionary yapısında, biz attrs['password'] ve attrs['password2'] ile ona ulaşıp if conditionunda birbirine eşit olup olmadığına bakıyoruz, eğer eşit değilse validation error döndürüyoruz, eşit ise hata vermeden attrs ile datayı dönebilirsin diyoruz.

serializers.py oluşturmaya devam ->
```py
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2',
                  'email', 'first_name', 'last_name')
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs
```

- create de açık açık username, email, first_name, last_name i validated_data içinden al ve .set_password içerisinine de validated_data içindeki passwordü ekle ve save et diye yazmışız. (geçen derste anlatıldığı gibi),
  
serializers.py oluşturmaya devam ->
```py
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2',
                  'email', 'first_name', 'last_name')
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
```

##### registration

- serializer ımızı yazdık, şimdi bunun için bir view yazacağız, views.py a gidiyoruz,
- Burada sadece create işlemi yapmak istiyoruz, bu user ı create etsin istiyoruz.
- Burada Concrete View lerden CreateAPIView kullanıyoruz, bunun işlevi neydi sadece create yapmak, import ediyoruz, 
- RegisterView imizi CreateAPIView den inherit ederek yazmaya başlıyoruz, 
- bu RegisterView imizde User default modelini kullanacağız, bunun için default User  modelini de import ediyoruz, 
- sonra RegisterView imizin queryset ini User modeli olarak yazıyoruz,
- bir de  serializer_class yazmamız lazım, onu da zaten oluşturmuştuk, import ediyoruz, 

views.py ->
```py
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
```

- Şu an bu view ile bir register işlemi yapabileceğiz,
- Biz register da bir token create işlemi yapmayacağız, bu view bizim için yeterli,  

- Şimdi bu view imiz için bir register endpoint i yazmamız gerekli, 
- main/urls e gidip user app imizin path ini include etmeliyiz, 

main/urls
```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('blog.urls')),
    path('user/', include('user.urls')),
]
```

- ardından user app imizin içinde urls.py oluşturup RegisterView imiz için endpoint yazıyoruz, 

user/urls
```py
from django.urls import path
from .views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view()),
]
```

- şimdi gidip bir test edelim, 
- http://127.0.0.1:8000/user/register/ endpoint ine gittiğimizde sayfamız geliyor ve form ile yeni bir user create edebiliyoruz, admin panelden user kısmından görüyoruz oluştuğunu,


##### login

- user app imiz için urls.py oluşturduğumuzda bu views.obtain_auth_token i kullanıyoruz,
- rest_framework.authtoken den views i imort ediyoruz, 
- path('login/', views.obtain_auth_token),  yazarak login/ path ine istek atılırsa/ login olduğumuz zaman bize otomatik olarak bir token create edecek veya tokenımız var ise onu getirecek. 

user/urls.py
```py
from django.urls import path
from .views import RegisterView
from rest_framework.authtoken import views

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', views.obtain_auth_token),
]
```

- testini yapalım, 
- postman den http://127.0.0.1:8000/user/login/   end pointi ile aynı admin panelden giriş yapar gibi username ve password ile login olmak için post ile istek atınca, bize db de daha önceden create etmiş olduğu token ı döndü.

- şimdi postmanden http://127.0.0.1:8000/user/register/  endpointi ile user create edelim ve admin panelde create ettiğimiz user için token oluşturuldu mu ona bakalım,

{
    "username": "bahar",
    "password": "bahar123456",
    "password2": "bahar123456",
    "email": "bahar@bahar.com",
    "first_name": "bahar",
    "last_name": "arat"
}

- admin panelde user create edildiğini gördük ama henüz Token tablosunda bu user ın bir token ı oluşmamış, token ne zaman oluşuyordu? login olduğu zaman oluşuyordu. O zaman  postman de http://127.0.0.1:8000/user/login/ endpointine create ettiğimiz user ın username ve password ü ile post isteği atalım bakalım bize ne dönecek, (bu user için db de bir token create etmesi ve bize dönmesini bekliyoruz.)
- postman de user create ettik, şimdi create ettiğimiz user ile login olalım, 
- evet db de bir token create etti ve bize o token ı döndü.


##### logout

- Şimdi login olduğunda token oluşuyor, tamam ama user logout olduğunda bu oluşmuş olan token ın silinmesi gerekiyor ki güvenlik açığı oluşmasın, 
- views.py da logout view imizi yazıyoruz,
- rest_framework.decorators den api_view  ve   rest_framework.response den Response u import edip, logout view imizi yazıyoruz,
  
```py
@api_view(['POST'])
def logout(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response({"message": 'User Logout: Token Deleted'})
```

- Yazdığımız view i tetikleyecek endpointimizi de urls.py da yazalım,
- Önce view imizi import edelim,
user/urls.py ->
```py
from django.urls import path
from .views import RegisterView, logout
from rest_framework.authtoken import views

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', views.obtain_auth_token),
    path('logout/', logout),
]
```

- Şimdi test edelim, ilk olarak daha önce register ile create etmiş olduğumuz user ile http://127.0.0.1:8000/user/login/   endpointini kullanarak POST ile login oluyoruz ve bize token create edip döndüğünü görüyoruz, 
{
    "username": "bahar",
    "password": "bahar123456"
}

response:
{
    "token": "1f0ebd3a1d63e4dafc5fc58f1f39a6d8aefbf7a9"
}

- Daha sonra http://127.0.0.1:8000/user/logout/  end pointine POST isteği atacağız ancak Headers kısmına user ın login olduktan sonra response ile dönen token ını -> 
  Authorization   Token 49c07ded178608ac4c743a6fc0095070096902f1  
yazıyoruz ve POST ile istek atıyoruz.
{
    "message": "User Logout: Token Deleted"
}

- Bize logout view inde Response olarak dönsün diye yazdığımız message ı görüyoruz ve user başarılı bir şekilde logout oluyor. 


#### permissions

- permission ı neden yazacağız? 
- blog app imizdeki;
  - category i sadece admin create edebilsin, diğer kullanıcılar read edebilsin.
  - post u da sadece user authenticated ise CRUD işlemi yapabilsin, diğer kullanıcılar read edebilsin.
    - Object permision ile de post un sahibi o post ile ilgili CRUD işlemi yapabilsin, diğer kullanıcılar read edebilsin şeklinde de yapılabilir. 
  - Şu aşamada authenticate olanlar CRUD yapabilsin, diğerleri read edebilsin şeklinde oluşturacağız. Bunun için hazır bir permission ımız var; IsAuthenticatedOrReadOnly  post view imiz için onu kullanabiliriz.

- blog/views.py da rest_framework.permissions dan IsAuthenticatedOrReadOnly i import ederek başlıyoruz.
- İlgili view imiz olan PostView imize gidip, permission_classes = [IsAuthenticatedOrReadOnly] yazıyoruz. Böylelikle user authenticated ise CRUD yapabilir, değilse sadece read yapabilir.

blog/views.py
```py
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Category, Post
from .serializers import CategorySerializer, PostSerializer

class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']

class PostView(ModelViewSet):
    queryset = Post.objects.all()
    # queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    # filterset_fields = ['category'] # id ile işlem yapabiliyoruz
    filterset_fields = ['category__name'] # name i ile işlem yapabiliyoruz.
    search_fields = ['title', 'content']
    ordering_fields = ['category__name']
    
    permission_classes = [IsAuthenticatedOrReadOnly]

```

- Şimdi CategoryView için ise custom bir permission yazacağız, 
- CategoryView için admin ise create edebilsin, değilse sadece read edebilsin,
- Bunun için IsAuthenticatedOrReadOnly in source code una gidiyoruz, 
- BasePermission den inherit ederek oluşturduğunu görüyoruz,
- Biz bu IsAuthenticatedOrReadOnly class ını alıp admin user için customize edeceğiz. Kopyalıyoruz, 

```copy
class IsAuthenticatedOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )
```

- blog app imizin içerisinde permissions.py isminde bir dosya create ediyoruz ve içerisine kopyaladığımız ve customize edeceğimiz IsAuthenticatedOrReadOnly class ını yapıştırıyoruz.
  
blog/permissions.py
```py
class IsAuthenticatedOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )
```

- class ımızı IsAdminOrReadOnly diye isimlendiriyoruz, 
- Tabi class ımızda kullandıklarımızı import emmeiz gerekiyor, 
- rest_framework.permissions den BasePermission  ve yine rest_framework.permissions dan SAFE_METHODS u import ediyoruz.
- has_permisson methodundaki is_authenticated yerine is_staff yazarsak burada "user staff mı" diyerek bunu kontrol ediyoruz.
- is_staff ise statusü admin user olmuş olacak, onun kontrolünü yapıyoruz.

blog/permissions.py
```py
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    
    # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')  # Yukarıda import etmektense burada da tanımlanıp kullanılabilir.
    
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )
```

- blog/views.py a gidip, Bu yazdığımız IsAdminOrReadOnly class ını import edip, 
- CategoryView imizde permission_classes = IsAdminOrReadOnly olarak tanımlıyoruz.

blog/views.py 
```py
from .permissions import IsAdminOrReadOnly

class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']
    
    permission_classes = [IsAdminOrReadOnly]
```

- Şimdi bunu test edelim, 
- Önce post işlemi yapacağız,
- http://127.0.0.1:8000/api/category/ end pointine post isteği atacağız, 
- admin panelden admin user ın token ını alıp, postman de, headers kısmında "Authorization  Token 0e47afefdc5f7ad33c9b1124edc34c213d901fe0" yazıp, 
- body kısmına da create edeceğimiz category nin istenilen fiellarını yazıyoruz, 
{
    "name": "new-category"
}

- post ile istek attığımız zaman admin yani staff user ın token ı ile yeni bir category create ediyoruz.
{
    "id": 5,
    "name": "new-category"
}



- Şimdi başka bir login olmuş normal user ın tokenı ile bu post işlemini tekrar yapalım, bize permisson hatası vermesini bekliyoruz, 
{
    "detail": "You do not have permission to perform this action."
}

- Evet yazmış category view için yazmış olduğumuz permission gereği login olmuş normal bir user category create edemiyor, category create etme permission ı sadece admin user da var.








