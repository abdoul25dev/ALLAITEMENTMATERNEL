# Documentation du Modèle Statistique : Régression Logistique (EDS Cameroun 2018)

Ce document détaille la méthodologie, les concepts et l'interprétation des résultats de l'analyse statistique sur les facteurs influençant l'Allaitement Maternel Exclusif (AME) au Cameroun.

## 1. Contexte et Objectif
L'objectif de ce modèle est d'identifier les variables socio-démographiques et de santé qui influencent de manière significative la probabilité qu'un enfant de moins de 6 mois reçoive un Allaitement Maternel Exclusif (AME). 
L'AME est défini strictement selon les critères de l'OMS : l'enfant ne reçoit que du lait maternel, à l'exclusion de tout autre liquide (même l'eau claire) ou aliment solide.

## 2. Préparation des Données et Preprocessing
Les données issues du fichier `CMKR71FL.DTA` (Enquête EDS 2018) ont été filtrées pour ne conserver que les enfants de moins de 6 mois.
La variable cible binaire `AME` a été créée à partir des variables suivantes :
- Allaitement actuel (Oui)
- Consommation d'eau claire (Non)
- Consommation d'aliments solides ou de laitage (Non)

## 3. Analyse Bivariée Avancée
Avant de construire le modèle prédictif, la relation entre chaque variable indépendante (ex: `Niveau_Education`, `Milieu_Residence`) et la variable cible `AME` a été testée via le **Test d'Indépendance du Chi-Deux**.
Pour mesurer la force de ces relations, nous avons calculé le **V de Cramer** :
- **V ≈ 0** : Aucune association.
- **V > 0.1** : Association faible.
- **V > 0.3** : Association modérée.
- **V > 0.5** : Association forte.

## 4. Vérification de la Multicolinéarité (VIF)
Pour s'assurer qu'aucune variable explicative n'est redondante (ex: Richesse et Milieu de Résidence très liés), nous avons calculé le **VIF (Variance Inflation Factor)**.
Un VIF inférieur à 5 garantit que le modèle de régression ne souffrira pas d'instabilité mathématique.

## 5. Le Modèle Logistique Binomial Pondéré
Parce que l'EDS est une enquête stratifiée, les observations doivent être pondérées (`v005`). Nous avons donc utilisé un **Generalized Linear Model (GLM)** avec une famille Binomiale.

L'équation générale de la régression logistique s'écrit :
`Logit(P) = ln(P / (1 - P)) = β0 + β1*X1 + β2*X2 + ... + βn*Xn`

Où :
- **P** est la probabilité que l'enfant soit exclusivement allaité.
- **β0** est la constante (l'ordonnée à l'origine).
- **βn** sont les coefficients attribués à chaque caractéristique.

### Interprétation des Odds Ratios (Rapports de Cotes)
L'exponentielle des coefficients (`exp(β)`) donne l'**Odds Ratio (OR)**.
- **OR = 1** : La variable n'a aucun effet sur l'AME.
- **OR > 1** : La variable *augmente* les chances d'AME (Facteur favorisant). Par exemple, si l'OR pour "Accouchement en Formation Sanitaire" est de 1.5, cela signifie que la mère a 1.5 fois plus de chances de pratiquer l'AME comparé à l'accouchement à domicile.
- **OR < 1** : La variable *diminue* les chances d'AME (Facteur limitant).

### Évaluation Globale (Pseudo R-carré et ROC)
Le modèle est évalué via le **Pseudo R-carré de McFadden**, qui mesure la proportion de la variance expliquée par le modèle par rapport à un modèle "vide" (sans variables).
La **Courbe ROC** (Receiver Operating Characteristic) évalue la capacité du modèle à bien séparer les classes. L'aire sous la courbe (AUC) varie entre 0.5 (hasard) et 1.0 (modèle parfait).
