penonton = 0
diskon = 0
def menu():
    global diskon , penonton
    print("selamat Datang di bioskop".capitalize())
    penonton = int(input("masukan jumlah penonton : ").capitalize())
    penonton += penonton
    if penonton < 5 :
        diskon += 0
    elif penonton >= 5 and penonton < 10 : 
        diskon += 0.20
    elif penonton >= 10 :
        diskon += 0.30

    while True:

        print("1. beli tiket".capitalize())
        print("2. beli snack".capitalize())
        print("3. pesanan".capitalize())
        print("4. keluar".capitalize())
        pilihan = int(input("Masukan Pilihan Anda : "))

        if pilihan == 1 :
            daftar_film()
        elif pilihan == 2 :
            snack()
        elif pilihan == 3 :
            pesanan()
        elif pilihan == 4 :
            print("Terimakasih Telah Memesan\nselamat menikmati film anda")
            exit()
        else:
            print("Input anda tidak valid")

pilihan_film = []
def daftar_film():
      print("silahkan pilih film yang ingin anda tonton".capitalize())
      with open ("Daftar_film.txt" , "r") as file:
            for i in file:
                data = i.strip()
                print( "-" , data)
              
            print("Silahkan Pilih Film Anda :".capitalize())
            film = input("Masukan Judul FIlm :").capitalize()
            pilihan_film.append(film)
            print("Terimakasih Telah memesan tiket".capitalize())
            print("silahkan cek kembali pesanan anda di bagian \"Pesanan\"".capitalize())


def snack():
    kategori = ["Bakery dan Pastry", "Snack Gurih", "Roti dan Makanan Ringan", "Dessert"]

    print("selamat datang di daftar snack".capitalize())
    print('silahkan pesen snack yang kalian inginkan!!'.capitalize())

    for indeks, nama in enumerate(kategori, start=1):
        print(f"{indeks}. {nama}")

    menu = int(input("masukan menu yang ingin anda pesan :"))

    if 1 <= menu <= len(kategori):
        menu = kategori[menu - 1]

        sedang_baca = False

        with open("daftar_snack.txt","r", encoding="utf-8") as file:
            for baris in file:
                baris = baris.strip()

                if not baris : 
                    continue

                if not baris.startswith("-"):
                    sedang_baca = baris.lower() == menu.lower()

                    if sedang_baca:
                        print(f"\n{baris}")

                    continue
                
                if sedang_baca:
                    print(baris)
    else:
        print("Pilihan Tidak tersedia")

def pesanan():
     print(f'Total Penonton : {penonton}'.capitalize())
     print(f"diskon yang di peroleh : {diskon}")
     print(f"film yang di pilih : {pilihan_film}")
            

menu()
