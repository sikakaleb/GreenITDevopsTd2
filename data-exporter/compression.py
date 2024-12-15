import gzip

# Compression du fichier nettoyé
with open('../data/meteo_nettoyee.json', 'rb') as file_in:
    with gzip.open('meteo_nettoyee.json.gz', 'wb') as file_out:
        file_out.writelines(file_in)

print("Fichier compressé : 'meteo_nettoyee.json.gz'.")
