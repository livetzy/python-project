import random
def menu():
    data = random.randint(1000,2000)
    print(f'password anda adalah : {data}')
    password = int(input('masukan password anda :'))

    if password == data :
        print('selamat datang bos')
        print('ingin menambahkan menu apa saat ini:')
        print('1.makanan')
        print('2.minuman')
        print('3.snack')
        print('4.keluar')
        pilihan = float(input('masukan pilihan anda :'))

        if pilihan == 1 :
            tambah_menu_makanan()
        elif pilihan == 2 :
            tambah_menu_minuman()
        elif pilihan == 3 :
            tambah_menu_snack()
        elif pilihan == 4 :
            print('Terimakasih telah menggunakan sistem ini')
            exit()
        else:
            print('input pilihan tidak valid')
    else:
        print('password salah')
        exit()

def tambah_menu_makanan():
    with open('menu_makanan.txt', 'w') as file :
        while True :
            makanan = input('masukan nama menu makanan :').upper()
            data = f'{makanan}\n'
            file.write(data)
            print('menu makanan berhasil di simpan')
            lanjutan = input('ingin menambah menu makanan lagi ? :')
            if lanjutan != 'ya' :
                print('terimakasih telah menambahkkan menu makanan')
                break
def tambah_menu_minuman():
    with open('menu_minuman.txt', 'w') as file :
        while True :
            minuman = input('masukan nama menu minuman :').upper()
            data = f'{minuman}\n'
            file.write(data)
            print('menu minuman berhasil di simpan')
            lanjutan = input('ingin menambah menu minuman lagi ? :')
            if lanjutan != 'ya' :
                print('terimakasih telah menambahkkan menu minuman')
                break
def tambah_menu_snack():
    with open('menu_snack.txt', 'w') as file :
        while True :
            snack = input('masukan nama menu snack :').upper()
            data = f'{snack}\n'
            file.write(data)
            print('menu snack berhasil di simpan')
            lanjutan = input('ingin menambah menu snack lagi ? :')
            if lanjutan != 'ya' :
                print('terimakasih telah menambahkkan menu snack')
                break

menu()