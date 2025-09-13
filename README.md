# Rubrica Contatti

Applicazione Python per la gestione di contatti personali con interfaccia grafica tkinter e database MySQL.

## Caratteristiche

- Interfaccia grafica
- Login
- Aggiunta, modifica, eliminazione contatti
- Persistenza dati su database MySQL / file di testo

## Prerequisiti

- Python 3.7+
- MySQL Server

## Installazione

1. **Installa MySQL** e avvialo
2. **Crea il database:**
   ```bash
   mysql -u root -p < schema_database.sql
   ```
3. **Installa dipendenze Python:**
   ```bash
   pip install mysql-connector-python
   ```
4. **Avvia l'applicazione:**
   ```bash
   python main.py
   ```

## Configurazione

L'applicazione crea automaticamente il file `credenziali_database.properties`. Modificalo se necessario con le tue credenziali MySQL:

```ini
[DATABASE]
host = localhost
port = 3306
database = rubrica
username = root
password = la_tua_password
```

## Login

Credenziali di default:
- Username: `admin` - Password: `admin`
- Username: `user` - Password: `123`
- Username: `mario` - Password: `password`

## Struttura del progetto

```
├── main.py                 # Entry point
├── schema_database.sql     # Script creazione database
├── database_manager.py     # Gestione database
├── persona.py             # Modello Persona
├── utente.py              # Modello Utente
├── lista.py               # Repository contatti
├── editor.py              # Dialog editor
├── interfaccia.py         # GUI principale
└── login.py               # Dialog login
```

## Funzionalità

- **Login**: Autenticazione utenti
- **Gestione contatti**: Aggiungi, modifica, elimina persone dalla rubrica
- **Interfaccia grafica**: Tabella con visualizzazione contatti
- **Persistenza**: Salvataggio automatico su database MySQL
