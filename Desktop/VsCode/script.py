from PIL import Image, ImageTk
import tkinter as tk

def get_file_icon(filepath):
    # Charger l'image d'icône (assurez-vous d'avoir une image par défaut)
    icon_path = "file_icon.png"  # Chemin de votre icône de fichier
    icon = Image.open(icon_path)
    icon.thumbnail((32, 32))  # Redimensionner à 32x32 pixels
    return ImageTk.PhotoImage(icon)

def get_folder_icon(folderpath):
    # Charger l'image d'icône (assurez-vous d'avoir une image par défaut)
    icon_path = "folder_icon.png"  # Chemin de votre icône de dossier
    icon = Image.open(icon_path)
    icon.thumbnail((32, 32))  # Redimensionner à 32x32 pixels
    return ImageTk.PhotoImage(icon)
# Exemple d'utilisation avec Tkinter
root = tk.Tk()
file_icon = get_file_icon("path_to_file")  # Remplacez par le chemin d'un fichier réel
file_label = tk.Label(root, text="Fichier", image=file_icon)
file_label.image = file_icon  # Préserver la référence à l'image
file_label.pack()

folder_icon = get_folder_icon("path_to_folder")  # Remplacez par le chemin d'un dossier réel
folder_label = tk.Label(root, text="Dossier", image=folder_icon)
folder_label.image = folder_icon  # Préserver la référence à l'image
folder_label.pack()


root.mainloop()