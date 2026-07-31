list_mahasiswa = []
class Mahasiswa():
    def __init__(self,nama,prodi,ipk,ip) :
        self.nama = nama
        self.prodi = prodi
        self.ipk = ipk

    def data_mahasiswa(self):
        biodata = input('masukan biodadata anda pisahkan setiap point dengan koma(,) :')
        menu = biodata.strip().split(',')
        list_mahasiswa.append(menu)

        for nilai in list_mahasiswa:
         
         return f'nama : {nilai[0]}\nprodi : {nilai[1]}\nipk : {nilai[2]}'

    def menu(self):
       print('1. input data mahasiswa')
       print('2. tampilkan data mahasiswa')
       print('3. keluar dari aplikasi')
       pilihan = input('masukan pilihan anda :')

       if pilihan == '1':
          self.input_data()
       elif pilihan == '2':
          pass
       elif pilihan == '3' :
          pass

    def input_data(self) :
       nama = input('masukan nama mahasiswa :')
       prodi = input('masukan program studi :')
       ipk = input('masukan ipk :')
       menu = Mahasiswa(nama,prodi,ipk)
       



mahasiswa = Mahasiswa(nama= '' , prodi = '' , ipk = '' , ip= list_mahasiswa)
menu = mahasiswa.menu()
print(menu)

