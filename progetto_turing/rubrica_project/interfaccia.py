import tkinter as tk
from tkinter import ttk, messagebox
from lista import Lista
from editor import Editor

class Interfaccia:
    def __init__(self):
        self.rubrica = Lista()
        
        if not self.rubrica.carica_da_database():  
            self.rubrica.aggiungi("Steve", "Jobs", "via Cupertino 13", "0612344", "56")
            self.rubrica.aggiungi("Bill", "Gates", "via Redmond 10", "06688989", "60")
            self.rubrica.aggiungi("Babbo", "Natale", "via del Polo Nord", "00000111", "99")

        self.root = tk.Tk()
        self.root.title("Rubrica Contatti - Database MySQL")
        self.root.geometry("600x400")
        
        self.create_widgets()
        self.center_window()
        self.refresh_table()

    def create_widgets(self):
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tabella (JTable equivalente in Tkinter)
        # Colonne: Nome, Cognome, Telefono
        columns = ("Nome", "Cognome", "Telefono")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
        
        # Definisci le colonne
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.W)
        
        # Scrollbar per la tabella
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack della tabella e scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame per i bottoni (in basso)
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
        """Aggiorna i dati nella tabella"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Riempi con i dati attuali
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
        
        # Conferma eliminazione
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