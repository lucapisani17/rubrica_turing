import mysql.connector  
from mysql.connector import Error 
import configparser 
import os
from tkinter import messagebox

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
        self.username = "root"
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