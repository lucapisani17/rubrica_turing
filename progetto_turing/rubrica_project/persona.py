class Persona:
    def __init__(self, nome, cognome, indirizzo, telefono, eta, id=None):
        self.id = id 
        self.nome = nome
        self.cognome = cognome
        self.indirizzo = indirizzo
        self.telefono = telefono
        self.eta = eta
        
    def __str__(self):
        return f"{self.nome} {self.cognome} - {self.telefono} - {self.eta} anni - {self.indirizzo}"