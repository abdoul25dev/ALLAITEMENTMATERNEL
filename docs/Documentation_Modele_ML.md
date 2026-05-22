# Documentation du Modèle de Machine Learning (EDS Cameroun 2018)

Ce document explique les concepts d'intelligence artificielle utilisés pour construire le système de prédiction de l'Allaitement Maternel Exclusif (AME).

## 1. Objectif du Machine Learning
Contrairement au modèle statistique classique (qui cherche à *expliquer* les relations), le Machine Learning vise la **performance prédictive maximale**. L'objectif est qu'en donnant les caractéristiques d'une mère (âge, éducation, richesse, lieu d'accouchement), le modèle devine de manière fiable si l'enfant sera allaité exclusivement ou non.

## 2. Préparation des Données pour l'Algorithme (One-Hot Encoding)
Les algorithmes mathématiques ne comprennent pas le texte ("Rural", "Urbain"). 
Le processus de **One-Hot Encoding** (via les *Dummies*) transforme chaque modalité textuelle en colonne binaire (0 ou 1). 
Par exemple, la colonne "Milieu de Résidence" devient "Residence_Rural" (1 si Rural, 0 sinon).

## 3. Séparation Apprentissage / Test (Train/Test Split)
Les données sont divisées en deux parties :
- **80% (Train)** : Utilisées pour que le modèle "apprenne" les motifs.
- **20% (Test)** : Utilisées pour "évaluer" le modèle sur des cas qu'il n'a jamais vus, afin d'assurer qu'il ne triche pas (mémorisation par cœur = Surapprentissage).

## 4. Modèles Testés
Trois algorithmes très puissants ont été mis en compétition :
1. **Régression Logistique (Machine Learning)** : Modèle linéaire classique, très rapide et interprétable, mais limité sur les relations complexes.
2. **Random Forest (Forêt Aléatoire)** : Assemble plusieurs centaines d'arbres de décision. Très robuste contre le surapprentissage et capable de détecter des relations non linéaires.
3. **Gradient Boosting** : Construit des arbres de manière séquentielle, chaque nouvel arbre corrigeant les erreurs des précédents. C'est souvent l'algorithme le plus performant pour les données tabulaires (tabulaires = type Excel).

*Note : Les classes étant potentiellement déséquilibrées, les poids (`class_weight='balanced'`) ont été utilisés pour forcer le modèle à prêter attention aux cas minoritaires.*

## 5. Explication des Métriques d'Évaluation
- **Accuracy (Précision globale)** : Pourcentage de prédictions exactes (AME et Non-AME confondus).
- **Précision** : Parmi tous ceux que le modèle a prédits "AME", combien l'étaient réellement ?
- **Rappel (Recall / Sensibilité)** : Parmi tous les *vrais* cas "AME", combien le modèle a-t-il réussi à détecter ?
- **F1-Score** : Moyenne harmonique entre Précision et Rappel. Idéal si on veut un équilibre entre ne pas rater d'AME et ne pas faire de fausses alertes.
- **ROC-AUC** : La capacité globale du modèle à classer correctement. Plus on s'approche de 1.0 (100%), meilleur est le modèle.

## 6. Analyse des Visualisations
1. **Matrice de Confusion** : Un tableau croisant ce que le modèle a prédit vs la réalité. Permet de voir précisément où le modèle se trompe (Faux Positifs vs Faux Négatifs).
2. **Learning Curves (Courbes d'apprentissage)** : Montrent l'évolution des performances en fonction du volume de données. 
   - Si les courbes d'apprentissage et de test se rejoignent avec un score élevé, le modèle généralise bien. 
   - Si la courbe d'apprentissage est à 100% mais le test reste bas, il y a surapprentissage (*overfitting*).
3. **KDE Plot (Distribution des probabilités)** : Montre comment le modèle sépare visuellement les certitudes. Un bon modèle aura une "bosse" rouge près de 0 et une "bosse" verte près de 1, prouvant qu'il n'est pas "indécis" au milieu (0.5).

## 7. Stress Test et Déploiement
Le modèle a été soumis à un **Stress Test** sur 1000 données générées artificiellement (avec introduction de bruit aléatoire pour simuler le monde réel chaotique). Cela garantit que le modèle ne "casse" pas face à des données légèrement inhabituelles.

Enfin, le modèle final est sauvegardé sous forme de fichiers `.pkl` et `.joblib`. L'application Web s'appuie sur ces fichiers : elle charge "l'intelligence" sauvegardée pour faire des prédictions instantanées sans avoir à tout recalculer.
