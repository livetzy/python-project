class Mahasiswa():
    def __init__(self,nama,nim,prodi):
        self.nama = nama
        self.nim = nim
        self.prodi = prodi

    def data(self):
        return (f'nama = {self.nama}\nnim = {self.nim}\nprodi = {self.prodi}')
    
    def tambah_data(self, nama, nim, prodi):
        self.nama = nama
        self.nim = nim
        self.prodi = prodi
        data_mhs = self.data()
        return data_mhs
    
    def ubah_data(self, nama_baru, nim_baru, prodi_baru):
        self.nama = nama_baru
        self.nim = nim_baru
        self.prodi = prodi_baru
        data = self.data()
        return data
    
    def hapus_data(self):
        for attr in ['nama', 'nim', 'prodi']:
            setattr(self, attr, None)

    def menu(self):
         while True:
            print('MENU DATA MAHASISWA')
            print('1. Tambah Data')
            print('2. Tampilkan Data')
            print('3. Ubah Data')
            print('4. Hapus Data')
            print('5. Keluar')
            pilihan = int(input('Masukkan pilihan: '))

            if pilihan == 1:
                self.run_tambah_data()
            elif pilihan == 2:
                self.tampilkan_data()
            elif pilihan == 3:  
                self.run_ubah_data()
            elif pilihan == 4:
                self.run_hapus_data()
            elif pilihan == 5:
                self.keluar()


    def run_tambah_data(self):
        print('INPUT DATA MAHASISWA')
        nama = input('Masukkan nama: ')
        nim = input('Masukkan NIM: ')
        prodi = input('Masukkan prodi: ')
        data_baru = self.tambah_data(nama, nim, prodi)
        print(data_baru)
        print('Data berhasil ditambahkan!')

    def tampilkan_data(self):
        print('Data Mahasiswa:')
        print(self.data())

        input('Tekan Enter untuk kembali ke menu...')

    def keluar(self):
        print('Terima kasih telah menggunakan program ini.')
        exit()

    def run_ubah_data(self):
        nim = input('Masukkan NIM untuk mengubah data: ')
        if nim != self.nim:
            print('NIM tidak sesuai, data tidak dapat diubah.')
        else:
            print('ubah data mahasiswa') 
            nama_baru = input('Masukkan nama baru: ') 
            nim_baru = input('Masukkan NIM baru: ') 
            prodi_baru = input('Masukkan prodi baru: ')
            data_baru = self.ubah_data(nama_baru, nim_baru, prodi_baru)
            print('Data berhasil diubah!')
            return data_baru

    def run_hapus_data(self):
        percobaan = 0
        dicoba = 3
        while percobaan < dicoba:
            nim = input('Masukkan NIM untuk menghapus data: ')
            if nim != self.nim:
                percobaan += 1
                print(f'NIM tidak sesuai, percobaan tersisa {dicoba - percobaan} kali.')
            else:
                print('hapus data mahasiswa :')
                self.hapus_data()
                print('Data berhasil dihapus!')
                break
        else:
            print('Percobaan habis, data tidak dapat dihapus.')
            
        
class Dosen():
    def __init__(self,nama_dosen,study,nid):
        self.nama_dosen = nama_dosen
        self.study = study
        self.nid = nid 

    def data_dosen(self):
        return f"NAMA: {self.nama_dosen}\nSTUDY: {self.study}\nNID: {self.nid}\n"
    
    def tambah_data_dosen(self,nama,study,nid):
        self.nama_dosen = nama
        self.study = study
        self.nid = nid
        data_dosen = Dosen(self.nama_dosen, self.study , self.nid)
        return data_dosen
    
    def hapus_data_dosen(self):
        for attr in ['NAMA' , 'STUDY' , 'NID']:
            setattr(self, attr, None)
        
    def menu_dosen(self):
        while True:
            print('== DATA DOSEN ==')
            print('0. tambah data')
            print('1. Tampilkan Data')
            print('2. Ubah Data')
            print('3. Hapus Data')
            print('4. Keluar')
            pilihan = int(input('Masukkan pilihan: '))

            if pilihan == 0 :
                self.run_tambah_data_dosen()
            elif pilihan == 1 :
                self.tampilkan_data_dosen()
            elif pilihan == 2 :
                self.run_ubah_data_dosen()
            elif pilihan == 3 :
                self.hapus_data_dosen()
            elif pilihan == 4 :
                self.keluar()
        
            
    def run_tambah_data_dosen(self):
        print('INPUT DATA DOSEN')
        nama_dosen = input('Masukkan nama: ').upper()
        study = input('Masukkan study: ').upper()
        nid = input('Masukkan nid: ')
        data_dosen = self.tambah_data_dosen(nama_dosen, study, nid)
        print(data_dosen)
        print('Data berhasil ditambahkan!')

    def tampilkan_data_dosen(self):
        print('Data Mahasiswa:')
        print(self.data_dosen())

        input('Tekan Enter untuk kembali ke menu...')

    def keluar(self):
        print('Terima kasih telah menggunakan program ini.')
        exit()

    def run_ubah_data_dosen(self):
        nid = input('Masukkan NId untuk mengubah data: ')
        if nid != self.nid:
            print('NID tidak sesuai, data tidak dapat diubah.')
        else:
            print('ubah data dosen') 
            nama_baru = input('Masukkan nama baru: ') 
            study_baru = input('Masukkan NIM baru: ') 
            nid_baru = input('Masukkan prodi baru: ')
            data_baru_dosen = self.tambah_data_dosen(nama_baru, study_baru, nid_baru)
            print(data_baru_dosen)
            print('Data dosen berhasil diubah!')
    
    def hapus_data_dosen(self):
        nama = input('masukan nama mahasiswa untuk menghapus data :')
        if nama == self.nama_dosen :
            self.hapus_data_dosen()
            print(f'data {nama} berhasil di hapus')
        else:
            print('nama tidak sesuai')



class MenuAplikasi():
    
    def Menu(self):
        print('SELAMAT DATANG DI PROGRAM DATA MAHASISWA')
        print('MASUKAN PILIHAN ANDA:')
        print('1. masuk ke menu mahasiswa')
        print('2. masuk ke menu dosen')
        pilihan = int(input('Masukkan pilihan: '))

        if pilihan == 1:
            mahasiswa = Mahasiswa(nama='', nim='', prodi='')
            mahasiswa.menu()
        elif pilihan == 2:
            dosen = Dosen(nama_dosen='', study='', nid='')
            dosen.menu_dosen()

if __name__ == '__main__':
    mahasiswa = MenuAplikasi()
    mahasiswa.Menu()
