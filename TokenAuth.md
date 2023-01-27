
- Önce environment kuruyoruz,

```bash
- py -m venv env
- ./env/Scripts/activate

- pip install -r requirements.txt

or

- pip install django
- pip install python-decouple
- pip install djangorestframework
- pip freeze > requirements.txt

```

- create .env and .gitignore files and add SECRET_KEY

/////////////////////////////////////

terminalden .env dosyası oluşturmak ->
1- Tek satırlık bir .env dosyası oluşturmak için; (bash ve powershell de çalışıyor.)

```bash
- echo SECRET_KEY=gshdagyufsd/9*-54548/*-*ur9u > .env
```

2- Çok satırlı, elimizi konsoldan çekmeden; (sadece bash de çalışıyor, powershell de çalışmıyor.)
```bash
- cat > .env
SECRET_KEY=gshdagyufsd/9*-54548/*-*ur9u
DEBUG=True
- Ctrl+C
```

/////////////////////////////////////


```bash
- py manage.py migrate
- py manage.py createsuperuser

```

- Braya kadar ne var; bir modelimiz var, serializers.ModelSerializer dan inherit edilmiş bir serializer ımız var, generics.ListCreateAPIView ve generics.RetrieveUpdateDestroyAPIView den inherit edilerek oluşturulmuş bir view imiz var.

## Authentication

- authentication ile yetki kontrolü, sizin kim olduğunuzu ve yetkileriniz ne olduğu belirleniyor, 


## Permission

- permission ile gerekli izinler tanımlanıyor.
  autherization, permission ile aynıdır


https://www.django-rest-framework.org/

- frontend authentication atlatması biraz daha kolay.


### Permissions:

- permission ların da seviyeleri vardır, global permission policy, view bazında permission hatta object bazında permission yapılabilir. Mesela student modeli üzerindeki bir öğrenci üzerinde bile permission policy yapılabilir.

- Permission policy leri global olarak, view bazında permission set etme,
- Global permission policy set etme, settings.py da yapılıyor, dokümanda var.
- view bazında permission set etme, class base viewlerde ve function base view lerde olmak üzere iki yolu var.
  class base view: 
  import edip,
  permission_classes = [IsAuthenticated]
  attribute ünün içerisinde uygulamak istediğimiz izni view bazında set edebiliyoruz.

  function base view: 
  import edip,
  @permission_classes([IsAuthenticated])
  decorator ün içerisinde uygulamak istediğimiz izni view bazında set edebiliyoruz.

- Build-in, hazır olarak gelen permission larımız var. 
  AllowAny (Default olarak geliyor. Yani herşeye izin ver.)
  IsAuthenticated (login olmuş userlara izin var.)
  IsAdminUser (admin userlara izin var.)
  IsAuthenticatedOrReadOnly (login olmuş userlara izin var, değilse sadece okuyabilsin)

- DjangoModelPermissions; view bazında verdiğimiz permissions ları set edebilmemiz için DjangoModelPermissions policy i uygulamamız gerekiyor. Buradaki izinler model seviyesinde izinler.
  DjangoModelPermissionsOrAnonReadOnly (login olmuş userlara izin var, değilse ReadOnly)

- DjangoObjectPermissions; yine yukarıdaki gibi bir user a model seviyesinde çeşitli izinler set ediliyor. Ama object seviyesinde izinler verebilmemiz için birtakım yapıya ihtiyaç var. django-gurdian gibi bir paket eklemek gerekiyor, object seviyesinde permission verebilmek için. Set etmek için DjangoObjectPermissions ismi ile set etmek gerekiyor.

- Custom Permissions; 
  .has_permission(self, request, view)
  .has_object_permission(self, request, view, obj)
  iki methodu kullanarak yazacağız.



### Authentications:

Authentication Çeşitleri:
    BasicAuthentication
    TokenAuthentication
    SessionAuthentication
    RemoteUserAuthentication


Authentication:

- Global Authentication, 
- View bazında set etme ,
  class base view:
  function base view:


- Best practice;
- Authentication policy golobal olarak set etmek daha kullanışlı. Genelde bu şekilde yapılıyor. View bazında set etmeye imkan var ama genelde global olarak set edilir. Authentication policy golobal olarak settings.py da yapılır, projemizin bütün kısımları için aynı olması daha kullanışlıdır.
- Permission policy ise global olarak set edilmez, view bazında set edilir.

- BasicAuthentication; frontend den yapılan her istekte, isteğin header kısmında isteği yapanın username i ve password ünü de istiyor. Her istekte kullanıcı username ve password göndermek zorunda. Bu yüzden BasicAuthentication güvenli değil. Genellikle test ortamında kullanılıyor. Genellikle testing için uygundur.


