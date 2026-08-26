import json

memori = {
    'nama' : 'jabez chrisopras ferdinand',
    'umur' : 18,
    'prodi' : 'teknik informatika'
}


with open('memori.json', 'w') as file :
    json.dump(memori,file,indent=4)
    
print('memori berhasil di simpan')