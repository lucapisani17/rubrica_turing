import tkinter as tk
from tkinter import ttk, messagebox

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