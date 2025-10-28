from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)
backend_url = os.getenv('BACKEND_URL', 'localhost')

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        date_value = request.form['date']
        data = {'date': date_value}
        try:
            requests.post(f"{backend_url}/save", json=data)
            message = "Date submitted successfully!"
        except Exception as e:
            message = f"Error: {e}"

    # Fetch the list of saved dates
    try:
        res = requests.get(f"{backend_url}/list")
        records = res.json()
    except Exception:
        records = []

    return render_template('index.html', message=message, records=records)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

