umur = 25

print(type(umur))

saldo = 3e8
print(type(saldo))

nama = 'jabez chrisopras ferdinand'

puisi = """""
nama saya jabez
umur saya 20 tahun
saya mahasiswa teknik informatika"""

print(type(puisi))

p = nama == puisi

print(p)

x = y = z = 0

print(x)
print(y)
print(z)

a ,b , c = 1 , 2 , 3

print(a)
nama, age = 'jabez', 18
print(nama, age)

nama = input('masukan nama anda :')
print('hallo', nama)
truefalse = bool(input('masukan nama anda :'))
print(truefalse)
nama = 'jabez'
age = 18
status = 'mahasiswa'
string = ('nama saya',nama,'umur saya',age,'status saya',status)
print(len(string))
print(string[0:4])

nama = 'jabez'
print(nama[-1:5])

nama = 'jabez \\ jordan \\ jobel'
print(nama)
kalimat = 'dia berkata \" halo \" kepada saya'
print(kalimat)
kalimat1 = '\'halo\' saya jabez'
print(kalimat1)

nama = 'jabez'
print(f'nama saya {nama.upper()}')

x = 10

x + 5 

x - 3
print(x)

nama = 'jabez'
print(nama * 2)
print('-' * 80 )

nama = 'chrisopras ferdinand'

if 'jabez' in nama :
    print('jabez ditemukan')
else:
    print('jabez tidak di temukan')

umur = int(input('masukan umur anda :'))
sim = input('punya sim (ya/no)')

if umur >= 17 and sim == 'ya':
    print('kamu boleh menggendarai motor')
elif umur >= 17 or sim == 'ya':
    print('kamu boleh menggandarai motor')
else:
    print('kamu tidak boleh menggendarai')


nama = input('masukan nama anda :')

match nama:
    case 'jabez' | 'jordan' | 'jobel':
        print('hallo anak pak novel ')
    case _:
        print('hallo nama kamu tidak ada di kk')
angka = int(input('masukan angka'))
hasil = 'positif' if angka > 0 else 'negatif'
print(hasil)

for i in range(1,5):
    print('hello jabez')

for i in range(10,0,-1):
    print(i)

nama = 'jabez', 'jordan', 'jobel'

for indeks in nama:
    print(indeks[0])
percobaan = 0
dicoba = 5
while percobaan < dicoba :
    password = int(input('masukan password :'))
    if password != 12345:
        print(f'password salah coba lagi sisah percobaan kamu {dicoba - percobaan}')
        percobaan += 1
    else:
        print('jawaban kamu benar')
        break
else:
 print('batas percobaan kamu habis')


for i in range(10):
    if i % 2 == 0:
     print(i)


while nama != 'jabez':
    if nama != 'jabez':
        nama = input('masukan nama anda :')
        print('nama salah coba lagi')
print('nama benar')



kalimat = input('masukan kalimat :')
katadicari = input('masukan kata in kalimat :')
for i in kalimat:
 if katadicari in kalimat:
        print(katadicari,'di temukan dikalimat', kalimat)
        break
        
else:
    print('kata tidak di temukan di kalimat')

for i in range(1,11):
    for j in range(1,11):
        hasil = i * j
        print(f'{i} * {j} = {hasil}')
    print('=' * 10)

list = []
nama = input('masukan nama :')
data = nama.split(',')
list.append(data)
data = nama.strip('').split(' ')
print(data)
for i  in data:
    print('-',i)
 
list_buah = []
buah = input('masukan list buah :')
data_buah = buah.strip().split(' ')
list_buah.append(data_buah)

for i in list_buah:
    print('-',i)
    print(len(i))

biodata = {
    'nama' : 'jabez',
    'umur' : 12,
    'status' : 'mahasiswa'
}
print(biodata)
for key, values in biodata.items():
    print(key,'=',values)

print(biodata.values())
print(biodata.keys())

biodata['nama'] = 'jabez chrisopras ferdinand'
print(biodata)
del biodata['umur']
for key, values in biodata.items():
    print(key,'=',values)

set = {'jeruk', 'apel'}
list = ['jeruk','apel']
set.add('mangga')
set.add('mangga')
set.add('anggur')
for e in set:
    print(e)

list.append('mangga')
list.append('mangga')
list.insert(0, 'mangga')

print(list)

def menu(nama,umur):
    print('nama saya :', nama)
    print('umur saya :', umur)

nama = input('masukan nama :').title()
umur = int(input('masukan umur anda :'))
menu(nama,umur)

def Hasil(panjang=0,lebar=2):
    luas = panjang * lebar
    return luas

hasil = Hasil(int,5)
print(hasil + 10)

def biodata(nama,sapaan= 'hallo'):
    return f'{sapaan} nama saya {nama} '

hasil = biodata('jabez',)
print(hasil)

def keyword(nama,umur,kota):
    return f'nama : {nama} umur : {umur} kota : {kota}'

hasil = keyword(kota='bandung',nama='jabez',umur=30)
print(hasil)


def Umur(nama,umur,kota='jakarta',status='single'):
    print(f"""
    === NAMA {(nama).upper()} ===
    umur = {umur}
    kota = {kota}
    status = {status}""")
    print('=' * 50)

Umur('jabez',18)
Umur('jobel',13,kota= 'surabaya')
Umur('jordan',21,kota= 'Semarang',status= 'not availabel')

nama_global = 'jabez'

def Nama():
    print(f'nama global {nama_global}')
def UbahNama():
    global nama_global
    nama_global ='jordan'
Nama()   
UbahNama()
Nama()

def List(*list):
    return list

hasil = List(1,2,3,4,5,6,'jabez')

for i in hasil:
    print('-',i)

def Dict(**dict):
    return dict
hasil = Dict(nama='jabez',kota='semarang',umur=18)

for key,value in hasil.items():
    print(key, '=', value)

number = float(input('masukan angka :'))
if number % 2 == 0 :
    print(f'{number} adalah bilangan genap')


nilai = {
    'andi': [90,80,70],
    'budi' : [80,90,70],
    'sinta': [70,80,90]
}

siswa = nilai['andi']
for i in siswa :
    avg = sum(siswa) / len(siswa)
    print(avg)