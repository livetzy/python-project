
class Operator():

    def pertambahan(self,a,b):
        return a + b
    def pengkurangan(self,a,b):
        return a + b
    def perkalian(self,a,b):
        return a * b
    def pembagian(self,a,b):
        if b != 0 :
            return a / b
        else :
            raise ZeroDivisionError ('input tidak bisa 0')
    def modulo(self,a,b):
        return a % b

    def biodata(nama,umur,status):
        data = f'nama : {nama}\numur : {umur}\nstatus : {status}'.upper()
        return data
    

class Kampus():
        def __init__(self,nama,akredasi,wilayah):
            self.nama = nama
            self.akredasi = akredasi
            self.wilayah = wilayah

        def data(self):
            return f'nama kampus : {self.nama}\nakredasi kampus : {self.akredasi}\nwilayah : {(self.wilayah)} '.upper()

        def biodata_mahasiswa(self,nama,nim,prodi,ipk):
            return f'kampus = {self.nama}\nnama mahasiswa : {nama}\nnim mahasiswa : {nim}\nprodi mahasiswa : {prodi}\nIPK : {ipk} '.upper()






