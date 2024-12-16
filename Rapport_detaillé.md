# Rapport sur les Stratégies de Green I.T. pour la Collecte et le Stockage de Données

## **Introduction**
Ce projet a pour objectif d’explorer différentes stratégies de Green I.T., en se concentrant sur :
- La collecte et la préparation des données.
- L’échantillonnage pour réduire les volumes tout en maintenant une précision acceptable.
- La compression des données pour optimiser leur transfert.
- Le transfert et le stockage des données dans plusieurs bases, avec des mesures de performance.

Nous utilisons des outils tels que **Prometheus**, **Grafana** et **node-exporter** pour visualiser les métriques (CPU, RAM, I/O) et évaluer l’impact des différentes étapes.

---

## **I. Collecte des données**

### **1. Nettoyage**
Les données initiales téléchargées (au format JSON) ont été nettoyées pour ne conserver que les champs pertinents : température réelle, température ressentie, humidité et vitesse du vent. Les données inutiles ont été supprimées pour optimiser les traitements suivants.

Exemple de structure nettoyée :
```json
{
  "date": "2024-12-16",
  "temperature_reelle": 15.2,
  "temperature_ressentie": 13.4,
  "humidite": 72,
  "vent": 5.6
}


---

### **2. Échantillonnage**

#### **a. Calcul initial des moyennes**
Avant tout échantillonnage, nous avons calculé les moyennes des températures réelles et ressenties ainsi que leurs écarts pour servir de base de comparaison.

#### **b. Échantillonnage aléatoire**
Une fonction a été implémentée pour sélectionner un pourcentage aléatoire des données. Les résultats montrent qu’un échantillonnage à **10-20%** conserve une précision acceptable tout en réduisant significativement le volume.

- Exemple :
    - **10% des données** : Précision moyenne de 4.59%.
    - **50% des données** : Précision moyenne de 2.35%.

#### **c. Échantillonnage périodique**
Nous avons testé un échantillonnage périodique hebdomadaire et mensuel :
- **Hebdomadaire :** 14.29% des données, précision moyenne de 0.78%.
- **Mensuel :** 3.43% des données, précision moyenne de 1.37%.

L’échantillonnage périodique hebdomadaire s’est révélé plus efficace que l’échantillonnage aléatoire pour un volume similaire.

#### **d. Échantillonnage stratifié**
L’échantillonnage stratifié a permis de regrouper les données par plages de température, améliorant ainsi la précision tout en maintenant un faible volume.
- **Stratification par plages de température :**
    - **T < 0, 0 <= T < 10, 10 <= T < 20, T >= 20.**
    - **19.71% des données**, précision moyenne de **1.51%**.

---

## **II. Compression**

### **1. Méthodes testées**
Nous avons testé trois outils de compression : **gzip**, **lz4**, et **zstd**, avec des niveaux de compression minimum et maximum.

### **2. Résultats**
Pour un fichier de 10 000 points :
```markdown
| Outil | Niveau | Compression (%) | Temps (s) | Ratio Compression\Temps |
|-------|--------|-----------------|-----------|-------------------------|
| gzip  | 1      | 88.55%          | 0.003     | 29611.00                |
| gzip  | 9      | 92.32%          | 0.007     | 13198.78                |
| lz4   | 0      | 84.27%          | 0.004     | 21065.63                |
| zstd  | 1      | 91.47%          | 0.004     | 22867.06                |
| zstd  | 22     | 94.18%          | 0.038     | 2488.73                 |
```

### **3. Analyse**
- **Meilleure compression :** `zstd` (niveau 22) avec 94.18%.
- **Meilleur ratio compression/temps :** `gzip` (niveau 1) et `zstd` (niveau 1).

---

## **III. Stockage des données**

### **1. Génération des jeux de données**
Trois jeux de données ont été générés pour les tests :
- **Petit volume :** 10 000 points (~quelques Mo).
- **Moyen volume :** 1 000 000 points (~centaines de Mo).
- **Gros volume :** 50 000 000 points (~plusieurs Go).

---

### **2. Protocoles de communication**

#### **a. HTTP**
Un serveur HTTP a été configuré pour recevoir des requêtes POST et mesurer la taille totale des données transférées.

#### **b. MQTT**
Un broker MQTT (Mosquitto) a été configuré pour transférer les données et mesurer la taille des messages.

#### **c. Comparaison**
| Protocole | Taille totale (octets) | Économies avec MQTT (%) |
|-----------|-------------------------|-------------------------|
| HTTP      | 2,000,000              | -                       |
| MQTT      | 1,200,000              | 40%                    |

---

### **3. Bases de données**

#### **a. Configuration**
Trois bases ont été déployées via Docker :
- **PostgreSQL :** Base relationnelle.
- **MongoDB :** Base NoSQL.
- **InfluxDB :** Base optimisée pour séries temporelles.

#### **b. Tests**
Trois scripts ont été développés pour chaque base afin de tester :
1. **Écriture :** Insertion des données une par une.
2. **Lecture brute :** Lecture des 100 dernières données.
3. **Agrégation :** Calcul de la moyenne des températures.

---

### **IV. Résultats des tests**

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

---

## **Conclusion**

### **1. Compression**
- `zstd` est le plus efficace en termes de compression.
- `gzip` et `zstd` offrent les meilleurs ratios compression/temps.

### **2. Communication**
- **MQTT** économise environ **40%** de bande passante par rapport à **HTTP**, grâce à ses en-têtes légers.

### **3. Bases de données**
- **Écriture :** InfluxDB est la plus rapide.
- **Lecture brute :** InfluxDB et MongoDB sont comparables.
- **Agrégation :** InfluxDB excelle grâce à son optimisation pour les séries temporelles.

### **4. Recommandations**
- **InfluxDB** est idéale pour les séries temporelles volumineuses.
- **MongoDB** convient pour des données semi-structurées avec des requêtes fréquentes.
- **PostgreSQL** est adaptée pour des données relationnelles nécessitant robustesse et cohérence.

Ce projet met en évidence l'importance d'optimiser chaque étape pour réduire la consommation de ressources tout en maintenant des performances acceptables.
```