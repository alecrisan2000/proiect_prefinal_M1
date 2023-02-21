from departament import Departament

from helper import *


class Angajat(Departament):

    def __init__(self, workdep, empname, job, hiredate, salary):
        """ Constructorul clasei Angajat. """
        super().__init__(workdep)
        self.empname = empname
        self.job = job
        self.hiredate = hiredate
        self.__salary = salary
        self.adaugare_angajat()

    def adaugare_angajat(self):
        angajati = databaseConnection("Angajat")
        if angajati.count_documents({"Nume": self.empname}) == 0:
            angajati_dict = {
                "Departament": self.workdep,
                "Nume": self.empname,
                "Functie": self.job,
                "Data_Angajarii": self.hiredate,
                "Salariu": self.__salary,
            }
            angajati.insert_one(angajati_dict)
            Departament.load_lista_departamente()
            print("Angajatul a fost adaugat cu succes.")
        else:
            print("Angajatul exista deja!")

    @classmethod
    def average_salary(cls):
        """ Calculates the average salary of employees in the lista_angajati. """

        angajati = databaseConnection("Angajat")
        results = angajati.find({"Salariu": {"$exists": True}})

        salary_list = [salariu for salariu in map(lambda x: x['Salariu'], results)]
        try:
            average = sum(salary_list) / len(salary_list)
            return f"Salariul mediu al angajatilor este: {round(average, 2)} lei."
        except ArithmeticError:
            print("Nu exista angajati!")

    @classmethod
    def nr_angajati_departament(cls):
        angajati = databaseConnection("Angajat")

        Departament.load_lista_departamente()

        for departament in Departament.lista_departamente:
            results = angajati.find({"Departament": {"$exists": True}})
            x = [angajat for angajat in filter(lambda x: x['Departament'] == departament, results)]
            print(departament, len(x))

    @classmethod
    def angajati_vechime(cls):
        angajati = databaseConnection("Angajat")
        results = angajati.find({"Data_Angajarii": {"$exists": True}})

        an = validare_float("anul")

        x = [angajat for angajat in
             filter(lambda x: (datetime.datetime.now() - x['Data_Angajarii']).days > int(an) * 365, results)]
        print(f"In firma sunt {len(x)} angajati mai vechi de {an} ani.")

        for angajat in x:
            print(f"{angajat['Nume']} s-a angajat in data {angajat['Data_Angajarii'].date()}")


