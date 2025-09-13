import tkinter as tk #equivalente di SWING
from tkinter import ttk, messagebox

import os #per i file

class Persona:
    def __init__(self,nome, cognome, indirizzo, telefono, eta):
        self.nome = nome
        self.cognome=cognome
        self.indirizzo=indirizzo
        self.telefono=telefono
        self.eta=eta
    def __str__(self):
        return f"{self.nome} {self.cognome} - {self.telefono} - {self.eta} anni - {self.indirizzo}"


class Lista:
    def __init__(self):
        self.persone=[]
        self.nome_file = "informazioni.txt"
    
    def aggiungi(self,nome, cognome, indirizzo, telefono, eta):
        try:
            eta = int(eta)
            persona = Persona(nome, cognome, indirizzo, telefono, eta)
            self.persone.append(persona)
            self.salva_su_file()
            return True
        except ValueError:
            print("Il valore inserito come eta' non è intero")
            return False
        
    def modifica(self, indice, nome=None, cognome=None, indirizzo=None, telefono=None, eta=None):
        if 0 <= indice < len(self.persone):
            p = self.persone[indice]
            if nome: p.nome = nome
            if cognome: p.cognome = cognome  
            if indirizzo: p.indirizzo = indirizzo
            if telefono: p.telefono = telefono
            if eta: p.eta = eta
            print(f"modificata la persona: {p}")
            self.salva_su_file()
            return True  
        return False  

    def elimina(self, indice):
        if 0 <= indice < len(self.persone):
            persona = self.persone.pop(indice)
            print(f"eliminata la persona: {persona}")
            self.salva_su_file()
            return True  
        else:
            print("Indice non trovato")
            return False  
    
    def mostra_tutti(self):
        if not self.persone:
            print("Rubrica vuota")
        else:
            for i, persona in enumerate(self.persone):
                print(f"[{i}] {persona}")
    
    def salva_su_file(self):
        try:
            with open(self.nome_file, 'w', encoding='utf-8') as file:
                for persona in self.persone:
                    linea = f"{persona.nome};{persona.cognome};{persona.indirizzo};{persona.telefono};{persona.eta}\n"
                    file.write(linea)
            return True
        except Exception as e:
            print(f"Errore nel salvataggio: {e}")
            return False
        
    def carica_da_file(self):
        try:
            if not os.path.exists(self.nome_file):
                print("File informazioni.txt non trovato")
                return False
            
            with open(self.nome_file, 'r', encoding='utf-8') as file:
                self.persone = []
                
                for linea in file:
                    linea = linea.strip()
                    if linea:
                        parti = linea.split(';')
                        if len(parti) == 5:
                            nome, cognome, indirizzo, telefono, eta = parti
                            try:
                                eta = int(eta)
                                persona = Persona(nome, cognome, indirizzo, telefono, eta)
                                self.persone.append(persona)
                            except ValueError:
                                print(f"Errore nell'età per: {nome} {cognome}")
            return True
        except Exception as e:
            print(f"Errore nel caricamento: {e}")
            return False

class Editor:
    def __init__(self, parent, rubrica, persona_index=None):
        self.parent = parent
        self.rubrica = rubrica
        self.persona_index = persona_index
        self.result = None

        self.window = tk.Toplevel(parent)
        self.window.title("Editor Persona")
        self.window.geometry("400x350")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_widgets()
        self.center_window()
        
        if persona_index is not None:
            self.load_persona_data()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.nome_entry = ttk.Entry(main_frame, width=30)
        self.nome_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Cognome:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cognome_entry = ttk.Entry(main_frame, width=30)
        self.cognome_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Indirizzo:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.indirizzo_entry = ttk.Entry(main_frame, width=30)
        self.indirizzo_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Telefono:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.telefono_entry = ttk.Entry(main_frame, width=30)
        self.telefono_entry.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Eta':").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.eta_entry = ttk.Entry(main_frame, width=30)
        self.eta_entry.grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Salva", command=self.salva_dati).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Annulla", command=self.annulla).pack(side=tk.LEFT, padx=10)
        
        self.nome_entry.focus()

    def carica_dati(self):
        persona = self.rubrica.persone[self.persona_index]
        self.nome_entry.insert(0, persona.nome)
        self.cognome_entry.insert(0, persona.cognome)
        self.indirizzo_entry.insert(0, persona.indirizzo)
        self.telefono_entry.insert(0, persona.telefono)
        self.eta_entry.insert(0, str(persona.eta))

    def salva_dati(self):
        nome = self.nome_entry.get().strip()
        cognome = self.cognome_entry.get().strip()
        indirizzo = self.indirizzo_entry.get().strip()
        telefono = self.telefono_entry.get().strip()
        eta = self.eta_entry.get().strip()
        if not nome or not cognome:
            messagebox.showerror("Errore", "Nome e cognome sono obbligatori!")
            return
        
        if not eta.isdigit():
            messagebox.showerror("Errore", "L'età deve essere un numero intero!")
            return
        if self.persona_index is None:
            if self.rubrica.aggiungi(nome, cognome, indirizzo, telefono, eta):
                self.result = "saved"
                self.window.destroy()
            else:
                messagebox.showerror("Errore", "Errore nel salvataggio!")
        else:
            if self.rubrica.modifica(self.persona_index, nome, cognome, indirizzo, telefono, eta):
                self.result = "saved"
                self.window.destroy()
            else:
                messagebox.showerror("Errore", "Errore nella modifica!")

    def annulla(self):
        self.result = "annullato"
        self.window.destroy()

    def center_window(self):
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.window.winfo_screenheight() // 2) - (350 // 2)
        self.window.geometry(f"400x350+{x}+{y}")

    def load_persona_data(self):
        self.carica_dati()
    
