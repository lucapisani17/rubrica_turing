import tkinter as tk #equivalente di SWING
from tkinter import ttk, messagebox

import os #per i file

#per mysql pip install mysql-connector-python
import mysql.connector  
from mysql.connector import Error 
import configparser 


class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.config_file = "credenziali_database.properties"
        self.load_config()
    
    def load_config(self):
        config = configparser.ConfigParser()
        self.host = "localhost"
        self.port = "3306" 
        self.database = "rubrica"
        self.username = "rubrica_user"
        self.password = "lucapisani"
        
        if os.path.exists(self.config_file):
            try:
                config.read(self.config_file)
                if 'DATABASE' in config:
                    self.host = config['DATABASE'].get('host', self.host)
                    self.port = config['DATABASE'].get('port', self.port)
                    self.database = config['DATABASE'].get('database', self.database)
                    self.username = config['DATABASE'].get('username', self.username)
                    self.password = config['DATABASE'].get('password', self.password)
            except Exception as e:
                print(f"Errore nel caricamento configurazione: {e}")
        else:
            self.create_default_config()
    
    def create_default_config(self):
        config = configparser.ConfigParser()
        config['DATABASE'] = {
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'username': self.username,
            'password': self.password
        }
        try:
            with open(self.config_file, 'w') as f:
                config.write(f)
        except Exception as e:
            print(f"Errore nella creazione configurazione: {e}")
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=int(self.port),
                database=self.database,
                user=self.username,
                password=self.password
            )
            if self.connection.is_connected():
                print("Connesso al database MySQL")
                return True
        except Error as e:
            print(f"Errore di connessione: {e}")
            messagebox.showerror("Errore Database", f"Impossibile connettersi al database:\n{e}")
            return False
        return False
    
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Disconnesso dal database")
    
    def create_tables(self):
        if not self.connection or not self.connection.is_connected():
            return False
        
        try:
            cursor = self.connection.cursor()
            
            create_persone_table = """
            CREATE TABLE IF NOT EXISTS persone (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                cognome VARCHAR(100) NOT NULL,
                indirizzo VARCHAR(200),
                telefono VARCHAR(20),
                eta INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            create_utenti_table = """
            CREATE TABLE IF NOT EXISTS utenti (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            cursor.execute(create_persone_table)
            cursor.execute(create_utenti_table)
            
            cursor.execute("SELECT COUNT(*) FROM utenti")
            if cursor.fetchone()[0] == 0:
                default_users = [
                    ("admin", "admin"),
                    ("user", "123"),
                    ("mario", "password")
                ]
                insert_user_query = "INSERT INTO utenti (username, password) VALUES (%s, %s)"
                cursor.executemany(insert_user_query, default_users)
            
            self.connection.commit()
            cursor.close()
            print("Tabelle create/verificate con successo")
            return True
            
        except Error as e:
            print(f"Errore nella creazione tabelle: {e}")
            return False



class Persona:
    def __init__(self,nome, cognome, indirizzo, telefono, eta, id=None):
        self.id = id 
        self.nome = nome
        self.cognome=cognome
        self.indirizzo=indirizzo
        self.telefono=telefono
        self.eta=eta
    def __str__(self):
        return f"{self.nome} {self.cognome} - {self.telefono} - {self.eta} anni - {self.indirizzo}"


class Lista:
    def __init__(self):
        self.persone = []
        self.db_manager = DatabaseManager()  
        
        if self.db_manager.connect():  
            self.db_manager.create_tables()  
        else:
            messagebox.showerror("Errore", "Impossibile connettersi al database!")
    
    def aggiungi(self, nome, cognome, indirizzo, telefono, eta):
        try:
            eta = int(eta)
            
            if not self.db_manager.connection or not self.db_manager.connection.is_connected():
                print("Connessione al database non disponibile")
                return False
            
            cursor = self.db_manager.connection.cursor()
            query = """
            INSERT INTO persone (nome, cognome, indirizzo, telefono, eta) 
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (nome, cognome, indirizzo, telefono, eta)
            
            cursor.execute(query, values)
            self.db_manager.connection.commit()
            
            person_id = cursor.lastrowid
            cursor.close()
            
            persona = Persona(nome, cognome, indirizzo, telefono, eta, person_id)
            self.persone.append(persona)
            
            print(f"Persona aggiunta: {persona}")
            return True
            
        except ValueError:
            print("Il valore inserito come età non è intero")
            return False
        except Error as e:
            print(f"Errore nell'inserimento: {e}")
            return False
    
    def modifica(self, indice, nome=None, cognome=None, indirizzo=None, telefono=None, eta=None):
        if 0 <= indice < len(self.persone):
            try:
                persona = self.persone[indice]
                
                if not self.db_manager.connection or not self.db_manager.connection.is_connected():
                    return False
                
                cursor = self.db_manager.connection.cursor()
                
                if nome: persona.nome = nome
                if cognome: persona.cognome = cognome
                if indirizzo: persona.indirizzo = indirizzo
                if telefono: persona.telefono = telefono
                if eta: persona.eta = int(eta)
                
                query = """
                UPDATE persone 
                SET nome=%s, cognome=%s, indirizzo=%s, telefono=%s, eta=%s 
                WHERE id=%s
                """
                values = (persona.nome, persona.cognome, persona.indirizzo, 
                         persona.telefono, persona.eta, persona.id)
                
                cursor.execute(query, values)
                self.db_manager.connection.commit()
                cursor.close()
                
                print(f"Modificata la persona: {persona}")
                return True
                
            except (ValueError, Error) as e:
                print(f"Errore nella modifica: {e}")
                return False
        return False
    
    def elimina(self, indice):
        if 0 <= indice < len(self.persone):
            try:
                persona = self.persone[indice]
                
                if not self.db_manager.connection or not self.db_manager.connection.is_connected():
                    return False
                
                cursor = self.db_manager.connection.cursor()
                query = "DELETE FROM persone WHERE id = %s"
                cursor.execute(query, (persona.id,))
                self.db_manager.connection.commit()
                cursor.close()
                
                self.persone.pop(indice)
                print(f"Eliminata la persona: {persona}")
                return True
                
            except Error as e:
                print(f"Errore nell'eliminazione: {e}")
                return False
        return False
    
    def carica_da_database(self):  
        try:
            if not self.db_manager.connection or not self.db_manager.connection.is_connected():
                return False
            
            cursor = self.db_manager.connection.cursor()
            query = "SELECT id, nome, cognome, indirizzo, telefono, eta FROM persone ORDER BY cognome, nome"
            cursor.execute(query)
            
            self.persone = []
            for row in cursor.fetchall():
                id, nome, cognome, indirizzo, telefono, eta = row
                persona = Persona(nome, cognome, indirizzo, telefono, eta, id)
                self.persone.append(persona)
            
            cursor.close()
            print(f"Caricate {len(self.persone)} persone dal database")
            return True
            
        except Error as e:
            print(f"Errore nel caricamento: {e}")
            return False
    
    def mostra_tutti(self):
        if not self.persone:
            print("Rubrica vuota")
        else:
            for i, persona in enumerate(self.persone):
                print(f"[{i}] {persona}")
    
    def __del__(self):  
        if hasattr(self, 'db_manager'):
            self.db_manager.disconnect()

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
        
        if not self.rubrica.carica_da_database():  
            self.rubrica.aggiungi("Steve", "Jobs", "via Cupertino 13", "0612344", 56)
            self.rubrica.aggiungi("Bill", "Gates", "via Redmond 10", "06688989", 60)
            self.rubrica.aggiungi("Babbo", "Natale", "via del Polo Nord", "00000111", 99)

        self.root = tk.Tk()
        self.root.title("Rubrica Contatti - Database MySQL")
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
        ttk.Button(button_frame, text="Aggiorna", command=self.aggiorna).pack(side=tk.LEFT, padx=10) 

    def aggiorna(self):
        if self.rubrica.carica_da_database():
            self.refresh_table()
            messagebox.showinfo("Aggiornamento", "Dati ricaricati dal database!")
    
    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for persona in self.rubrica.persone:
            self.tree.insert("", tk.END, values=(persona.nome, persona.cognome, persona.telefono))
    
    def nuovo(self):
        editor = Editor(self.root, self.rubrica)
        self.root.wait_window(editor.window)
        
        if editor.result == "saved":
            self.refresh_table()
            messagebox.showinfo("Successo", "Persona aggiunta con successo!")
    
    def modifica(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona una persona da modificare!")
            return
        
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
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"600x400+{x}+{y}")
    
    def run(self):
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

        self.db_manager = DatabaseManager()

        if not self.db_manager.connect():
            messagebox.showerror("Errore", "Impossibile connettersi al database per il login!")
            return
        
        self.db_manager.create_tables()
        
        self.window = tk.Tk()
        self.window.title("Login - Rubrica Contatti MySQL")
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
        
        try:
            cursor = self.db_manager.connection.cursor()
            query = "SELECT id, username FROM utenti WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                self.login_successful = True
                self.window.destroy()
                return
            else:
                messagebox.showerror("Errore Login", "Username o password non corretti!")
                self.password_entry.delete(0, tk.END)
                self.username_entry.focus()
                
        except Error as e:
            messagebox.showerror("Errore Database", f"Errore durante il login:\n{e}")
    
    
    def center_window(self):
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (300 // 2)
        y = (self.window.winfo_screenheight() // 2) - (200 // 2)
        self.window.geometry(f"300x200+{x}+{y}")
    
    def run(self):
        self.window.mainloop()
        self.db_manager.disconnect()
        return self.login_successful

if __name__ == "__main__":
    app = Login()
    login_ok = app.run()
    
    if login_ok:
        app = Interfaccia()
        app.run()
    else:
        print("Accesso negato")
        

