
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



#### TokenAuthentication

- BasicAuthentication güvenli değil çünkü her istekte username ve password ü gönderiyoruz (frontend den, react tan, fetch ile, axios ile yapılan her istekte header kısmına username ve password ü tekrar koyuyorsunuz.). Bu güvenlik açısından çok uygun bir durum değil. Bir de BasicAuthentication bizim password ümüzü Base64 e göre kendince şifreliyor ama Base64 çok kolay çözülebilen bir şifreleme yöntemi hemen çözülebiliyor. (base64decode.org da çözdük.) Zaten dokümanında da bu uyarı var, test için kullanın, eğer production için kullanılacaksa API lerinizin https isteklerine yani güvenli isteklere cevap verdiğinden emin olun gibi bir uyarı var. 

- TokenAuthentication -> Bizim için backedimiz bize bir token üretecek, bize o token ı verecek, frontend den yapacağımız her istekte o token ı isteğimizin header kısmına koyacağız ve isteğin kimden geldiğini o token ile anlayacak ve authenticated bir user gibi bize bir permission verecek.

- Bunu nasıl uyguluyoruz?
- Dokümanda yazdığı gibi 'rest_framework.authtoken' paketini INSTALLED_APPS e akliyoruz;

.
.
.
.
