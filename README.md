## Weather Pipeline Morocco 


## 1. Présentation du besoin traité
Une entreprise de livraison et de logistique opère dans plusieurs villes marocaines. Les conditions météorologiques peuvent impacter ses opérations, notamment en cas de fortes précipitations, de vents importants ou de températures extrêmes.

L'entreprise souhaite donc mettre en place une solution permettant de récupérer les prévisions météorologiques des prochains jours, d'identifier les périodes à risque et d'aider les responsables à anticiper les éventuelles perturbations.


## 2. Étapes suivies pendant les 5 jours de réalisation

- **Jour 1 : Préparation de l'environnement et extraction des données brutes**
  - création du projet et organisation des dossiers ;
  - préparation de l'environnement Python ;
  - telechargement des données depuis Simple-Maps ;
  - sauvgardement des donnees csv dans le dossier `data/ma.csv` ;
  - récupération des données météo depuis l'API Open-Meteo ;
  - sauvegarde des réponses JSON dans le dossier `data/bronze/raw_json/` ;
  - vérification que les données sont bien récupérées avant la transformation.

### Résultat du Jour 1
La première étape du pipeline a été validée : les données météo brutes ont bien été collectées et stockées dans la couche Bronze pour plusieurs villes du Maroc.


- **Jour 2 : Calcul de Risque weather & Configuration du base de donnes**
  - Création d'un score de risque météorologique de 0 à 100 permettant d'identifier les conditions  potentiellement defavorables. 
  - suppression des lignes duplicated et l'ajout de deux collones `(risk_score, risk_level)`
  - configuration du bases de donnes (creation de base de donne)


    
