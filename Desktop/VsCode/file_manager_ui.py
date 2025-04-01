import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
import send2trash
import zipfile

class FileManagerApp:
    def __init__(self, master):
        # Configurer le style moderne et élégant
        self.master = master
        self.master.configure(bg='#f0f0f0')
        
        # Créer un style personnalisé
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Thème moderne
        self.style.configure('TButton', background='#4CAF50', foreground='white', font=('Arial', 10, 'bold'))
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 12))
        
        # Créer la disposition principale
        self.create_layout()
        
        # Charger le répertoire initial
        self.current_directory = os.path.expanduser('~')
        self.update_file_list()
    
    def create_layout(self):
        # Conteneur principal avec un design moderne
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Barre de navigation avec le chemin actuel
        nav_frame = ttk.Frame(main_frame)
        nav_frame.pack(fill=tk.X, pady=10)
        
        self.path_var = tk.StringVar(value=self.current_directory)
        path_label = ttk.Label(nav_frame, textvariable=self.path_var, style='TLabel')
        path_label.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Boutons de navigation
        nav_buttons = [
            ("🏠 Accueil", self.go_home),
            ("↑ Parent", self.go_parent),
            ("📂 Choisir", self.choose_directory)
        ]
        
        for text, command in nav_buttons:
            btn = ttk.Button(nav_frame, text=text, command=command, style='TButton')
            btn.pack(side=tk.RIGHT, padx=5)
        
        # Liste des fichiers avec un design moderne
        self.file_listbox = tk.Listbox(
            main_frame, 
            selectmode=tk.EXTENDED, 
            bg='white', 
            font=('Arial', 10),
            selectbackground='#4CAF50',
            activestyle='none'
        )
        self.file_listbox.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Ajouter un scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        
        # Bind les événements
        self.file_listbox.bind('<Double-1>', self.open_item)
        
        # Cadre des actions
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        # Boutons d'action
        actions = [
            ("📋 Copier", self.copy_files),
            ("✂ Couper", self.cut_files),
            ("🗑 Supprimer", self.delete_files),
            ("🤏 Renommer", self.rename_file),
            ("📦 Compresser", self.compress_files)
        ]
        
        for text, command in actions:
            btn = ttk.Button(action_frame, text=text, command=command, style='TButton')
            btn.pack(side=tk.LEFT, padx=5, expand=True)
    
    def update_file_list(self):
        # Mettre à jour la liste des fichiers
        self.file_listbox.delete(0, tk.END)
        
        try:
            # Lister les fichiers et dossiers
            items = os.listdir(self.current_directory)
            
            # Trier les éléments (dossiers d'abord, puis fichiers)
            items.sort(key=lambda x: (not os.path.isdir(os.path.join(self.current_directory, x)), x))
            
            for item in items:
                full_path = os.path.join(self.current_directory, item)
                
                # Ajouter un emoji pour les dossiers et fichiers
                if os.path.isdir(full_path):
                    display_item = f"📁 {item}"
                else:
                    display_item = f"📄 {item}"
                
                self.file_listbox.insert(tk.END, display_item)
            
            # Mettre à jour le chemin
            self.path_var.set(self.current_directory)
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lister les fichiers : {e}")
    
    def open_item(self, event):
        # Ouvrir un fichier ou un dossier
        selection = self.file_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        item = self.file_listbox.get(index).split(" ", 1)[1]  # Retirer l'emoji
        full_path = os.path.join(self.current_directory, item)
        
        if os.path.isdir(full_path):
            # Si c'est un dossier, l'ouvrir
            self.current_directory = full_path
            self.update_file_list()
        else:
            # Si c'est un fichier, l'ouvrir avec l'application par défaut
            try:
                os.startfile(full_path)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier : {e}")
    
    def go_home(self):
        # Aller au répertoire personnel
        self.current_directory = os.path.expanduser('~')
        self.update_file_list()
    
    def go_parent(self):
        # Aller au dossier parent
        parent = os.path.dirname(self.current_directory)
        self.current_directory = parent
        self.update_file_list()
    
    def choose_directory(self):
        # Choisir un nouveau répertoire
        directory = filedialog.askdirectory(initialdir=self.current_directory)
        if directory:
            self.current_directory = directory
            self.update_file_list()
    
    def copy_files(self):
        # Copier les fichiers sélectionnés
        selections = self.file_listbox.curselection()
        if not selections:
            messagebox.showinfo("Information", "Aucun fichier sélectionné")
            return
        
        destination = filedialog.askdirectory(title="Choisir le dossier de destination")
        if not destination:
            return
        
        for index in selections:
            item = self.file_listbox.get(index).split(" ", 1)[1]
            src_path = os.path.join(self.current_directory, item)
            dst_path = os.path.join(destination, item)
            
            try:
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dst_path)
                else:
                    shutil.copy2(src_path, dst_path)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la copie : {e}")
        
        messagebox.showinfo("Succès", "Fichiers copiés avec succès")
    
    def cut_files(self):
        # Couper les fichiers sélectionnés
        selections = self.file_listbox.curselection()
        if not selections:
            messagebox.showinfo("Information", "Aucun fichier sélectionné")
            return
        
        destination = filedialog.askdirectory(title="Choisir le dossier de destination")
        if not destination:
            return
        
        for index in selections:
            item = self.file_listbox.get(index).split(" ", 1)[1]
            src_path = os.path.join(self.current_directory, item)
            dst_path = os.path.join(destination, item)
            
            try:
                shutil.move(src_path, dst_path)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du déplacement : {e}")
        
        self.update_file_list()
        messagebox.showinfo("Succès", "Fichiers déplacés avec succès")
    
    def delete_files(self):
        # Supprimer les fichiers sélectionnés (envoi dans la corbeille)
        selections = self.file_listbox.curselection()
        if not selections:
            messagebox.showinfo("Information", "Aucun fichier sélectionné")
            return
        
        # Confirmation de suppression
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ces fichiers ?"):
            for index in reversed(selections):  # En ordre inverse pour éviter les problèmes d'indexation
                item = self.file_listbox.get(index).split(" ", 1)[1]
                path = os.path.join(self.current_directory, item)
                
                try:
                    send2trash.send2trash(path)
                except Exception as e:
                    messagebox.showerror("Erreur", f"Erreur lors de la suppression : {e}")
            
            self.update_file_list()
            messagebox.showinfo("Succès", "Fichiers supprimés avec succès")
    
    def rename_file(self):
        # Renommer un fichier
        selections = self.file_listbox.curselection()
        if len(selections) != 1:
            messagebox.showinfo("Information", "Sélectionnez un seul fichier à renommer")
            return
        
        index = selections[0]
        old_name = self.file_listbox.get(index).split(" ", 1)[1]
        old_path = os.path.join(self.current_directory, old_name)
        
        # Boîte de dialogue pour le nouveau nom
        new_name = tk.simpledialog.askstring("Renommer", "Entrez le nouveau nom :", initialvalue=old_name)
        
        if new_name:
            new_path = os.path.join(self.current_directory, new_name)
            try:
                os.rename(old_path, new_path)
                self.update_file_list()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du renommage : {e}")
    
    def compress_files(self):
        # Compresser les fichiers sélectionnés
        selections = self.file_listbox.curselection()
        if not selections:
            messagebox.showinfo("Information", "Aucun fichier sélectionné")
            return
        
        # Choisir le dossier de destination
        destination = filedialog.askdirectory(title="Choisir le dossier de destination")
        if not destination:
            return
        
        # Nom du fichier zip
        zip_name = tk.simpledialog.askstring("Compression", "Nom du fichier zip :", initialvalue="archive.zip")
        if not zip_name:
            return
        
        zip_path = os.path.join(destination, zip_name)
        
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for index in selections:
                    item = self.file_listbox.get(index).split(" ", 1)[1]
                    full_path = os.path.join(self.current_directory, item)
                    
                    if os.path.isdir(full_path):
                        # Compresser récursivement pour les dossiers
                        for root, dirs, files in os.walk(full_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, os.path.dirname(full_path))
                                zipf.write(file_path, arcname=os.path.join(item, arcname))
                    else:
                        zipf.write(full_path, arcname=item)
            
            messagebox.showinfo("Succès", "Fichiers compressés avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la compression : {e}")