class Interfaccia:
    def __init__(self):
        self.rubrica = Lista()
        if not self.rubrica.carica_da_file():
            self.rubrica.aggiungi("Steve", "Jobs", "via Cupertino 13", "0612344", 56)
            self.rubrica.aggiungi("Bill", "Gates", "via Redmond 10", "06688989", 60)
            self.rubrica.aggiungi("Babbo", "Natale", "via del Polo Nord", "00000111", 99)

        self.root = tk.Tk()
        self.root.title("Rubrica Contatti")
        self.root.geometry("600x400")
        
        self.create_widgets()
        self.center_window()
        self.refresh_table()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        

        columns = ("Nome", "Cognome", "Telefono")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        button_frame = ttk.Frame(self.root)
        button_frame.pack(side=tk.BOTTOM, pady=10)
        
        ttk.Button(button_frame, text="Nuovo", command=self.nuovo).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Modifica", command=self.modifica).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Elimina", command=self.elimina).pack(side=tk.LEFT, padx=10)
    
    def refresh_table(self):
        """Aggiorna i dati nella tabella"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for persona in self.rubrica.persone:
            self.tree.insert("", tk.END, values=(persona.nome, persona.cognome, persona.telefono))
    
    def nuovo(self):
        """Apre l'editor per creare una nuova persona"""
        editor = Editor(self.root, self.rubrica)
        self.root.wait_window(editor.window)
        
        if editor.result == "saved":
            self.refresh_table()
            messagebox.showinfo("Successo", "Persona aggiunta con successo!")
    
    def modifica(self):
        """Apre l'editor per modificare la persona selezionata"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona una persona da modificare!")
            return
        
        # Ottieni l'indice della persona selezionata
        item = selection[0]
        index = self.tree.index(item)
        
        editor = Editor(self.root, self.rubrica, index)
        self.root.wait_window(editor.window)
        
        if editor.result == "saved":
            self.refresh_table()
            messagebox.showinfo("Successo", "Persona modificata con successo!")
    
    def elimina(self):
        """Elimina la persona selezionata"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona una persona da eliminare!")
            return
        
        if messagebox.askyesno("Conferma", "Sei sicuro di voler eliminare questa persona?"):
            item = selection[0]
            index = self.tree.index(item)
            
            if self.rubrica.elimina(index):
                self.refresh_table()
                messagebox.showinfo("Successo", "Persona eliminata con successo!")
    
    def center_window(self):
        """Centra la finestra sullo schermo"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"600x400+{x}+{y}")
    
    def run(self):
        """Avvia l'applicazione"""
        self.root.mainloop()

class Utente:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __str__(self):
        return f"Utente: {self.username}"

class Login:
    def __init__(self):
        self.login_successful = False
        self.utenti = [
            Utente("admin", "admin"),
            Utente("user", "123"),
            Utente("mario", "password")
        ]
        
        self.window = tk.Tk()
        self.window.title("Login - Rubrica Contatti")
        self.window.geometry("300x200")
        self.window.resizable(False, False)
        
        self.create_widgets()
        self.center_window()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.window, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="ACCESSO RUBRICA", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        ttk.Label(main_frame, text="Utente:").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.username_entry = ttk.Entry(main_frame, width=20)
        self.username_entry.grid(row=1, column=1, sticky=tk.W, pady=8, padx=(10, 0))
        
        ttk.Label(main_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=8)
        self.password_entry = ttk.Entry(main_frame, width=20, show="*")
        self.password_entry.grid(row=2, column=1, sticky=tk.W, pady=8, padx=(10, 0))
        
        login_button = ttk.Button(main_frame, text="LOGIN", command=self.verifica_login)
        login_button.grid(row=3, column=0, columnspan=2, pady=20)
        
        self.username_entry.focus()
        
        self.window.bind('<Return>', lambda event: self.verifica_login())
    
    def verifica_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        for utente in self.utenti:
            if utente.username == username and utente.password == password:
                self.login_successful = True
                self.window.destroy()
                return
        
        messagebox.showerror("Errore Login", "Username o password non corretti!")
        self.password_entry.delete(0, tk.END) 
        self.username_entry.focus()
    
    def center_window(self):
        """Centra la finestra sullo schermo"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (300 // 2)
        y = (self.window.winfo_screenheight() // 2) - (200 // 2)
        self.window.geometry(f"300x200+{x}+{y}")
    
    def run(self):
        """Avvia la finestra di login"""
        self.window.mainloop()
        return self.login_successful

if __name__ == "__main__":
    app = Login()
    login_ok = app.run()
    
    if login_ok:
        app = Interfaccia()
        app.run()
    else:
        print("Accesso negato")
        

