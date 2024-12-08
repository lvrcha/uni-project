from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/') # интерфейс
def home():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    latitude = request.form['latitude']
    longitude = request.form['longitude']

    api_key = 'VMfkL1TfXobJKA0GRZ8EnA6daU7kZNQW'

    # url для запроса api
    url = f"http://dataservice.accuweather.com/currentconditions/v1/{latitude},{longitude}?apikey={api_key}&language=ru-ru"

    try:
        response = requests.get(url)
        response.raise_for_status()  # проверка  на ошибки статуса http
        data = response.json()

        # извлечение данных (температура, влажность, скорость ветра, % выпадения осадков)
        temperature = data[0]['Temperature']['Metric']['Value']
        humidity = data[0]['RelativeHumidity']
        wind_speed = data[0]['Wind']['Speed']['Metric']['Value']
        precipitation_probability = data[0]['PrecipitationProbability']

        return render_template('result.html',
                               temperature=temperature,
                               humidity=humidity,
                               wind_speed=wind_speed,
                               precipitation_probability=precipitation_probability)
    except Exception as e:
        return f"Ошибка получения данных: {e}"

if __name__ == '__main__':
    app.run(debug=True)
