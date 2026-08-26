class Mahasiswa():
    def __init__(self,nama,nim,jurusan):
        self.nama = nama
        self.nim = nim
        self.jurusan = jurusan 

    def data(self,nama,nim,jurusan):
        biodata = f"nama : {nama}\nnim : {nim}\njurusan : {jurusan}\nSenang Berkenalan Dengan Anda"

        return biodata

    def input(self):
        nama = input('masukan nama anda :')
        nim = input('masukan nim anda :')
        jurusan = input('masukan jurusan anda :')
        nilai = self.data(nama, nim , jurusan)
        print(nilai)

mahasiswa = Mahasiswa(nama= '', nim= '', jurusan= '')
mahasiswa.input()


class Buku:
    def __init__(self, judul , penulis , tahun):
        self.judul = judul
        self.penulis = penulis
        self.tahun = tahun


    def info(self,judul,penulis,tahun):
         return f'Judul : {judul}\nPenulis : {penulis}\nTahun : {tahun}'

    def input(self):
        Judul = input('masukan judul buku anda :')
        penulis = input('masukan nama penulis :')
        tahun = input('masukan Tahun Penulisan buku :')
        nilai = self.info(Judul , penulis , tahun)
        print(nilai)

if __name__ == "__main__":
    buku = Buku(judul= 'judul', penulis='', tahun= '')
    buku.input()



