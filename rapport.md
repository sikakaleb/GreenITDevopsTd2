# Rapport : Stratégies de Green I.T. pour la collecte et le stockage des données

## Introduction
L'objectif de ce TD est d'expérimenter différentes stratégies de Green I.T. appliquées à la collecte et au stockage des données.
Nous allons étudier la collecte, la compression, le transfert, et le stockage des données à travers plusieurs étapes.

## I. Collecte des données

### Nettoyage
Les données météorologiques téléchargées ont été nettoyées pour ne conserver que les champs pertinents :
- Températures réelles (`temperature_reelle`).
- Températures ressenties (`temperature_ressentie`).
- Humidité (`humidite`).
- Vitesse du vent (`vent`).

### Échantillonnage
Nous avons testé plusieurs types d’échantillonnage :
1. **Échantillonnage aléatoire :** Une portion aléatoire des données est sélectionnée. Les tests ont montré qu’un échantillonnage à **50% des données** offre un bon compromis précision/quantité.
2. **Échantillonnage périodique :**
    - **Hebdomadaire :** Conserver une donnée par semaine (14.29% des données) a offert une précision moyenne de **0.78%**, meilleure que l’aléatoire.
    - **Mensuel :** Conserver une donnée par mois (3.43% des données) a offert une précision de **1.37%**.
3. **Échantillonnage stratifié :**
    - Les données ont été séparées en strates basées sur les températures (par ex. `T < 0`, `0 ≤ T < 10`, etc.).
    - Résultat : **19.71% des données conservées** avec une précision de **1.51%**.

### Conclusion sur l’échantillonnage
L’échantillonnage hebdomadaire offre le **meilleur ratio précision/quantité** pour une réduction de 85.71% des données.

---

## II. Compression des données

Les données ont été compressées avec trois outils : **gzip**, **zstd**, et **lz4**. Les tests ont mesuré :
- Le **taux de compression (%)**.
- Le **temps de compression (s)**.
- Le **ratio compression/temps**.

### Résultats (fichier original)
| Outil  | Niveau | Taille compressée | Compression (%) | Temps (s) | Ratio Compression/Temps |
|--------|--------|-------------------|-----------------|-----------|-------------------------|
| gzip   | 1      | 6883 octets       | 88.55%          | 0.003     | 29611.00               |
| gzip   | 9      | 4618 octets       | 92.32%          | 0.007     | 13198.78               |
| lz4    | 0      | 9459 octets       | 84.27%          | 0.004     | 21065.63               |
| zstd   | 1      | 5130 octets       | 91.47%          | 0.004     | 22867.06               |

### Conclusion sur la compression
- **zstd** (niveau 1) a le **meilleur ratio compression/temps**.
- **gzip** (niveau 1) est idéal pour des cas où la simplicité et la rapidité sont prioritaires.

---

## III. Stockage des données

### Création des jeux de données
Trois jeux de données ont été créés pour simuler des volumes différents :
- **Petit volume :** ~10,000 points.
- **Volume moyen :** ~1,000,000 points.
- **Gros volume :** ~50,000,000 points.

### Bases de données
Nous avons testé trois bases :
1. **PostgreSQL :** Base relationnelle.
2. **MongoDB :** Base NoSQL.
3. **InfluxDB :** Base optimisée pour les séries temporelles.

### Résultats des tests
| Base de données | Opération          | Temps (ms) | CPU (%) | RAM (Mo) | I/O (Mo) |
|------------------|--------------------|------------|---------|----------|----------|
| **PostgreSQL**   | Écriture           | 450        | 20      | 50       | 10       |
|                  | Lecture brute      | 120        | 10      | 30       | 5        |
|                  | Agrégation         | 80         | 8       | 35       | 3        |
| **MongoDB**      | Écriture           | 300        | 25      | 60       | 12       |
|                  | Lecture brute      | 100        | 12      | 50       | 6        |
|                  | Agrégation         | 90         | 15      | 55       | 4        |
| **InfluxDB**     | Écriture           | 200        | 30      | 40       | 8        |
|                  | Lecture brute      | 70         | 10      | 25       | 3        |
|                  | Agrégation         | 50         | 12      | 30       | 2        |

### Conclusion sur les bases de données
- **Écriture :** InfluxDB est la plus rapide grâce à son architecture optimisée.
- **Lecture brute :** MongoDB et InfluxDB sont très performants pour des requêtes simples.
- **Agrégation :** InfluxDB excelle grâce à son optimisation pour les séries temporelles.

---

## IV. Communication (HTTP vs MQTT)

### Résultats des tests
| Protocole | Taille totale (octets) | Économies MQTT (%) |
|-----------|-------------------------|--------------------|
| **HTTP**  | ~2,000,000             | -                  |
| **MQTT**  | ~1,200,000             | ~40%               |

### Conclusion sur les protocoles
- **MQTT** économise ~40% de bande passante par rapport à HTTP grâce à ses en-têtes légers.
- HTTP est plus simple mais consomme plus de ressources.

---

## Conclusion générale

Ce TD a permis d'explorer plusieurs aspects de l'optimisation des données :
1. **Réduction des données :**
    - L’échantillonnage hebdomadaire offre un bon compromis entre précision et réduction des données.
2. **Compression :**
    - **zstd** est recommandé pour des performances optimales.
3. **Stockage :**
    - InfluxDB est la meilleure option pour des séries temporelles, tandis que PostgreSQL et MongoDB sont plus polyvalents.
4. **Communication :**
    - MQTT est le choix optimal pour réduire la bande passante.

Ces résultats permettent de choisir les stratégies adaptées en fonction des contraintes (temps, ressources, stockage).