- Şimdi Permission policy leri BasicAuthentication da görelim.

- admin panelden birkaç modelimize tane obje(student) ekleyelim

- Postman kullanışlı bir araç, özellikle API yazıyorsanız. Django güzel bize browsable API yapısı sunuyor ama konular detaylandıkça, bizim için yeterli gelmiyor. Biz yazdığımız API leri test etmek için postman gibi araçları kullanıyoruz.

- Postman i açtık, url imize (ListCreate url i) get ile veri çektik, body kısmına objemizi yazarak POST ile ekledik. (eklerken virgül e dikkat, objenin son satırından sonra virgül gelmeyecek.)

- Halihazırda  herhangi bir permission, authentication policy uygulamadık, yani herkes get ve post ile veri çekip, create edebiliyor.



#### BasicAuthentication

- BasicAuthentication ekliyoruz;
- Projemize dönüyoruz, authentication ları global olarak set etmek daha makbul.
- Dokümandan Setting the authentication scheme başlığının altındaki kodları alıp  settings.py dosyamıza yazıyoruz.

<settings.py> ->

```py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ]
}
```

##### IsAuthenticated: (login olması durumu)

- global olarak BasicAuthentication ı set ettik ama herhangi bir permission policy imiz yok. Yani şuan yine GET ve POST ile herhangi bir kullanıcı veri çekip, create edebilir.
- Bunun için list ve create için kullandığımız view e gidip;
  rest_framework.permissions dan IsAuthenticated ı import ederek view imizin içine permission_classes ımızı [IsAuthenticated] olarak tanımlıyoruz.

  from rest_framework.permissions import IsAuthenticated

  permission_classes = [IsAuthenticated] 
    
<views.py> ->

```py
from rest_framework.permissions import IsAuthenticated

class StudentList(generics.ListCreateAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    permission_classes = [IsAuthenticated]

```

- Artık bu view imizi çalıştırmak isteyen userın login olmuş olması lazım. login olmamış bir user listeleme (GET) ve create (POST) yapamaz. Niye çünkü IsAuthenticated policy sini bu view e set ettik.

- Postmanden deniyoruz;

 "detail": "Authentication credentials were not provided."

 hatası verdi. Yani authenticated değilsin.

<!-- - StudentOperations view imiz için de aynısını yapıyoruz. -->

- Tamam authenticated olalım, authenticated policy mizi ne diye belirlemiştik? BasicAuthentication . BasicAuthentication nasıl authenticated oluyordu? her istekte username ve password u ekleyerek.
- Bizim iki tane kullanıcımız vardı. postman de Authorization kısmına gidiyoruz, Basic Auth seçimi yaptık, karşımıza Username ve Password giriş menüsü çıktı. Her isteğimizde hangi user login olacaksa onun username ve password ü ile istek atıyoruz.
- Deniyoruz, get isteği yaptık, çalıştı, POST yaptık çalıştı. (Yalnız bu işlemleri postmande yaparken tarayıcıda admin paneli kapatmamız lazım. Açıksa hata veriyor. çünkü settins.py da SessionAuthentication kısmını kapatmıştık. YOOO ÇALIŞTI anlamadım burayı belki yoktur böyle birşey.)


##### IsAdminUser: (admin olması durumu)

- Bunun için list ve create için kullandığımız view e gidip;
  rest_framework.permissions dan IsAdminUser ı import ederek view imizin içine permission_classes ımızı [IsAdminUser] olarak tanımlıyoruz.

  from rest_framework.permissions import IsAuthenticated, IsAdminUser

  permission_classes = [IsAdminUser] 
    
<views.py> ->

```py
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class StudentList(generics.ListCreateAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser]

```

- Artık bu view imizi çalıştırmak isteyen userın login olmuş olması yetmiyor, login olan kişinin admin olması gerekiyor. admin olmayan user listeleme (GET) ve create (POST) yapamaz. Niye çünkü IsAdminUser policy sini bu view e set ettik.

- Postmanden deniyoruz;

 "detail": "You do not have permission to perform this action."

 hatası verdi. Yani bu aksiyon için permission a sahip değilsin dedi.


