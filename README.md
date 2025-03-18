# Profil Vocal Professionnel - Identification de la Tessiture

Ce projet Python permet d'identifier et de classifier la tessiture vocale en temps réel à partir d'un enregistrement audio. L'application fournit une interface graphique conviviale et un guide utilisateur pour réaliser un enregistrement de qualité, analyser le signal audio et afficher le Voice Range Profile (VRP).

## Fonctionnalités

- **Enregistrement audio en streaming :** Capture audio en temps réel avec un guide d’utilisation.
- **Analyse vocale :** Extraction de la fréquence fondamentale grâce à `librosa.pyin`.
- **Classification de la tessiture :** Attribution en 6 catégories :
  - **Voix féminine :**
    - Soprano (min_freq ≥ 250 Hz)
    - Mezzo-soprano (200 Hz ≤ min_freq < 250 Hz)
    - Contralto (min_freq < 200 Hz)
  - **Voix masculine :**
    - Ténor (min_freq ≥ 130 Hz)
    - Baritone (100 Hz ≤ min_freq < 130 Hz)
    - Basse (min_freq < 100 Hz)
- **Affichage graphique :** Visualisation du Voice Range Profile avec Matplotlib.

## Prérequis

Assurez-vous d'avoir Python installé ainsi que les bibliothèques suivantes :

- tkinter (inclus avec Python)
- sounddevice
- librosa
- numpy
- matplotlib

## Installation

1. Clonez ce dépôt
2. Installez les dépendances nécessaires via le fichier requirements.txt :

       pip install -r requirements.txt

## Utilisation

   Exécutez le script principal :

    python main.py

  Suivez les instructions à l'écran :
        Installez-vous dans un environnement silencieux avec un microphone de qualité.
        Cliquez sur "Démarrer l'enregistrement".
        Chantez de votre note la plus basse à la plus haute en tenant chaque note quelques secondes et en variant l'intensité.
        Cliquez sur "Terminer l'enregistrement" pour lancer l'analyse.

  Consultez le Voice Range Profile et la classification de la tessiture affichés à l'écran.

Structure du Projet

  main.py : Script principal contenant l'interface graphique et le traitement audio.
  requirements.txt : Liste des dépendances nécessaires.
  README.md : Ce fichier de documentation.
  LICENSE : Licence du projet (MIT - NonCommercial).

Licence

Ce projet est distribué sous la Licence MIT - NonCommercial.
Cela signifie que l'utilisation du logiciel est autorisée uniquement à des fins non commerciales. Toute vente ou utilisation commerciale est strictement interdite.
Pour plus de détails, consultez le fichier LICENSE.


Remarques

  Les seuils de classification vocale sont indicatifs et peuvent être ajustés en fonction des protocoles professionnels et des études acoustiques.
  Assurez-vous d'utiliser un environnement silencieux et un équipement de qualité pour obtenir les meilleurs résultats d'analyse.
  Développé par Auzoult Marc-Antoine ( https://viking-production.fr )
