import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import time
from PIL import Image, ImageTk

class FileManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Explorateur de Fichiers")
        self.root.geometry("800x600")

        self.current_path = os.getcwd()
        self.favorites = []  # Liste des favoris
        self.recent_files = []  # Liste des fichiers récents

        # Load folder and file icons
        self.folder_icon = ImageTk.PhotoImage(Image.open("folder_icon.png").resize((16, 16)))
        self.file_icon = ImageTk.PhotoImage(Image.open("file_icon.png").resize((16, 16)))
        self.home_icon = ImageTk.PhotoImage(Image.open("home_icon.png").resize((16, 16)))
        self.recent_icon = ImageTk.PhotoImage(Image.open("recent_icon.png").resize((16, 16)))
        self.download_icon = ImageTk.PhotoImage(Image.open("download_icon.png").resize((16, 16)))
        self.favorite_icon = ImageTk.PhotoImage(Image.open("favorite_icon.png").resize((16, 16)))
        self.tag_icon = ImageTk.PhotoImage(Image.open("tag_icon.png").resize((16, 16)))

        # Layout principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Panneau latéral gauche
        sidebar = tk.Frame(main_frame, width=200, bg="#2c3e50", relief=tk.SUNKEN)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Widgets dans le panneau latéral
        tk.Label(sidebar, text="Navigation", bg="#2c3e50", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Button(sidebar, text="Accueil", command=self.go_home, bg="#34495e", fg="white", relief=tk.FLAT, image=self.home_icon, compound=tk.LEFT).pack(fill=tk.X, padx=10, pady=5)
        tk.Button(sidebar, text="Récent", command=self.show_recent, bg="#34495e", fg="white", relief=tk.FLAT, image=self.recent_icon, compound=tk.LEFT).pack(fill=tk.X, padx=10, pady=5)
        tk.Button(sidebar, text="Téléchargements", command=self.show_downloads, bg="#34495e", fg="white", relief=tk.FLAT, image=self.download_icon, compound=tk.LEFT).pack(fill=tk.X, padx=10, pady=5)
        tk.Button(sidebar, text="Favoris", command=self.show_favorites, bg="#34495e", fg="white", relief=tk.FLAT, image=self.favorite_icon, compound=tk.LEFT).pack(fill=tk.X, padx=10, pady=5)
        tk.Button(sidebar, text="Tags", command=self.show_tags, bg="#34495e", fg="white", relief=tk.FLAT, image=self.tag_icon, compound=tk.LEFT).pack(fill=tk.X, padx=10, pady=5)

        # Frame pour les composants principaux
        main_content = tk.Frame(main_frame)
        main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Barre d'outils
        toolbar = tk.Frame(main_content, bg="#ecf0f1")
        toolbar.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(toolbar, text="Précédent", command=self.go_back, bg="#bdc3c7", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Actualiser", command=self.refresh_list, bg="#bdc3c7", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Créer Dossier", command=self.create_folder, bg="#bdc3c7", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Favoris", command=self.show_favorites, bg="#bdc3c7", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

        # Barre de recherche et filtrage
        search_frame = tk.Frame(main_content, bg="#ecf0f1")
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(search_frame, text="Rechercher :", bg="#ecf0f1").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Chercher", command=self.refresh_list, bg="#bdc3c7", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

        # Filtrage des fichiers par type
        tk.Label(search_frame, text="Filtrer :", bg="#ecf0f1").pack(side=tk.LEFT, padx=5)
        self.filter_var = tk.StringVar(value="Tous")
        filter_options = ["Tous", "Images", "Texte", "PDF", "Vidéos"]
        self.filter_menu = ttk.Combobox(search_frame, textvariable=self.filter_var, values=filter_options, state="readonly")
        self.filter_menu.pack(side=tk.LEFT, padx=5)
        self.filter_menu.bind("<<ComboboxSelected>>", lambda e: self.refresh_list())

        # Barre d'adresse
        self.path_var = tk.StringVar()
        path_entry = tk.Entry(main_content, textvariable=self.path_var, state="readonly", font=("Arial", 10))
        path_entry.pack(fill=tk.X, padx=5, pady=5)

        # Arborescence des fichiers
        self.tree = ttk.Treeview(main_content, columns=("Nom", "Type", "Détails"), show="headings")
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Détails", text="Détails")
        self.tree.column("Nom", width=300)
        self.tree.column("Type", width=100)
        self.tree.column("Détails", width=200)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tree.bind("<Double-1>", self.open_item)
        self.tree.bind("<Button-3>", self.show_context_menu)  # Clic droit

        self.refresh_list()

    def refresh_list(self):
        """Actualise la liste des fichiers et dossiers."""
        self.tree.delete(*self.tree.get_children())

        selected_filter = self.search_var.get().lower()
        file_filter = self.filter_var.get()

        file_extensions = {
            "Images": (".png", ".jpg", ".jpeg", ".gif", ".bmp"),
            "Texte": (".txt", ".md", ".csv"),
            "PDF": (".pdf",),
            "Vidéos": (".mp4", ".avi", ".mov", ".mkv"),
        }

        try:
            for item in os.listdir(self.current_path):
                full_path = os.path.join(self.current_path, item)
                if os.path.isdir(full_path):
                    icon = self.folder_icon
                    if selected_filter in item.lower() or not selected_filter:
                        self.tree.insert("", tk.END, values=(item, "Dossier", ""), image=icon)
                else:
                    ext = os.path.splitext(item)[1].lower()
                    size = os.path.getsize(full_path)
                    mod_time = time.ctime(os.path.getmtime(full_path))
                    icon = self.file_icon

                    if (selected_filter in item.lower() or not selected_filter):
                        if file_filter == "Tous" or (file_filter in file_extensions and ext in file_extensions[file_filter]):
                            self.tree.insert("", tk.END, values=(item, "Fichier", f"{size} octets, modifié {mod_time}"), image=icon)
        except PermissionError:
            messagebox.showerror("Erreur", "Vous n'avez pas la permission d'accéder à ce répertoire.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur inattendue est survenue : {e}")

        self.update_path_bar()

    def update_path_bar(self):
        """Met à jour la barre d'adresse avec le chemin actuel."""
        self.path_var.set(self.current_path)

    def open_item(self, event=None):
        """Ouvre un dossier ou un fichier."""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_name = self.tree.item(selected_item, "values")[0]
        new_path = os.path.join(self.current_path, item_name)

        if os.path.isdir(new_path):
            self.current_path = new_path
            self.refresh_list()
        else:
            try:
                os.startfile(new_path)  # Ouvre le fichier avec l'application par défaut
                if new_path not in self.recent_files:
                    self.recent_files.append(new_path)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier : {e}")

    def go_back(self):
        """Remonte d'un dossier."""
        parent_path = os.path.dirname(self.current_path)
        if parent_path and parent_path != self.current_path:
            self.current_path = parent_path
            self.refresh_list()

    def go_home(self):
        """Retourne au répertoire de départ."""
        self.current_path = os.getcwd()
        self.refresh_list()

    def create_folder(self):
        """Crée un nouveau dossier."""
        folder_name = simpledialog.askstring("Créer un dossier", "Nom du dossier :")
        if folder_name:
            new_folder_path = os.path.join(self.current_path, folder_name)
            try:
                os.mkdir(new_folder_path)
                self.refresh_list()
            except FileExistsError:
                messagebox.showerror("Erreur", "Un dossier avec ce nom existe déjà.")

    def add_to_favorites(self):
        """Ajoute un fichier ou dossier aux favoris."""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_name = self.tree.item(selected_item, "values")[0]
        item_path = os.path.join(self.current_path, item_name)

        if item_path not in self.favorites:
            self.favorites.append(item_path)
            messagebox.showinfo("Favoris", f"Ajouté aux favoris : {item_name}")
        else:
            messagebox.showinfo("Favoris", f"{item_name} est déjà dans les favoris.")

    def show_favorites(self):
        """Affiche les favoris."""
        self.tree.delete(*self.tree.get_children())
        for favorite in self.favorites:
            item_name = os.path.basename(favorite)
            if os.path.isdir(favorite):
                self.tree.insert("", tk.END, values=(item_name, "Dossier", ""), image=self.folder_icon)
            else:
                size = os.path.getsize(favorite)
                mod_time = time.ctime(os.path.getmtime(favorite))
                self.tree.insert("", tk.END, values=(item_name, "Fichier", f"{size} octets, modifié {mod_time}"), image=self.file_icon)

    def show_recent(self):
        """Affiche les fichiers récents."""
        self.tree.delete(*self.tree.get_children())
        for recent in self.recent_files:
            item_name = os.path.basename(recent)
            if os.path.isdir(recent):
                self.tree.insert("", tk.END, values=(item_name, "Dossier", ""), image=self.folder_icon)
            else:
                size = os.path.getsize(recent)
                mod_time = time.ctime(os.path.getmtime(recent))
                self.tree.insert("", tk.END, values=(item_name, "Fichier", f"{size} octets, modifié {mod_time}"), image=self.file_icon)

    def show_downloads(self):
        """Affiche les téléchargements (fictif, exemple)."""
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.current_path = downloads_path
        self.refresh_list()

    def show_tags(self):
        """Affiche une fenêtre pour gérer les tags."""
        tag_window = tk.Toplevel(self.root)
        tag_window.title("Gérer les Tags")
        tag_window.geometry("400x300")

        tk.Label(tag_window, text="Ajouter un tag :", font=("Arial", 10)).pack(pady=10)
        tag_var = tk.StringVar()
        tk.Entry(tag_window, textvariable=tag_var).pack(pady=5)

        tk.Button(tag_window, text="Ajouter", command=lambda: self.add_tag(tag_var.get())).pack(pady=5)
        tk.Button(tag_window, text="Fermer", command=tag_window.destroy).pack(pady=5)

    def add_tag(self, tag):
        """Ajoute un tag (exemple simple, vous pouvez le lier à des fichiers)."""
        if tag:
            messagebox.showinfo("Succès", f"Tag '{tag}' ajouté !")
        else:
            messagebox.showerror("Erreur", "Aucun tag entré.")

    def show_context_menu(self, event):
        """Affiche un menu contextuel."""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="Ouvrir", command=self.open_item)
        context_menu.add_command(label="Renommer", command=self.rename_selected)
        context_menu.add_command(label="Supprimer", command=self.delete_selected)
        context_menu.add_command(label="Ajouter aux Favoris", command=self.add_to_favorites)
        context_menu.post(event.x_root, event.y_root)

    def delete_selected(self):
        """Supprime le fichier ou dossier sélectionné."""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_name = self.tree.item(selected_item, "values")[0]
        item_path = os.path.join(self.current_path, item_name)

        if messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer '{item_name}' ?"):
            try:
                if os.path.isdir(item_path):
                    os.rmdir(item_path)  # Ne supprime que les dossiers vides
                else:
                    os.remove(item_path)
                self.refresh_list()
            except OSError as e:
                messagebox.showerror("Erreur", f"Impossible de supprimer : {e}")

    def rename_selected(self):
        """Renomme le fichier ou dossier sélectionné."""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_name = self.tree.item(selected_item, "values")[0]
        item_path = os.path.join(self.current_path, item_name)

        new_name = simpledialog.askstring("Renommer", f"Nouveau nom pour '{item_name}':")
        if new_name:
            new_path = os.path.join(self.current_path, new_name)
            try:
                os.rename(item_path, new_path)
                self.refresh_list()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de renommer : {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileManager(root)
    root.mainloop()