- Tamam authenticated olalım, authenticated policy mizi ne diye belirlemiştik? BasicAuthentication . BasicAuthentication nasıl authenticated oluyordu? her istekte username ve password u ekleyerek.
- Bizim iki tane kullanıcımız vardı. postman de Authorization kısmına gidiyoruz, Basic Auth seçimi yaptık, karşımıza Username ve Password giriş menüsü çıktı. Her isteğimizde hangi user login olacaksa onun username ve password ü ile istek atıyoruz.
- Önce admin olmayan user ımızın username ve password ü ile denedik, hata verdi, sonra admin in username ve password ü ile denedik çalıştı.
- Deniyoruz, get isteği yaptık, çalıştı, POST yaptık çalıştı.


##### IsAuthenticatedOrReadOnly: (eğer kullanıcı login değil ise sadece read yapabilsin, create put update delete gibi işlemleri yapamasın.)

- Bunun için list ve create için kullandığımız view e gidip;
  rest_framework.permissions dan IsAuthenticatedOrReadOnly ı import ederek view imizin içine permission_classes ımızı [IsAuthenticatedOrReadOnly] olarak tanımlıyoruz.

  from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

  permission_classes = [IsAuthenticatedOrReadOnly] 
    
<views.py> ->

```py
from rest_framework.permissions import IsAuthenticated, IsAdminUseri IsAuthenticatedOrReadOnly

class StudentList(generics.ListCreateAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    # permission_classes = [IsAuthenticated]
    # permission_classes = [IsAdminUser]
    permission_classes = [IsAuthenticatedOrReadOnly]

```

- Artık bu view imizi çalıştırmak isteyen user eğer login değilse sadece read yapabilir, create put update delete gibi işlemleri yapamaz.

- Postmanden deniyoruz;
  login olmayan bir user ile Get ile listeleme yaptık, çalıştı ama post ile create yapmaya çalştığımızda aşağıdaki hatayı verdi. 

 "detail": "Authentication credentials were not provided."

 hatası verdi. Yani Kimlik doğrulama bilgileri sağlanmadı. dedi.

- Login değilse sadece get, read  yapabiliyor, post yapamıyor.
- Login oluyoruz, post yapmaya çalışıyoruz, evet post yapabildik.



### Buradan başlıyor...

#### TokenAuthentication  

- BasicAuthentication güvenli değil çünkü her istekte username ve password ü gönderiyoruz (frontend den, react tan, fetch ile, axios ile yapılan her istekte header kısmına username ve password ü tekrar koyuyorsunuz.). Bu güvenlik açısından çok uygun bir durum değil. Bir de BasicAuthentication bizim password ümüzü Base64 e göre kendince şifreliyor ama Base64 çok kolay çözülebilen bir şifreleme yöntemi hemen çözülebiliyor. (base64decode.org da çözdük.) Zaten dokümanında da bu uyarı var, test için kullanın, eğer production için kullanılacaksa API lerinizin https isteklerine yani güvenli isteklere cevap verdiğinden emin olun gibi bir uyarı var. 

- TokenAuthentication -> Bizim için backedimiz bize bir token üretecek, bize o token ı verecek, frontend den yapacağımız her istekte o token ı isteğimizin header kısmına koyacağız ve isteğin kimden geldiğini o token ile anlayacak ve authenticated bir user gibi bize bir permission verecek.

- Bunu nasıl uyguluyoruz?
- Dokümanda yazdığı gibi 'rest_framework.authtoken' paketini INSTALLED_APPS e akliyoruz;

<setting.py> ->

```py
'rest_framework.authtoken',
```

- Bunu ekledikten sonra terminalde bize 3 tane uygulanmayı bekleyen migrations uyarısı yaptı. bekleyen migrations tablon var. Çünkü tokenları bir tabloya kaydedecek. O yüzden server ı durdurup migrate yapıyoruz. ve server ı tekrar çalıştırıyoruz.

```bash
- py manage.py migrate
- py manage.py runserver
```

- Ardından settings.py daki  DEFAULT_AUTHENTICATION_CLASSES kısmındaki BasicAuthentication ı TokenAuthentication olarak değiştiriyoruz.

<setting.py> ->

```py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ]
}

```

- Artık uygulamamıza login olacak kullanıcılar TokenAuthentication ile login olacaklar.

- Admin panele gidiyoruz, Auth Token isimli bir yapının geldiğini görüyoruz.

- Tokens a girip admin için bir token ekliyoruz. Artık frontend den yapacağımız isteklerde bu token ı koyarsak bizi login olarak algılayacak. 

- view imizin permission_classes ını IsAuthenticated olarak değiştiriyoruz ki authenticated olmayanlar list veya create yapamasın.

      permission_classes = [IsAuthenticated]

