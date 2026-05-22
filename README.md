# Projet d'Intelligence Artificielle en Santé : Allaitement Maternel Exclusif (AME) - EDS Cameroun 2018

Ce projet vise à modéliser et prédire la probabilité de l'Allaitement Maternel Exclusif (AME) chez les enfants de moins de 6 mois au Cameroun, à partir des données de l'Enquête Démographique et de Santé (EDS 2018).

Développé par **ABDOUL GANIOU TELLY**, étudiant en Master 1 Data Science.

---

## Architecture du Projet

Le projet couvre le pipeline complet de Data Science : de l'extraction de données brutes à la mise en production via une application Web Streamlit interactive.

### 1. Préparation des Données (`01_generation_dataset.py`)
- Extraction des données depuis le fichier source brut DHS (`CMKR71FL.DTA`).
- Nettoyage et **décodage exhaustif** : Les codes cryptiques DHS (ex: `v012`, `v190`) ont été renommés en colonnes claires (`Age_Mere_Actuel`, `Indice_Richesse`).
- Les modalités numériques (1, 2) ont été mappées avec leurs libellés textuels réels ("Urbain", "Rural").
- **Sortie** : `dataset_allaitement_edsc2018_decode.xlsx` (contenant les données nettoyées et le dictionnaire détaillé des métadonnées).

### 2. Modélisation Statistique (`02_Analyse_Statistique_Allaitement.ipynb`)
- **Définition stricte de l'AME** : L'enfant ne reçoit que le lait maternel, ni eau, ni nourriture, selon les standards OMS.
- **Analyse Bivariée** : Tests du Chi-Deux et calcul du **V de Cramer** pour évaluer rigoureusement la force de la corrélation.
- **Analyse Multivariée** : Test de multicolinéarité via le **VIF (Variance Inflation Factor)**.
- **Régression Logistique** : Modèle GLM binomial robuste, prenant en compte le poids de l'échantillon (`v005`). Évaluation via le Pseudo R-carré (McFadden), la courbe ROC, l'AUC, et les Odds Ratios.

### 3. Machine Learning (`03_Machine_Learning_Allaitement.ipynb`)
- Pipeline de prédiction : One-Hot Encoding automatique via *Dummies*.
- **Algorithmes testés** : Régression Logistique (Scikit-Learn), Random Forest, Gradient Boosting.
- **Évaluation** : Précision, Rappel, F1-Score, AUC.
- **Visualisations avancées** : Matrice de Confusion, Courbes d'Apprentissage (Learning Curves) pour vérifier l'absence de surapprentissage, et Courbe KDE des probabilités.
- **Stress Test** : Le modèle sélectionné (le plus performant) a été évalué sur des milliers de données synthétiques bruitées pour garantir sa solidité face au monde réel.
- **Export** : Le modèle final est sauvegardé dans le dossier `model/` (formats `.pkl` et `.joblib`) avec le mapping de ses colonnes (`model_columns.joblib`).

### 4. Application Web de Production (`app/`)
Une application **Streamlit** moderne, haut de gamme et épurée (UI médicale) servant de vitrine pour les prédictions du modèle :
- **Formulaire de Prédiction** : Les champs saisissent le profil de la mère et interagissent en temps réel avec le modèle `.joblib`.
- **Diagnostic Clinique** : Les résultats ne donnent pas qu'un chiffre, ils fournissent une analyse des facteurs de réussite ou d'échec de l'AME.
- **Historique Local & Export** : Les prédictions sont persistées intelligemment dans la session, avec la possibilité d'un export Excel professionnel instantané.

---

## Lancement Rapide (Mise en Production)

### Prérequis
Assurez-vous d'avoir Python installé ainsi que les dépendances nécessaires.
```bash
pip install pandas numpy scikit-learn matplotlib seaborn statsmodels xgboost jupyter streamlit xlsxwriter streamlit-javascript
```

### Démarrage de l'Application
Placez-vous à la racine du projet et exécutez l'application Streamlit :
```bash
streamlit run app/app.py
```
L'application s'ouvrira automatiquement dans votre navigateur web par défaut.

---

## 📂 Structure du Répertoire (Workspace Nettoyé)

- `CMKR71FL.DTA` : Fichier de base de l'enquête EDS.
- `dataset_allaitement_edsc2018_decode.xlsx` : Jeu de données prêt à l'emploi.
- `generate_nb_stat.py` / `generate_nb_ml.py` : Scripts générateurs de notebooks.
- `02_Analyse_Statistique_Allaitement.ipynb` : Notebook d'analyse statistique de pointe.
- `03_Machine_Learning_Allaitement.ipynb` : Notebook de Machine Learning (avec visualisations des métriques).
- `docs/` : Dossier contenant les documentations mathématiques exhaustives des modèles.
- `model/` : Fichiers persistants des modèles de prédiction ML (`.joblib`, `.pkl`).
- `app/` : Dossier contenant le code source (`app.py`, `utils.py`, `styles.css`) de l'application Streamlit.

---
**ABDOUL GANIOU TELLY**  
*Étudiant en Master 1 Data Science*
