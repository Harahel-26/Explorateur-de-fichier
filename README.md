# Explorateur de Fichiers en Python avec Tkinter

## **Membres du groupe**
## ADJABA Ayodélé
## AGELE Delore
## DAFIA Jonas
## HOUANDJA Stéphanie
## KOUTCHIKA Harahel

## Description
Ce projet est une application d'explorateur de fichiers développée en Python avec l'interface graphique Tkinter. Il permet de naviguer, gérer et organiser les fichiers et dossiers de votre système de manière simple et intuitive. L'application offre des fonctionnalités telles que la navigation dans les dossiers, la gestion des favoris, des fichiers récents, la recherche et le filtrage des fichiers, ainsi que la gestion des tags.

## Fonctionnalités
- **Navigation dans les dossiers** : Accédez à vos fichiers et dossiers facilement.
- **Favoris** : Ajoutez des dossiers et fichiers aux favoris pour un accès rapide.
- **Fichiers récents** : Consultez les fichiers que vous avez récemment ouverts.
- **Téléchargements** : Affichez le répertoire de téléchargements.
- **Recherche** : Recherchez des fichiers et dossiers par nom.
- **Filtrage** : Filtrez les fichiers par type (images, texte, PDF, vidéos).
- **Création de dossiers** : Créez de nouveaux dossiers à partir de l'interface.
- **Gestion des tags** : Ajoutez et gérez des tags pour organiser vos fichiers (fonction de base).
- **Contexte** : Menu contextuel pour des actions supplémentaires sur les fichiers (ouvrir, renommer, supprimer, ajouter aux favoris).
  
## Prérequis
- Python 3.x
- Tkinter (généralement inclus avec Python)
- Pillow (pour la gestion des icônes)

### Documentation des Problèmes et Solutions

#### 1. Problème : Chargement des icônes
*Description :* Les icônes pour les dossiers et fichiers n'étaient pas chargées correctement, ce qui entraînait des erreurs d'affichage.

*Solution :* 
- Vérifiez que les fichiers d'icônes (par exemple, folder_icon.png, file_icon.png, etc.) sont présents dans le même répertoire que le script Python.
- Utilisez la bibliothèque PIL (Pillow) pour redimensionner les icônes avant de les afficher dans l'application. Cela garantit que les icônes sont de la bonne taille pour l'affichage dans l'interface utilisateur. Mais pourtant ces deux icônes ne s'affichent pas.

#### 2. Problème : Permissions d'accès aux répertoires
*Description :* Lors de l'accès à certains répertoires, des erreurs de permission se produisaient, ce qui empêchait l'affichage des fichiers.

*Solution :* 
- Utilisez un bloc try-except pour gérer les exceptions PermissionError. Cela permet d'afficher un message d'erreur convivial à l'utilisateur au lieu de faire planter l'application.
- Exemple de code :
  python
  except PermissionError:
      messagebox.showerror("Erreur", "Vous n'avez pas la permission d'accéder à ce répertoire.")
  

#### 3. Problème : Filtrage des fichiers
*Description :* Le filtrage des fichiers par type ne fonctionnait pas correctement, car les extensions de fichiers n'étaient pas vérifiées de manière appropriée.

*Solution :* 
- Créez un dictionnaire pour mapper les types de fichiers à leurs extensions respectives. Cela permet de vérifier facilement si un fichier correspond au type sélectionné dans le menu déroulant.
- Exemple de code :
  python
  file_extensions = {
      "Images": (".png", ".jpg", ".jpeg", ".gif", ".bmp"),
      "Texte": (".txt", ".md", ".csv"),
      "PDF": (".pdf",),
      "Vidéos": (".mp4", ".avi", ".mov", ".mkv"),
  }
  

#### 4. Problème : Ouverture de fichiers
*Description :* L'ouverture de fichiers avec os.startfile() ne fonctionnait pas sur certains systèmes d'exploitation, notamment Linux.

*Solution :* 
- Utilisez une approche conditionnelle pour ouvrir des fichiers en fonction du système d'exploitation. Par exemple, pour Linux, utilisez subprocess pour ouvrir des fichiers avec l'application par défaut.

#### 5. Problème : Suppression de dossiers non vides
*Description :* La tentative de suppression de dossiers non vides entraînait une erreur.

*Solution :* 
- Utilisez shutil.rmtree() pour supprimer des dossiers non vides. Cela permet de supprimer un dossier et tout son contenu.
- Exemple de code :
  python
  import shutil
  if os.path.isdir(item_path):
      shutil.rmtree(item_path)
  

#### 6. Problème : Renommage de fichiers
*Description :* Le renommage de fichiers ou de dossiers échouait parfois en raison de conflits de noms.

*Solution :* 
- Ajoutez une vérification pour voir si le nouveau nom existe déjà avant de renommer. Si c'est le cas, demandez à l'utilisateur de choisir un autre nom.
- Exemple de code :
  python
  if os.path.exists(new_path):
      messagebox.showerror("Erreur", "Un fichier ou dossier avec ce nom existe déjà.")
  
  ### Étape 1 : Prérequis

Avant de commencer, assurez-vous d'avoir installé Python sur votre machine. Vous pouvez télécharger Python depuis le site officiel : [python.org](https://www.python.org/downloads/).

# Vérifiez si Python est installé
python --version


### Étape 2 : Installer les bibliothèques nécessaires

Le projet utilise la bibliothèque Pillow pour la gestion des images. Vous devez l'installer via pip. Ouvrez votre terminal ou votre invite de commande et exécutez la commande suivante :

bash
pip install Pillow

![Capture d'écran]asserts/Screenshot1.png

### Étape 3 : Préparer les icônes

Le projet utilise plusieurs icônes pour représenter les dossiers et fichiers. Vous devez vous assurer que les fichiers d'icônes suivants sont présents dans le même répertoire que votre script Python :

- folder_icon.png
- file_icon.png
- home_icon.png
- recent_icon.png
- download_icon.png
- favorite_icon.png
- tag_icon.png

![Capture d'écran]asserts/Screenshot2.png

### Étape 4 : Exécuter le script

Une fois que vous avez installé les dépendances et préparé les icônes, vous pouvez exécuter le script. Ouvrez votre terminal ou votre invite de commande, naviguez jusqu'au répertoire contenant le script et exécutez la commande suivante :

bash
python explorateur.py

![Capture d'écran]assets/Screenshot3.png

### Étape 5 : Utilisation de l'application

Une fois l'application lancée, vous verrez une interface graphique avec plusieurs options. Voici quelques fonctionnalités clés :

- *Navigation* : Utilisez le panneau latéral pour naviguer entre les répertoires.
- *Barre d'outils* : Utilisez les boutons pour créer des dossiers, actualiser la liste, etc.
- *Recherche et filtrage* : Recherchez des fichiers et filtrez par type.
- *Favoris et fichiers récents* : Accédez rapidement à vos fichiers favoris et récents.

![Capture d'écran]assert/Screenshot4.png

### Étape 6 : Gestion des fichiers

Vous pouvez ouvrir, renommer, supprimer des fichiers et dossiers, et les ajouter à vos favoris en utilisant le menu contextuel (clic droit sur un élément).

![Capture d'écran]asserts/Screenshot5.png