- Token ı alıyoruz, postman e gidiyoruz Authorization ı No Auth yapıyoruz, GET isteği atıyoruz ama bizim IsAuthenticated yaptığımız için authenticated olmamızı bekliyor. 
- Authentication credentials ımızı TokenAuthentication yapmıştık,
- Postmande Headers kısmına geliyoruz Authorization satırı ekleyip value kısmına <Token *********> yazıp taken ımızı ekliyoruz
  
  Token e2146929f2852b491aabbd7f89c3c29b63ffb454

- Token ın eklenmiş haliyle get isteği attığımızda çalıştı.

- Bearer token jwt de kullanılıyor, json web token

- Biz burada admin panlede token ürettik, manuel olarak aldık ve postmande yapıştırıp sonra get, post yaptık. Ancak bunu normalde böyle yapmıyoruz, user username ve password ü ile istek atacak, user a response olarak token dönmesi gerekecek, user da response olarak dönen token ı bir değişkene tanımlayacak ve user bundan sonra yapacağı her istekte bu token ı kullanacak. Bunu otomatik sağlamamız lazım.
- Bunun için dokümana gidiyoruz, çeşitli token create etme yöntemleri var.


- signals kullanarak token create etmek
- signals : bir işlem yapıldığında başka bir işlemi de peşinden ekleme; 

dokümandaki kodlar: <signals.py> ->

```py
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
# herhangi bir user create edildiğinde (post_save dediği o) aşağıdaki kodu çalıştır.
def create_auth_token(sender, instance=None, created=False, **kwargs):
# buradaki instace user ı dinliyor, bir user create edildiğinde;
    if created:
        Token.objects.create(user=instance)
        # bu user a token tablosunda bir token create ediyor.
```

- Bunu sonra kullanacağız.


####  obtain_auth_token view i kullanarak token create etmek;

- Bu view kullanıcı login olduğunda bize token dönüyor. Biz bunu kullanacağız token için. Djangonun içerisinde gelen bir yapı.

- Bunu kullanmak için, login, register, logout işlemleri için user_api isminde bir tane daha app oluşturuyoruz.

```bash
- py manage.py startapp user_api
```


main <settings.py>

```py
INSTALLED_APPS = [
    'rest_framework.authtoken',
    'user_api',
]

```


main <urls.py>

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('student_api.urls')),
    path('user/', include('user_api.urls')),
]
```


user_api <urls.py>

```py
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
]
```

- .../user/login şeklinde istek geldiğinde obtain_auth_token view imizi çalıştıracak.
- obtain_auth_token django tarafından hazır olarak sunulan bir yapı.
- obtain_auth_token bu view bizden username ve password bekliyor ve bir token dönüyor. Bu token ı da eğer token tablosunda bir token varsa döndürüyor, yoksa tabloda bir token create ediyor.
- Deniyoruz, serverı çalıştırıyoruz, admin panele gidiyoruz, umit diye bir user ve admin var ve ikisinin de token ı var. postmane gidiyoruz, Headers kısmındaki Token ı kaydettiğimiz satırı siliyoruz, postman in urls kısmına localhost..../user/login/ yazıyoruz, bizden ne istiyor bu url e giderken? username ve password istiyor, body kısmına 
  {
    "username":"admin"
    "password":"admin"
  }
yazarak post isteği atıyoruz. Bize bir token dönüyor, (react ta kullanıcı username ve password ile bu end point e post methoduyla istek atacak request kullanıcıya bir tane token dönecek ve kullanıcı bu token ı alıp bir değişkene atayacak ve o değişkeni bundan sonraki her istekte hearer kısmına koyacak.)bundan sonra biz o token ı Headers kısmında Authorization kısmına eklersek bizi artık login olmuş olarak görcek ve get veya post isteği atınca bize response olarak dönecek. 
- kullanıcının token ı varsa on dönecek, yoksa bir tane create edip onu dönecek. Admin panelde token ı olmayan bir kullanıcıya token oluşturduğunu gördük.
- Çalıştırıyoruz, çalıştı.
- kullanıcı logout olunca o kullanıcının token ını token tablosundan silecek.


- Rgister;
- user create edeceğiz.
- register için user_api app imizde bir register view i yazmamız ve bunu bir url e bağlamamız ardından da bu url e istek atmamız lazım.
- kullanıcı register olacağı zaman bilgilerin girecek ve gönderecek, bu bilgiler bize gelince bunları serializer dan geçirmemiz lazım, json yapısından python veri yapılarına çevirebilmek için.
- user_app imizin içine register serializer eklememiz lazım.
- serializers.py dosyası create edip, serializers.ModelSerializer dan inherit ederek oluşturulmuş bir RegisterSerializer class ını kullanıyoruz. Bu kapsamlı bir register serializers, bunu başka projelerinizde de kopyalayıp kullanabilirsiniz. 

RegisterSerializer (Şam, başka projelerde de kullanılabilir.)

<serializers.py>

```py
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

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

