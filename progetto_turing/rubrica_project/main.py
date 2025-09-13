from login import Login
from interfaccia import Interfaccia

if __name__ == "__main__":
    app = Login()
    login_ok = app.run()
    
    if login_ok:
        app = Interfaccia()
        app.run()
    else:
        print("Accesso negato")