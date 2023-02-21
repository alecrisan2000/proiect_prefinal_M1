import sys
from angajati import Angajat
from departament import Departament

from helper import *


def vizualizare_angajati():
    Departament.load_lista_departamente()
    for departament in Departament.lista_departamente:
        print(35 * '=')
        print(departament.center(35))
        print(35 * '=')
        vizualizare_angajati_din_departament(departament)


def vizualizare_angajati_din_departament(departament_cautat):
    angajati = databaseConnection("Angajat")
    flag = 0

    Departament.load_lista_departamente()
    for departament in Departament.lista_departamente:
        if departament.upper() == departament_cautat.upper():
            flag = 1
            for i in angajati.find({'Departament': departament}, {'_id': 0, 'Departament': 0}):
                for x, y in i.items():
                    print(f"{x} : {y}")
                print(35 * '-')
    if flag == 0:
        print("Nu exista acest departament")
        departament = validare_string("departamentul")
        print(departament)
        vizualizare_angajati_din_departament(departament)


def vizualizare():
    while True:
        print(35 * "=")
        print("Vizualizare".center(35))
        print(35 * "=")
        print(""" 
        1. Vizualizare a tuturor angajatilor in functie de departament
        2. Vizualizarea angajatilor dintr-un departament
        3. Iesire la meniul principal
        """)
        match input("Alegeti optiunea: "):
            case '1':
                vizualizare_angajati()
                input("Enter ca sa te intorci la submeniu")
            case '2':
                Departament.load_lista_departamente()
                print("Departamente: " + str(Departament.lista_departamente))
                departament = validare_string("departamentul")
                vizualizare_angajati_din_departament(departament)
                input("Enter ca sa te intorci la submeniu")
            case '3':
                break


def informatii_firma():
    while True:
        print(35 * "=")
        print("Informatii firma".center(35))
        print(35 * "=")
        print(""" 
        1. Afisare medie salariala.
        2. Afisare nr angajati/ departament
        3. Afisare nr de angajati cu vechime mai mare de x ani.
        4. Iesire la meniul principal
        """)

        match input("Alegeti optiunea: "):
            case '1':
                print(Angajat.average_salary())
                input("Enter ca sa te intorci la submeniu")
            case '2':
                Angajat.nr_angajati_departament()
                input("Enter ca sa te intorci la submeniu")
            case '3':
                Angajat.angajati_vechime()
                input("Enter ca sa te intorci la submeniu")
            case '4':
                break


def adaugare_angajati():
    print("Adaugare angajat")
    departament = validare_string("departamentul")
    nume = validare_string("numele angajatului: ")
    functie = validare_string("functia: ")
    while True:
        match input("Doriti sa folositi data de azi? y/n: "):
            case "y":
                data = datetime.datetime.now()
                break
            case "n":
                data = validare_data()
                break
    salariu = validare_float("salariul")
    Angajat(departament, nume, functie, data, salariu)
    input("Enter ca sa te intorci la submeniu")


def stergere_angajat():
    angajati = databaseConnection("Angajat")
    nume = validare_string("numele angajatului: ")
    if angajati.count_documents({"Nume": nume}) == 1:
        angajati.delete_one({"Nume": nume})
        print("Angajatul a fost sters!")
    else:
        print("Angajatul nu exista!")


def modificare_angajat():
    angajati = databaseConnection("Angajat")
    nume = validare_string("numele angajatului: ")
    if angajati.count_documents({"Nume": nume}) == 1:
        atribute = []
        for i in angajati.find({"Nume": nume}, {'_id': 0}):
            for x in i.keys():
                atribute.append(x)
        while True:
            print(f"Atributele ce pot fi modificate sunt: {atribute}")
            atribut_mod = input("Ce doriti sa modificati?")
            if atribut_mod not in atribute:
                print("Nu exista atributul!")
            else:
                if atribut_mod == "Salariu":
                    noua_valoare = validare_float(" noua valoare")
                elif atribut_mod == "Data_Angajarii":
                    noua_valoare = validare_data()
                else:
                    noua_valoare = validare_string("noua valoare")
                angajati.update_one({"Nume": nume}, {"$set": {atribut_mod: noua_valoare}})
                print("Modificarea a fost efectuata cu succes")
                break
    else:
        print("Angajatul nu exista!")


def main():
    """ Functia de main a proiectului. Reprezinta meniul principal"""
    dict_optiuni = {

        "1": vizualizare,
        "2": informatii_firma,
        "3": adaugare_angajati,
        "4": stergere_angajat,
        "5": modificare_angajat,
        "6": sys.exit
    }

    while True:
        print(35 * "=")
        print("Meniu".center(35))
        print(35 * "=")
        print("1. Vizualizare\n2. Informatii despre firma\n3. Adaugare angajati\n4. Stergere angajat\n5. Modificare angajat\n6. Iesire")
        print(35 * "=")

        optiune = input("Introduceti optiune: ")
        # Apelarea optiunii corespunzatoare input-ului
        if optiune in dict_optiuni:
            dict_optiuni[optiune]()
        else:
            print("Nu ati introdus o optiune valida.")


if __name__ == "__main__":
    main()