# from django.contrib.auth.models import User
# from rest_framework import serializers

# class RegistrationSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']
```

- email, password ve password2 yi yeniden tanımlamışız, normalde email zorunlu değildi ama required True ile zorunlu hale getirebiliriz. Ayrıca bir validasyon eklemişiz, UniqValidator eklemişiz, yani bir kullanıcı kayıtlı bir email i tekrar kullanamasın.
- password lerimiz write_only=True yani password leri sadece yazabiliriz, biryere password datası gönderemez, required=true, validators da belirtiyoruz. password2 confirmation için.  Bu üç field ı tekardan tanımlamışız.
- ModelSerializer, hangi model? User modeli, 
- kullanıcıdan register olması için beklediğimiz fieldları ekliyoruz,modelin username,password, email, first_name, last_name fieldlarını doldurulmasını istiyoruz,
- ayrıca first_name ve last_name e required=True, diyerek doldurmasın ızorunlu hale getiriyoruz.
- Ardından custom validation yazmışız, password ve password2 doğru mu değil mi bunun kontrolü yapılıyor ve doğru değilse bir hata mesajı döndürüyor.
- Sonrasında create methodunu yeniden tanımlıyoruz, çünkü bize gelen data içerisinde username, email, first_name, last_name var. Biz bu username, email, first_name, last_name ile bir user create edebiliyoruz. password ü bu şekilde create edemiyoruz, o zaman password db de açık bir şekilde yazılı olurdu. Bu da güvenli olmazdı. password ü set_password methodu ile user a ekliyoruz ve user  save edip döndürüyoruz.

- serializers ımızı da yazdığımıza göre register için yazacağımızı view imize geçebiliriz,
- RegisterSeralizers ımızı import ediyoruz,
- User modelimizi django.contrib.auth.models den import ediyoruz, 
- RegisterView class view imizi generics.CreateAPIView dan inherit ederek yazıyoruz, 
  queryset = User.objects.all()
  serializer_class = RegistrationSerializer


- RegisterViewimizi yazdık, bunun endpoint ini oluşturacağız urls.py da;

```py
  from .views import RegisterView
  
  path('register/', RegisterView.as_view(), name='register'),

