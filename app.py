from flask import Flask, render_template, url_for
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, redirect
import datetime

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


client = MongoClient('mongodb://localhost:27017/')
db = client['Proiect_preFinal']  # replace with your database name
collection = db['Angajat']  # replace with your collection name


@app.route('/employees', methods=['GET'])
def get_employees():
    employees = []
    for i in collection.find().sort('Departament'):
        employees.append(i)
    return render_template('employees.html', employees=employees)


@app.route('/employees/average-salary', methods=['GET'])
def get_average_salary():
    avg_salary = collection.aggregate([{"$group": {"_id": "", "average_salary": {"$avg": "$Salariu"}}}])
    return jsonify({'Salariul mediu al angajatilor este:': list(avg_salary)[0]['average_salary']})


@app.route('/employees_dep', methods=['GET', 'POST'])
def get_employees_dep():
    if request.method == "POST":
        dep = request.form.get("dep")
        return view(dep)
    return render_template('form.html')


def view(dep):
    employees = []
    for i in collection.find({'Departament': dep}):
        employees.append(i)
    return render_template('employees.html', employees=employees)


lista_departamente = []


def load_lista_departamente():
    for i in collection.find({}, {'_id': 0}):
        for x, y in i.items():
            if x == "Departament" and y not in lista_departamente:
                lista_departamente.append(y)


@app.route('/employees_per_dep', methods=['GET'])
def get_employees_per_dep():
    dep_len = {}
    load_lista_departamente()
    for departament in lista_departamente:
        results = collection.find({"Departament": {"$exists": True}})
        x = [angajat for angajat in filter(lambda x: x['Departament'] == departament, results)]
        dep_len[departament] = len(x)
    return dep_len

@app.route('/employees_year', methods=['GET', 'POST'])
def get_employees_year():
    results = collection.find({"Data_Angajarii": {"$exists": True}})
    if request.method == "POST":
        an = request.form.get("an")
        x = [angajat for angajat in
             filter(lambda x: (datetime.datetime.now() - x['Data_Angajarii']).days > int(an) * 365, results)]
        return f"In firma sunt {len(x)} angajati mai vechi de {an} ani."
    return render_template('form2.html')



if __name__ == '__main__':
    app.run(debug=True)
