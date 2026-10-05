list_minuman = [] 
list_makanan = []
list_snack = []
class Menu:
    def __init__(self,makanan,minuman):
        self.makanan = makanan
        self.minuman = minuman

    def pesanan(self):
         print('== PESANAN ANDA =='.upper())
         print('-' * 40)
         print('== pesanan makanan anda =='.upper())
         for menu in list_makanan:
          print('-',menu)
          print('-' * 40)
  
         print('== pesanan minuman anda =='.upper())
         for menu in list_minuman:
            print('-',menu)
         print('-' * 40)

         print('== pesanan snack anda == '.upper())
         for menu in list_snack:
             print('-',menu)
         print('-' * 40)

    def Pilihan(self):
        while True:
                print('SELAMAT DATANG DI MENU')
                print('SILAHKAN PILIH MENU ANDA')
                print('1. Menu Makanan')
                print('2. Menu Minuman')
                print('3. Menu snack')
                print('4. cek pesanan')
                print('5. batalkan pesanan yang tidak jadi di pesan')
                print('6. keluar dari aplikasi')
                pilihan = int(input('Masukan Pilihan Anda :'))

                if pilihan == 1 :
                    self.menu_makanan() 
                elif pilihan == 2 :
                    self.menu_minuman()
                elif pilihan == 3:
                    self.menu_snack()
                elif pilihan == 4:
                    self.pesanan()
                elif pilihan == 5 :
                    self.batalkan_pesanan()
                elif pilihan == 6 :
                    print('terimakasih telah berkunjung ke toko kami'.upper())
                    exit()

    def menu_makanan(self):
        daftar_makanan = []
        print('selamat Datang Di Menu Makanan'.upper())
        print('--- Menu Makanan ---'.upper() )
        with open ('menu_makanan.txt', 'r') as file :
            for data in file :
                menu = data.strip().upper()
                print('-', menu)
                daftar_makanan.append(menu)
            makanan = input('masukan pesanan anda :').upper()
            if makanan in daftar_makanan :
                print(f'{makanan} berhasil di pesan')
                list_makanan.append(makanan)
            else:
                print(f'{makanan} tidak terdapat di daftar menu')

            lanjutan = input('ingin memesan lagi? (ya/tidak) :')
            if lanjutan == 'ya':
                self.menu_makanan()
            else:
                print('\"terimakasih telah memesan\"\n\"mohon menunggu pesanannya\"')

    def menu_minuman(self):
        daftar_minuman = []
        print('Selamat Datang Di Menu Minuman')
        print('--- Menu Minuman ---')
        with open ('menu_minuman.txt','r') as file :
            for data in file:
                menu = data.strip().upper()
                print('-', menu)
                daftar_minuman.append(menu)
            minuman = input('masukan pesanan anda :').upper()

            if minuman in daftar_minuman:
                print(f'{minuman} berhasil di pesan ')
                list_minuman.append(minuman)
            else:
                print('pesanan tidak ada di daftar menu')
            lanjutan = input('ingin melanjutkan pemesanan? (ya/tidak) :')
            if lanjutan == 'ya':
                self.menu_minuman()
            else:
                print('terimakasih telah memesan\nmohon menunggu pesanan anda')
    
    def menu_snack(self):
        daftar_snack = []
        print('=== SELAMAT DATANG DI DAFTAR SNACK ===')
        print('ini adalah daftar menu snack kami')
        with open ('menu_snack.txt', 'r') as file :
            for menu in file :
                data = menu.strip().upper()
                print('-',data)
                daftar_snack.append(data)
            snack = input('masukan pesanan anda :').upper()

            if snack in daftar_snack :
                print(f'{snack} di tambahkan ke pesanan')
                list_snack.append(snack)
            else:
                print('pesanan tidak terdapat di dalam menu')
            lanjutan = input('ingin melanjutkan pesanan ? (ya/tidak):')
            if lanjutan == 'ya' :
                self.menu_snack()
            else:
                print('terimakasih telah memesan\nmohon menungggu pesanan anda ')

    def batalkan_pesanan(self):
        print('- makanan\n- minuman\n- snack'.upper())
        pilihan = input('ingin membatalkan pesanan menu apa :')

        if pilihan == 'makanan':
                 print('pesanan anda :')
                 for i in list_makanan:
                     print('-', i)
                 else:
                     print('anda belum memesan menu makanan')
                 makanan = input('masukan menu makanan yang ingin di hapus :').upper()
                 for i in list_makanan:
                        if makanan  == i :
                            list_makanan.remove(makanan)
                            print('pesanan berhasil dibatalkan')
                    
        elif pilihan == 'minuman' :
            print('pesanan anda :')
            for nilai in list_minuman :
                print('pesanan anda')
                print('-', nilai)
            else:
                print('anda belum memesan menu minuman')
            minuman = input('masukan menu minuman yang ingin di hapus :').upper()
            for i in list_minuman:
                if minuman == i :
                    list_minuman.remove(minuman)
                    print('pesanan berhasil di batalkan')

        elif pilihan == 'snack' :
            print('pesanan anda :')
            for nilai in list_snack :
                print('-', nilai)
            else:
                print('anda belum memesan menu snack')
            snack = input('masukan menu snack yang ingin di hapus :').upper()
            for i in list_snack :
                if snack == i :
                    list_snack.remove(snack)
                    print('pesanan menu snack berhasil di batalkan :')

if __name__ == '__main__':
    mahasiswa = Menu(makanan=list_makanan, minuman = list_minuman)
    mahasiswa.Pilihan()
        