```

- artık yeni bir user ı postman üzerinden ya da react üzerinden create edebiliriz.
- postman e gidiyoruz, 
- http//:localhost8000/user/register/ url ine bizden istediği fieldları post methoduyla, body kısmından, json tipinde  gönderdiğimizde 
  {
    "username": "tuğba",
    "password": "tuğ123456",
    "password2": "tuğ123456",
    "email": "test@test.com",
    "first_name": "tuğba",
    "last_name": "arat"
}

bize yeni bir user create ediyor;

{
    "username": "tuğba",
    "email": "test@test.com",
    "first_name": "tuğba",
    "last_name": "arat"
}

- admin panelden de kontrolünü yapıyoruz; evet create olmuş.

- daha sonra create ettiğimiz bu kullanıcı ile /user/login/ endpointinden username ve password ile istek attığımızda bu user için token oluşturdu ve o token ile /api/student/ endpointinden get ve post istekleri atabiliyoruz.

- Evet artık postman üzerinden yani react ile /user/register endpointine istediği bilgilerle post methoduyla istek atarsanız, django ile yazdığınız backend e kullanıcı register edebilirsiniz.

- Tamam şimdi kullanıcı register oldu ama hala token bilgisi yok, yani bu register olmuş kullanıcı login olması gerekiyor ki token tanımlansın, ve isteklerinde bu token ı kullansın ki biz de o token a göre isteğe yanıt verelim.
- Genelde bir user uygulamaya register olduğunda direct uygulamaya login edilir. Bu mantıktan yola çıkarak register view imizin create methodunu override edeceğiz, içerisinde token ımızı oluşturup response datanın içerisine koyacağız.
- Burada frontend ekibi ile konuşarak, kullanıcı register olduğunda işte kullanıcının fotoğrafını da döndür, profil bilgileri vs. ne döndürülmek isteniyorsa bu şekilde dönen dataya ek konulup göderilebilir. Biz şu an sadece token koyacağız.

- bir kullanıcı register olduğu zaman o kullanıcıya bir token üretelim ve o token ı, burada dönen data içerisine ekleyelim.
- Bunu nerede yapacağız? register yapan view imizde yapacağız.
- Peki biz bu view imizin hangi methodunu override ederek yapacağız?
- bu view imizi CreateAPIView den inherit ederek oluşturmuştuk, source koduna gidiyoruz, CreateAPIView de CreateModelMixin den inherit edilerek oluşturulmuş, onun source koduna gidiyoruz, buradaki create methoduna bakıyoruz, bizim user create etmemizi sağlayan method bu. Biz bu user methodunun içerisine usera ait bir token create edeceğiz ve o token ı da buradaki response a koyacağız.
- Bunu kopyalıyoruz, view imize getirip yapıştırıyoruz, 
- Response ve status u da import ediyoruz.
 
<views.py> ->

```py
from django.shortcuts import render
from .serializers import RegistrationSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        user = serializer.save()
        token = Token.objects.create(user=user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
```

- CreateModelMixin source codu na tekrar gidiyoruz, burada self.perform_create(serializer) diye bir method var, ne yapıyormuş? sadece serializer save yapıyormuş. Biz kendi view imizde bu methodu değil de serializer.save() yapıp bunu da bir user değişkenine tanımlıyoruz. Böylece bir user create etmiş oluyoruz.
  user = serializer.save()

- Şimdi bu user ile token tablosunda bir token create edip token değişkenine tanımlayacağız;

    token = Token.objects.create(user=user)
  
- Token tablomuzu da import etmeliyiz tabi;

  from rest_framework.authtoken.models import Token

- Az önce create edilmiş olan user a bir token create ettik ve bu token ı da 

  data = serializer.data
  data['token'] = token.key

- bizim normalde döndürdüğümüz data olan serializer.data yı, data isminde yeni bir değişkene  atadık,  bu değişkene de token isminde key ve value şeklinde tekrardan token key ini ekledik.
- Artık response olarak serializer.data yı değil de data yı response edeceğiz.

```py
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        user = serializer.save()
        token = Token.objects.create(user=user)
        data = serializer.data
        data['token'] = token.key
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
```

view imizin son hali yani token creaet edilmiş ve bu token ın data içerisine eklenmiş hali ->

user_app <view.py> ->

```py
from django.shortcuts import render
from .serializers import RegistrationSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        user = serializer.save()
        token = Token.objects.create(user=user)
        data = serializer.data
        data['token'] = token.key
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
```
 
- Test edelim, başka bir user create edelim ve bakalım çalışıyor mu?
- Test ettik, create ettiğimiz user bilgileri ile birlikte token bilgisi de döndü.


#### signal kullanarak token create etmek:
- Signals Token create etmek için:
- Token create etmek için bir de signal kullanıyorduk demiştik;
- dokümandan By using signals kısmından kodları kopyalayıp, user_api daki models.py a ekliyoruz.
- 
user_api <models.py>

```py
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
```

- Bu signal bizim user tablomuzu dinliyor, User tablomuzda herhangi bir post_save işlemi olduğu zaman, yani user create edildiği zaman onu instance a atıyor ve created True oluyor ve created true ise Token tablomuzda yeni oluşturulmuş user ile bir token oluşturuyor.

- Tamam şimdi signal kullanalım, view imize gidelim, 
- Artık view imizde token create etmeyeceğimiz için yoruma alıyoruz, serializer.save() dediğimizde user ımız create ediliyordu, user ı create ettiğimiz zaman signal dirkt gidip token tablosuna create edecek. O yüzden burada create değil de token tablosunda model tarafından create edilmiş token ı çekip, aynı şekilde data nın içerisine koyup, response olarak gönderebiliriz, hatta ekstra datanın içerisine istediğimiz herhangi bir şeyi de koyabiliriz. Mesela bir tane mesaj koyalım, 
```py

  # token = Token.objects.create(user=user)
  token = Token.objects.get(user=user)
  data['message'] = 'user created successfully'

```


user_app <view.py> ->

```py
from django.shortcuts import render
from .serializers import RegistrationSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        user = serializer.save()
        # token = Token.objects.create(user=user)
        token = Token.objects.get(user=user)
        data = serializer.data
        data['token'] = token.key
        data['message'] = 'user created successfully'
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
```

- postmande çalıştırdık, user register ettik ve bu sefer signal ile token create ettiğini ve data içerisinde döndüğünü gördük.


- Logout
- Şimdi logout yapacağız;
- logout da herhangi bir veri almayacağımız için serializer filan yazmaya gerek yok. 
- views.py dosyasına gidip logout_view imizi direct yazıyoruz.
- Basit bir function view imiz var, serializer a filan gerek yok çünkü bir veri gelmeyecek, sadece post methoduyla logout endpointine istek attığımızda isteğin head kısmında kimin token ı varsa, yani o istek kime ait ise onu logout edecek yani token tablosundan token ını silecek bu kadar. @api_view decorator ünü import etmemiz lazım.

<views.py> ->

```py
@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        data = {
            'message': 'logout'
        }
        return Response(data)

```

- Bu ne yapıyor? request.method post ise, request.user.auth_token.delete() ile o user ımızın token ını delete edecek token tablosundan, data response edecek, içinde de logout yazan bir mesaj olan bir data response edecek.

- Şimdi bu view imize bir url yazalım; 

user_api <urls.py>

```py
    path('logout/', logout_view, name='logout'),

```

- test ediyoruz; herhangi bir user ın token ıile /user/logout/ endpoint inden post methoduyla istek atınca, token ı sildi ve logout etti.


- login, logout, register yaptık;
- şimdi custom permission yazalım;
- documana gidiyoruz, eğer custom permission yazacaksanız en temelde BasePermission class ı var, bunu inherit ederek yazabilirsiniz veya mevcut permissions larla, neydi onlar? IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly bunları inherit ederek bunların şu methodlarını değiştirebilirsiniz ->  
  .has_permission(self, request, view)
  .has_object_permission(self, request, view, obj)

- view bazında bir permissions yazmak istiyorsanız, has_permission ,
- object seviyesinde bir permissions yazmak istiyorsanız, has_object_permission methodunu override etmeniz gerekiyor.
- Biz ikisini de yapacağız, şöyle bir mantık kuracağız, bizim userlarımız vardı, bu userlar student modelimizde student da   create ediyorlar, biz hangi user hangi student ı create etti bunu tespit edebilmek için student modelimize bir de user field ı ekleyeceğiz ve o andaki login olan user student create ettiği zaman user bigisi de bu eklediğimiz user field ına atanacak. Daha sonra o student object ini update edeceğimiz zaman şunu kontrol edeceğiz -> sen o student in create edeni misin? eğer create edeni sen isen o zaman update veya delete edebilirsin, ama değilsen sadece bu student verisini okuyabilirsin. Böylece object seviyesinde bir permissions tanımlamış olacağız.

- student_api app imizin altında permissions.py isimli bir dosya oluşturuyoruz;
- Ne demiştik ya BasePermission class ından inherit edeceğiz veya mevcut permission policy lerimizi inherit edip o iki methodu yani -> 
  .has_permission(self, request, view)
  .has_object_permission(self, request, view, obj)

  bu methodları değiştireceğiz.

- önce view bazında bir custom permission yazacağız; permissions.py dosyamıza gidip, permissions larımızı rest_framework den import ediyoruz, sonra permissions.IsAdminUser dan inherit ederek class view imizi yazmaya başlıyoruz. Buradaki amacımız view in isminden de anlaşılacağı üzere admin ise admin ise izin ver, admin değil ise 
sadece read only yapabilsin tamamen engelleme. Normalde IsAdmin de tamamen engelliyordu, ama biz custom yapacağız.
  def has_permission(self, request, view):
    if request.method in permissions.SAFE_METHODS
    gelen isteğim (get head options) veride bir değişiklik yapmayan sadece read eden methodlar ise o zaman ->
    return True  
    yani izin ver
    değilse yani (post put delete) veride bir değişiklik yapan methodlar ise o zaman 
    return bool(request.user.is_staff)
    stuff ise true dön, değilse false dön izin verme.

permissions.py

```py
from rest_framework import permissions

class IsAdminorReadOnly(permissions.IsAdminUser):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user.is_staff)
```

- Şimdi bu permissions.py da yazdığımız IsAdminorReadOnly class ını student_api app imizin views.py ına giderek import ediyoruz; ve permission_classes ına tanımlıyoruz.
  from .permissions import IsAdminorReadOnly
  permission_classes = [IsAdminorReadOnly]

student_api <views.py> ->

```py
from django.shortcuts import HttpResponse
from .models import Student
from .serializers import StudentSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .permissions import IsAdminorReadOnly



