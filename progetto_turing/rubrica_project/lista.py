from persona_v1 import Persona
from mysql.connector import Error
from database_manager import DatabaseManager
from tkinter import messagebox

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