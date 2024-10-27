from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
API_BASE_URL = 'http://localhost:5000/api/cars'


@app.route('/')
def indeks():
    response = requests.get(API_BASE_URL)
    cars = response.json() if response.ok else []
    return render_template('index.html', cars=cars, appType='Client-Server')


@app.route('/createcar')
def createcar():
    return render_template('createcar.html', appType='Client-Server')


@app.route('/createcarsave', methods=['POST'])
def createcarsave():
    data = {
        "carname": request.form['carName'],
        "carbrand": request.form['carBrand'],
        "carmodel": request.form['carModel'],
        "carprice": request.form['carPrice']
    }
    requests.post(API_BASE_URL, json=data)
    return redirect(url_for('indeks'))


@app.route('/readcar')
def readcar():
    response = requests.get(API_BASE_URL)
    cars = response.json() if response.ok else []
    return render_template('readcar.html', rows=cars, appType='Client-Server')


@app.route('/updatecar')
def updatecar():
    return render_template('updatecar.html', appType='Client-Server')


@app.route('/updatecarsave', methods=['POST'])
def updatecarsave():
    car_id = request.form['carId']
    data = {
        "carname": request.form['carName'],
        "carbrand": request.form['carBrand'],
        "carmodel": request.form['carModel'],
        "carprice": request.form['carPrice']
    }
    requests.put(f"{API_BASE_URL}/{car_id}", json=data)
    return redirect(url_for('readcar'))


@app.route('/deletecar')
def deletecar():
    return render_template('deletecar.html', appType='Client-Server')


@app.route('/deletecarsave', methods=['POST'])
def deletecarsave():
    car_id = request.form['carId']
    requests.delete(f"{API_BASE_URL}/{car_id}")
    return redirect(url_for('readcar'))


@app.route('/searchcar')
def searchcar():
    return render_template('searchcar.html', appType='Client-Server')


@app.route('/searchcarsave', methods=['POST'])
def searchcarsave():
    search_query = request.form['searchQuery']
    response = requests.get(API_BASE_URL)
    if response.ok:
        cars = response.json()
        results = [
            car for car in cars if search_query.lower() in car['carname'].lower()
            or search_query.lower() in car['carbrand'].lower()
            or search_query.lower() in car['carmodel'].lower()
            or search_query.lower() in car['carprice'].lower()
        ]
    else:
        results = []
    return render_template('searchcar.html', appType='Client-Server', results=results, search_query=search_query)


@app.route('/help')
def help():
    return "ini halaman Helps"


@app.route('/uploadcsv', methods=['GET', 'POST'])
def uploadcsv():
    if request.method == 'POST':
        file = request.files['csvFile']
        if file and file.filename.endswith('.csv'):
            # Membaca file CSV dan mengirim datanya ke API
            df = pd.read_csv(file)
            for _, row in df.iterrows():
                data = {
                    "carname": row.get('name', "null"),
                    "carbrand": row.get('brand', "null"),
                    "carmodel": row.get('model', "null"),
                    "carprice": row.get('price', "null")
                }
                requests.post(API_BASE_URL, json=data)
            return redirect(url_for('readcar'))
    return render_template('uploadcsv.html', appType='Client-Server')


if __name__ == '__main__':
    app.run(port=5010, debug=True)