# Create your views here.
def home(request):
    return HttpResponse('<h1>API Page</h1>')


class StudentList(generics.ListCreateAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminorReadOnly]
    # permission_classes = [IsAdminUser]
    # permission_classes = [IsAuthenticatedOrReadOnly]
       

class StudentOperations(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
```

- şimdi gidelim postman e, admin olmayan bir user ile post deneyelim, bir de admin ile post deneyelim; 
- admin panelden bakıyoruz, bir tane admin user var, diğerleri stuff değil, bir admin daha yapıyoruz,
- admin olmayan bir user ile deniyoruz, token tablosundan token ını alıp onunla istek atacağız,
- Evet önce get isteği yapıyoruz, get ise sıkıntı yok okuyabilecek ama post isteği yapınca izin vermemesi lazım çünkü istek attığımız user is staff değil, deniyoruz, evet "You do not have permission to perform this action." hata mesajı döndürüyor bize.
- Aynı işlemi admin olan bir user ile deneyelim, is staff olan bir user ın token ı ile get ve post isteği attığımızda çalıştı.
- Normalde default gelen böyle bir permission policy yok ama bunu kendimiz yazdık. Bu şekilde view seviyesinde permissions lar yazılabilir. Eğer permission izin vermesini istiyorsanız true dönmesi lazım, izin vermesini istemiyorsanız false dönmesi lazım.


- Son olarak object seviyesinde bir permissions yazalım;
- Bunun için ne yapmamız gerekiyordu? 
  .has_object_permission(self, request, view, obj)
  ile override etmemiz gerekiyordu.

- Biz neye bakacaktık? modelimizdeki her bir objenin yani burada her bir student oluyor, her bir student ın create edenine bakacağız, o student ın create edenini login olmuş olan user ise o student üzernde değişiklik yapmasına izin vereceğiz ama create edeni değilse değişiklik yapamazsın anlamına gelen bir permission.
- Modelimize yani student_api appimizin models.py ına gidiyoruz, user field ekliyoruz, bu user field User tablomuz ile ForeignKey ile bağlı, yani bir user birden fazla student create edebilir, blank=True null=True ise mevcut tablomuzdaki verilerim için bize sıkıntı çıkarmasın diye ekliyoruz.
  
  from django.contrib.auth.models import User

  user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

student_api <models.py> ->

```py
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    number = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return f"{self.last_name} {self.first_name}"
```


```bash
- py manage.py makemigrations
- py manage.py migrate
```

- şimdi student_api -> views.py da student ların create edildiği view e gidiyoruz,  permission_classes ını IsAuthenticated yapıyoruz, ki diğer login olmuş kullanıcılar da create yapabilsinler, 
- Ardından;
  
  def perform_create(self, serializer):
    serializer.save(user=self.request.user)
  
  yazıyoruz, yani o an login olmuş user kim ise onu student ın yeni oluşturduğumuz student field ına ekliyoruz.

- artık student create edebiliriz, postmanden create ediyoruz, etti, admin panelden student lara bakıyoruz, evet kaydettiğimiz student ın user ını da görüyoruz.
- Şimdi yazacağımız permission ile bu objenin update delete işlemlerini sadece bu objenin create edeni kim ise ona izin vereceğiz.
- Tekrar permissions lara gidiyoruz, permissions.BasePermission dan inherit ederek yeni bir class yazıyoruz, bu objenin create edeni değilsen sadece readonly yapabilirsin.
  
  class IsAddedByUserorReadOnly(permissions.BasePermission):

  def has_object_permission(self, request, view, obj)


  bakın burada object de var, artık object i de yakalayıp burada kullanabiliyoruz. has_permission da object yoktu ama  has_object_permission da object i de argüman olarak geldiği için object i de yakalayabiliyoruz.

        if request.method == permissions.SAFE_METHODS:
            return True
        else:
            return obj.user == request.user or request.user.is_staff

yani student objesinin create edeni login olmuş user ise veya admin ise  true döndürür ve SAFE_METHODS lardan olmayan UPDATE DELETE methodlarında true döndürür.

student_api <permissions.py> ->

```py

class IsAddedByUserorReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.user == request.user or request.user.is_staff

```

- Bu yazdığımız permissions ı alıp şimdi student_api -> views.py da student ların create edildiği view e gidiyoruz,  permission ımızı import ediyoruz, 

  from .permissions import IsAdminorReadOnly, IsAddedByUserorReadOnly

- Biz bir obje üzerinde işlem yapacağımız için o view imiz olan StudentOperations view imizin permission_classes ına yeni yazdığımız permissions ı ekliyoruz.

  class StudentOperations(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [IsAddedByUserorReadOnly]



student_api <views.py> ->

```py
class StudentOperations(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [IsAddedByUserorReadOnly]
```

- test ediyoruz, admin ile put yapabildik, ama başka bir user ile yani objeyi create eden user dışında bir user ile put yapmaya izin vermedi. sadece create eden user ve admin objede put yapmaya izin verdi.

- permission ların dibine kadar indik.
