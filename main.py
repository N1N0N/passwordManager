import sys

from cryptography.fernet import Fernet
import os
import time
#Funktion um MasterKey zu generaten
def generateKey():
    if os.path.exists('key.key'):
        os.remove('key.key')

    key = Fernet.generate_key()

    with open('key.key', 'wb') as masterPw:
        masterPw.write(key)
    return key.decode('utf-8')


#Wird das Programm das erste mal gestartet? Falls ja KeyGen und data.txt file
def firstStart():
    if not os.path.exists('key.key'):
        print("Willkommen zum Password Manager!")
        generateFirstKey = input("Um fortzufahren musst du einen Master Key generieren. Willst du fortfahren? (Y/n): ")
        if generateFirstKey.lower() == 'y':
            key = generateKey()
            print(f"Dein Key lautet: '{key}' speicher ihn gut ab!")
            with open('data.txt', 'w') as data:
                data.write('')
    else:
        print("Willkommen zurueck!")


# Password encryption prozess
def encrypt_password(password, key):
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password.decode()


# Password decryption prozess
def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password.encode())
    return decrypted_password.decode()


# Neue Passwoerter
def addData():
    with open('key.key', 'rb') as key_file:
        key = key_file.read()

    while True:
        platform = input("Platform: ")
        name = input("Name: ")
        password = input("Password: ")
        encrypted_password = encrypt_password(password, key)

        with open("data.txt", "a") as data:
            data.write(name + "|" + encrypted_password + "|" + platform + "\n")
        addAnother = input("Willst du ein neues Passwort hinzufuegen? (Y/n): ")
        if addAnother.lower() == 'y':
            continue
        else:
            break


# Passwoerter auflisten
def listData():
    with open('key.key', 'rb') as key_file:
        key = key_file.read()

    with open('data.txt', 'r') as data:
        for line in data:
            strippedLine = line.rstrip()
            name, encrypted_password, platform = strippedLine.split("|")
            password = decrypt_password(encrypted_password, key)
            print(f"Plattform: {platform} | Username: {name} | Password: {password}")


# main / alles handlen und richtig ausfuehren
def main():
    authenticated = False
    while True:
        if not os.path.exists('key.key'):
            firstStart()

        if not authenticated:
            masterQuery = input("Geb den Master Key ein: ")
            with open('key.key', 'r') as masterPw:
                if masterPw.read() == masterQuery:
                    print("Richtig!")
                    authenticated = True
                else:
                    print("Falscher Master Key. Bitte versuche es erneut.")
                    continue

        decision = input(
            "Willst du deine Passwoerter auflisten, ein Passwort hinzufuegen, einen neuen Master Key erstellen oder das Programm verlassen? (list, add, new, exit): ")
        if decision == 'list':
            listData()
        elif decision == 'add':
            addData()
        elif decision == 'new':
            newKeyConfirmation = input("Bist du dir sicher? Das Programm sich bei Generation eines neuen MasterKeys schliessen und alle Passwoerter aus der Liste loeschen? (Y/n): ")
            if newKeyConfirmation == 'Y':
                open('data.txt', 'w').close()
                newKey = generateKey()
                print(f"Neuer MasterKey erfolgreich generiert. Er lautet: '{newKey}'. Speicher ihn gut ab!")
                print("Das Programm schliesst sich in 10 Sekunden")
                time.sleep(10)
                sys.exit()


            else:
                continue
        elif decision == 'exit':
            print("Programm beendet.")
            break
        else:
            print("Ungueltige Eingabe. Bitte versuche es erneut.")


if __name__ == '__main__':
    main()
