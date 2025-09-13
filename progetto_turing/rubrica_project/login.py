import tkinter as tk
from tkinter import ttk, messagebox
from database_manager import DatabaseManager
from mysql.connector import Error

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
        """Centra la finestra sullo schermo"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (300 // 2)
        y = (self.window.winfo_screenheight() // 2) - (200 // 2)
        self.window.geometry(f"300x200+{x}+{y}")
    
    def run(self):
        """Avvia la finestra di login"""
        self.window.mainloop()
        self.db_manager.disconnect()
        return self.login_successful