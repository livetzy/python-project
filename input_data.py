list_data_mahasiswa = []
class Mahasiswa():
    def __init__(self,nama,nim,prodi):
        self.nama = nama
        self.nim = nim
        self.prodi = prodi

    def data(self):
        if not list_data_mahasiswa:
            return "Data Mahasiswa Kosong"
        else:    
            return self.tambah_data(list_data_mahasiswa)
    
    def tambah_data(self,n):
        laporan = ""
        for data in n:
         laporan += F"""
    NAMA = {data[0]}
    NIM = {data[1]}
    PRODI = {data[2]}
                """
        return laporan
    
    def ubah_data(self, nim, nama_baru, nim_baru, prodi_baru):
        for data in list_data_mahasiswa:
                if nim == data[1]:
                    data[0] = nama_baru
                    data[1] = nim_baru
                    data[2] = prodi_baru

                    return "Data Berhasil Di Ubah"
                
        return "Data Tidak Sesuai"

    def hapus_data(self,nim):
        for data in list_data_mahasiswa:
           if nim == data[1] and nim in data:
               list_data_mahasiswa.remove(data)

               return "Data Berhasil Di Hapus"
         
        return 'data mahasiswa kosong'
    
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
        while True:
            print('INPUT DATA MAHASISWA')
            nama = input('Masukkan nama: ').upper()
            nim = input('Masukkan NIM: ').upper()
            prodi = input('Masukkan prodi: ').upper()
            print('Data berhasil ditambahkan!')
            data_baru = f'{nama},{nim},{prodi}\n'
            mahasiswa = data_baru.strip().split(',')
            list_data_mahasiswa.append(mahasiswa)

            lanjutan = input('ingin menambahkan data lagi? (ya/tidak):')
            if lanjutan.lower() != 'ya' :
                print('terimakasih telah menambahkan data')
                break

    def tampilkan_data(self):
        print('Data Mahasiswa:')
        print(self.data())
        input('Tekan Enter untuk kembali ke menu...')

    def keluar(self):
        print('Terima kasih telah menggunakan program ini.')
        exit()

    def run_ubah_data(self):
        nim_lama = input('Masukkan NIM untuk mengubah data: ').upper()

        for data in list_data_mahasiswa: 
            if nim_lama == data[1]: 
                print('ubah data mahasiswa') 
                nama_baru = input('Masukkan nama baru: ').upper()
                nim_baru = input('Masukkan NIM baru: ').upper()
                prodi_baru = input('Masukkan prodi baru: ').upper()
                data_baru = self.ubah_data(nim_lama ,nama_baru, nim_baru, prodi_baru)
                print('Data berhasil diubah!')
                print(data_baru)
                return
            
        else:
            print("Nim Tidak Di Temukan Di Dalam Data")

    def run_hapus_data(self):
            for data in list_data_mahasiswa:
                while True:
                    nim = input('Masukkan NIM untuk menghapus data: ').upper()
                    if nim == data[1]:
                        print('hapus data mahasiswa :')
                        print(self.hapus_data(nim))
                        print(f'Data {data[0]} berhasil dihapus!')

                        lanjutan = input('ingin menghapus data lagi? (ya/tidak): ')
                        if lanjutan.lower() != 'ya':
                            print('sampai jumpa, terimakasih telah menggunakan program ini')
                        
                    else:
                        print('NIM tidak sesuai, data tidak dapat dihapus.')
                        break

list_data_dosen = []
class Dosen():
    def __init__(self,nama_dosen,study,nid):
        self.nama_dosen = nama_dosen
        self.study = study
        self.nid = nid 

    def data_dosen(self):
        if not list_data_dosen:
            return 'Data Dosen Kosong'  
        else:
            return self.tampilan_data_dosen(list_data_dosen)
            
    def tampilan_data_dosen(self,n) :
        laporan = ""
        for data in n:
         laporan += f"""
Nama : {data[0]}
Study : {data[1]}
Nid : {data[2]}\n"""   
         
        return laporan

    def ubah_data_dosen(self,nim_lama,nama_baru,Study_baru,Nid_Baru):
        for data in list_data_dosen:
            if nim_lama == data[2]: 
                data[0] = nama_baru
                data[1] = Study_baru
                data[2] = Nid_Baru
                return "Data Berhasil DI Ubah"

        return "Data Tidak Berhasil Di Ubah"
                     
    def hapus_data_dosen(self, nid):
        for data in list_data_dosen:
            if nid == data[2] and nid in data :
                list_data_dosen.remove(data)

                return "Data Berhasil Di Hapus"
            
        return "Data Tidak Berhasil Di Hapus"
        
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
                self.run_hapus_data_dosen()
            elif pilihan == 4 :
                self.keluar()
            
    def run_tambah_data_dosen(self):
        while True :
            print('INPUT DATA DOSEN')
            nama_dosen = input('Masukkan nama: ').upper()
            study = input('Masukkan study: ').upper()
            nid = input('Masukkan nid: ').upper()
            data_dosen = f'{nama_dosen},{study},{nid}\n'
            data = data_dosen.strip().split(',')
            print('Data berhasil ditambahkan!') 
            list_data_dosen.append(data)
            lanjutan = input('ingin memasukan data lagi (ya/no) ? :')

            if lanjutan != 'ya' :
             print('terimakasih telah menginput data')
             break

    def tampilkan_data_dosen(self):
        print('Data Dosen')
        print(self.data_dosen())
        input('Tekan Enter untuk kembali ke menu...')

    def keluar(self):
        print('Terima kasih telah menggunakan program ini.')
        exit()

    def run_ubah_data_dosen(self):
        nid_lama = input('Masukkan NId untuk mengubah data: ').upper()

        for data in list_data_dosen:
            if nid_lama == data[2]:
                print('ubah data dosen') 
                nama_baru = input('Masukkan nama baru: ').upper()
                study_baru = input('Masukan Study Baru: ').upper()
                nid_baru = input('Masukkan Nid baru: ').upper()
                data_baru_dosen = self.ubah_data_dosen(nid_lama ,nama_baru , study_baru , nid_baru)
                print('Data dosen berhasil diubah!')      
                print(data_baru_dosen)
                return
            
        else:
            print('NID tidak sesuai, data tidak dapat diubah.')

    def run_hapus_data_dosen(self):
        for data in list_data_dosen :
            while True:
                nid = input('masukan nid untuk mengubah data :').upper()
                if nid == data[2] :
                    print(self.hapus_data_dosen(nid))
                    print(f'data {data[0]} berhasil di hapus')

                    lanjutan = input('ingin menghapus data lagi ? (ya/no) :')
                    if lanjutan != 'ya' :
                        break
                else:
                    print('nama tidak sesuai')

class MenuAplikasi():
    
    def Menu(self):
        print('SELAMAT DATANG DI PROGRAM INPUT DATA')
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
