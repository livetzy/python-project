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
