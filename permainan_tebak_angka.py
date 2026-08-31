import random

angka_random = random.randint(1,10)
angka_random2 = random.randint(1,100)
angka_random3 = random.randint(1,1000)
batas_tebakan = 10
def permainan():
    print('== SELAMAT DATANG DI PERMAINAN TEBAK ANGKA ==')
    print('silahkan pilih range angka yang ingin anda tebak')
    print('1. (1 - 10)')
    print('2. (1 - 100)')
    print('3. (1 - 1000)')

    pilihan = int(input('masukan pilihan anda :'))
    if pilihan == 1 :
        tebak_angka1()
    elif pilihan == 2 :
        tebak_angka2()
    elif pilihan == 3 :
        tebak_angka3()

def tebak_angka1():
    tebakan1 = 0
    print('HALO SELAMAT DATANG DI TEBAK ANGKA')
    print('RANGE TEBAKAN ANDA ADALAH 1 - 10')
    print('Selamat Mencoba Gudluck!!')

    while batas_tebakan > tebakan1 :

        angka_tebakan = int(input('masukan angka tebakan :'))

        if angka_tebakan > angka_random :
            print('tebakan salah , angka tebakan lewat')
            tebakan1 += 1
            print(f'percobaan tersisah {batas_tebakan - tebakan1}')

        if angka_tebakan < angka_random :
            print('tebakan salah , angka  tebakan kurang')
            tebakan1 += 1
            print(f'percobaan tersisah {batas_tebakan - tebakan1}')

        else:
            print(f'YAA angka tebakan anda benar!! {angka_random}')
            break

    else: 
        print(f'batas tebakan anda habis, angka random nya adalah {angka_random}')

def tebak_angka2():
    tebakan2 = 0
    print('HALO SELAMAT DATANG DI PERMAINAN TEBAK ANGKA')
    print('RANGE TEBAKAN ANDA ADALAH 1 - 100')
    print('Selamat Mencoba Gudluck!!')

    while batas_tebakan > tebakan2 :

        angka_tebakan = int(input('masukan angka tebakan anda :'))

        if angka_tebakan > angka_random2 :
            print('tebakan salah , angka terlalu besar')
            tebakan2 += 1
            print(f'sisah percobaan {batas_tebakan - tebakan2}')
            

        if angka_tebakan < angka_random2 :
            print('tebakan salah , angka terlalu kecil')
            tebakan2 += 1
            print(f'sisah percobaan {batas_tebakan - tebakan2}')

        else:
            print(f'YAA angka tebakan anda benar!! {angka_random}')
            break

    else:
        print(f'batas tebakan anda habis, angka random nya adalah {angka_random2}')
            
def tebak_angka3():
    tebakan3 = 0
    print('HALO SELAMAT DATANG DI PERMAINAN TEBAK ANGKA')
    print('RANGE TEBAKAN ANDA ADALAH 1 - 1000')
    print('Selamat Mencoba Gudluck!!')

    while batas_tebakan > tebakan3 :

        angka_tebakan = int(input('masukan angka tebakan anda :'))

        if angka_tebakan > angka_random3 :
            print('tebakan salah , angka terlalu besar')
            tebakan3 += 1
            print(f'sisah percobaan {batas_tebakan - tebakan3}')

        elif angka_tebakan < angka_random3 :
            print('tebakan salah , angka terlalu kecil')
            tebakan3 += 1
            print(f'sisah percobaan {batas_tebakan - tebakan3}')

        else:
            print(f'jawaban kamu benar!!, angka nya {angka_random3}')
            break

    else:
        print(f'batas tebakan anda habis, angka random nya adalah {angka_random3}')

permainan()