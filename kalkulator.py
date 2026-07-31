def Kalkulator():
    while True:
        hasil = int(input("Masukkan angka pertama: "))

        while True:
            operator  = input("Masukkan operator (+, -, *, /): ")
            if operator == '=':
                print("Hasil akhir:", hasil)
                break
            angka = int(input('masukan angka kedua :'))
            if operator == '+':
                hasil += angka
            elif operator == '-':
                hasil -= angka
            elif operator == '*':
                hasil *= angka
            elif operator == '/':
                if angka != 0:
                    hasil /= angka
                else:
                    print("Error: Pembagian dengan nol tidak diperbolehkan.")
            elif operator == '%':
                hasil %= angka
            elif operator == '|':
                hasil |= angka
            elif operator == '//':
                    hasil //= angka
            elif operator == '^':
                hasil ^= angka
            else:
                print("Operator tidak valid. Silakan masukkan operator yang benar.")

        lanjutan = input("Apakah Anda ingin melanjutkan perhitungan dengan hasil akhir? (y/n): ")
        if lanjutan.lower() != 'y':
            print(('terimakasih telah menggunakan aplikasi ini').upper())
            print(('sampai jumpa').upper())
            break

        

def menu() :
    print('MENU KALKULATOR')
    print('1. Kalkulator')
    print('2. Keluar')
    pilihan = int(input('Masukkan pilihan: '))
    if pilihan == 1:
        Kalkulator()
    elif pilihan == 2:
        print("Terima kasih telah menggunakan kalkulator.")
        exit()
    else:
        print("Pilihan tidak valid. Silakan masukkan pilihan yang benar.")

menu()

# import matematika

# pertambahan = matematika.tambah(5, 2)
# pengurangan = matematika.kurang(6, 3)
# biodata = matematika.biodata('jabez chrisopras ferdinand', 18 , 'mahasiswa').upper()
# pembagian = matematika.pembagian(5,2)

# print(pertambahan)
# print(biodata)
# print(pengurangan)
# print(pembagian)


import matematika

data = matematika.Kampus('jabez','teknik informatika',116).data()
print(data)


nama_mahasiswa = input('masukan nama :')
nim = input('masukan nim mahasiswa :')
ipk = float(input('input ipk :'))
prodi = input('masukan prodi anda :')

data_mahasiswa = matematika.Kampus('universitas dian nuswantoro','unggul','semarang').biodata_mahasiswa(nama=nama_mahasiswa,ipk=ipk,nim=nim,prodi=prodi)
print(data_mahasiswa)

print(matematika.Operator().pembagian(10,2))
print(matematika.Operator().perkalian(18,30))
print(matematika.Operator().pertambahan(10,10))

import modules

# data = modules.data
print(data)

data = modules.biodata('jabez chrisopras ferdinand')
print(data)

