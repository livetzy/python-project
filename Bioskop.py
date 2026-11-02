total_penonton = 0
diskon = 0
def menu():
    global diskon , total_penonton
    print("selamat Datang di bioskop".capitalize())
    try:
        penonton = int(input("masukan jumlah penonton : ").capitalize())
        total_penonton += penonton
        if penonton < 5 :
            diskon += 0
        elif penonton >= 5 and penonton < 10 : 
            diskon += 0.20
        elif penonton >= 10 :
            diskon += 0.30
    except ValueError:
            print("Input tidak valid. input harus berupa angka.")
            total_penonton += penonton

    while True:

        print("1. beli tiket".capitalize())
        print("2. beli snack".capitalize())
        print("3. pesanan".capitalize())
        print("4. keluar".capitalize())
        try:
            pilihan = int(input("Masukan Pilihan Anda : "))
        except ValueError:
            print("input tidak valid. input harus berupa angka.")
            continue

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
    print("selamat datang si daftar film".capitalize())

    kategori = ["Horor","Drama dan Keluarga","Aksi dan Petualangan","Thriller, Kriminal, dan Misteri","Animasi dan Fantasi"]

    for indeks, nama in enumerate(kategori, start=1): 
        print(f" {indeks}. {nama}")

    pilihan = int(input("masukan pilihan anda : ").capitalize())

    if 1 <= pilihan <= len(kategori):
        pilihan = kategori[pilihan - 1]

    sedang_baca = False

    with open ("Daftar_film.txt", "r", encoding="utf-8") as file:

        for baris in file :
            baris = baris.strip()

            if not baris:
                continue

            if not baris.startswith("-"):
                sedang_baca = baris.lower() == pilihan.lower()

                if sedang_baca:
                    print(f"\n{baris}")

                continue

            if sedang_baca:
                print(baris)

        film = input("masukan film yang ingin anda tonton : ".capitalize())
        pilihan_film.append(film + "\n")
    

pilihan_snack = []
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

    while True :

      snack = input("Masukan snack yang anda inginkan : ".capitalize())
      lanjutan = input("ingin memesan snack lagi? (y/n) : ")
      pilihan_snack.append(snack)
      
      if lanjutan != 'y' :
          print("terimakasih telah memesan")
          break
      


def pesanan():
     print(f'Total Penonton : {total_penonton}'.capitalize())
     print(f"diskon yang di peroleh : {diskon}".capitalize())
     print()
     print("daftar film yang di pesan :".title())
     for indeks, film in enumerate(pilihan_film, start=1):
         print(f"{indeks}. {film}")
     print('daftar snack yang di pesan :'.title())
     for indeks, menu in enumerate(pilihan_snack,start=1):
        print(f'{indeks}. {menu}')
     print()
                    
menu()
