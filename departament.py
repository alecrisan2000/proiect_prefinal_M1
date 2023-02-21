from helper import *


class Departament:
    # Variabila de clasa care va contine obiecte de tip Departament
    lista_departamente = []

    def __init__(self, workdep):
        """ Constructorul clasei Departament. """
        self.workdep = workdep
        Departament.lista_departamente.append(workdep)

    @classmethod
    def load_lista_departamente(cls):
        angajati = databaseConnection("Angajat")
        for i in angajati.find({}, {'_id': 0}):
            for x, y in i.items():
                if x == "Departament" and y not in Departament.lista_departamente:
                    Departament(y)
