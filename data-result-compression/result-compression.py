import gzip
import lz4.frame
import zstandard as zstd
import time
import os
import shutil


def mesurer_taille_fichier(fichier):
    """
    Retourne la taille du fichier en octets.
    """
    return os.path.getsize(fichier)


def compresser_gzip(fichier_entree, fichier_sortie, niveau=9):
    """
    Compresse un fichier en utilisant gzip.
    """
    debut = time.time()
    with open(fichier_entree, 'rb') as f_in:
        with gzip.open(fichier_sortie, 'wb', compresslevel=niveau) as f_out:
            shutil.copyfileobj(f_in, f_out)
    fin = time.time()
    return fin - debut


def compresser_lz4(fichier_entree, fichier_sortie, niveau=0):
    """
    Compresse un fichier en utilisant lz4.
    """
    debut = time.time()
    with open(fichier_entree, 'rb') as f_in:
        with lz4.frame.open(fichier_sortie, 'wb', compression_level=niveau) as f_out:
            shutil.copyfileobj(f_in, f_out)
    fin = time.time()
    return fin - debut


def compresser_zstd(fichier_entree, fichier_sortie, niveau=1):
    """
    Compresse un fichier en utilisant zstd.
    """
    debut = time.time()
    with open(fichier_entree, 'rb') as f_in:
        with open(fichier_sortie, 'wb') as f_out:
            cctx = zstd.ZstdCompressor(level=niveau)
            f_out.write(cctx.compress(f_in.read()))
    fin = time.time()
    return fin - debut


def analyser_compression(fichier_original, fichier_compresse, temps):
    """
    Analyse les performances de compression.
    """
    taille_originale = mesurer_taille_fichier(fichier_original)
    taille_compressee = mesurer_taille_fichier(fichier_compresse)
    pourcentage_compression = 100 * (1 - taille_compressee / taille_originale)
    ratio_compression_temps = pourcentage_compression / temps
    return taille_compressee, pourcentage_compression, ratio_compression_temps


# Fichiers à tester
fichier_original = "../data/meteo_nettoyee.json"
fichier_grand = "../data/meteo_nettoyee_large.json"

# Création d'un fichier volumineux
def creer_fichier_grand(fichier_source, fichier_destination, multiplicateur):
    with open(fichier_source, 'rb') as src, open(fichier_destination, 'wb') as dest:
        contenu = src.read()
        for _ in range(multiplicateur):
            dest.write(contenu)


creer_fichier_grand(fichier_original, fichier_grand, 50)  # Multiplier la taille

# Test de compression sur les deux fichiers
outils = {
    "gzip": compresser_gzip,
    "lz4": compresser_lz4,
    "zstd": compresser_zstd
}

niveaux = {
    "gzip": [1, 9],
    "lz4": [0, 16],
    "zstd": [1, 22]
}

resultats = []

for fichier_test in [fichier_original, fichier_grand]:
    print(f"\nTests sur le fichier : {fichier_test} ({mesurer_taille_fichier(fichier_test) / 1_000_000:.2f} Mo)")
    for outil, fonction in outils.items():
        for niveau in niveaux[outil]:
            fichier_compresse = f"{fichier_test}.{outil}.lvl{niveau}.compressed"
            temps = fonction(fichier_test, fichier_compresse, niveau)
            taille_compressee, compression, ratio = analyser_compression(fichier_test, fichier_compresse, temps)
            resultats.append({
                "outil": outil,
                "niveau": niveau,
                "fichier": fichier_test,
                "taille_compressee": taille_compressee,
                "compression (%)": compression,
                "temps (s)": temps,
                "ratio (compression/temps)": ratio
            })
            print(f"Outil: {outil}, Niveau: {niveau}, Taille: {taille_compressee / 1_000_000:.2f} Mo, "
                  f"Compression: {compression:.2f}%, Temps: {temps:.2f}s, Ratio: {ratio:.2f}")

# Résultats dans un fichier CSV (facultatif)
import pandas as pd
df = pd.DataFrame(resultats)
df.to_csv("resultats_compression.csv", index=False)
print("\nRésultats enregistrés dans 'resultats_compression.csv'.")
