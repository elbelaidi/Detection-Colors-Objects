import os
import subprocess

def main():
    while True:
        print("Selectionnez le fichier a executer :")
        print("1. Pour detection de couleurs")
        print("2. Pour detection d'objets")
        print("3. Exit")
        
        choice = input("Entrez le numero correspondant a votre choix: ")

        if choice == '1':
            print("Pour detection de couleurs")
            subprocess.run(['python', 'detect_color.py'])
        elif choice == '2':
            print("Pour detection d'objets")
            subprocess.run(['python', 'detect.py', '--source', '0'])
        elif choice == '3':
            print("Exit")
            break
        else:
            print("Choix invalide. Veuillez reessayer.")

if __name__ == "__main__":
    main()
