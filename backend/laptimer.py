import requests # type: ignore

#Crear una nueva session en la base de datos para esta sesion

start_line = "from Postgress database using track id in current_session_settings.json"
finish_line = "from Postgress database using track id in current_session_settings.json"
session_best_lap = "from Postgress database using current session uuid"
open_weather_api_key = '8cf215b6d4b2a40546b8e3ed97aa56e6'
location = "Daventry"
initial_latitude = 52.07683  # Ejemplo: latitud de Cambridge, Reino Unido
initial_longitude = 1.05000  # Ejemplo: longitud de Cambridge, Reino Unido

class Weather:
    def __init__(self, initial_latitude, initial_longitude, open_weather_api_key):
        self.initial_longitude = initial_longitude
        self.initial_latitude = initial_latitude
        self.open_weather_api_key = open_weather_api_key

    def get_weather(self):
        # Realizamos la solicitud a la API de OpenWeatherMap
        weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={initial_latitude}&lon={initial_longitude}&units=metric&appid={open_weather_api_key}")
        
        # Comprobamos si la ciudad fue encontrada
        if weather_data.json()['cod'] == '404':
            print("City not found")
        else:
            # Extraemos la información de la respuesta
            weather = weather_data.json()['weather'][0]['main']
            temp = round(weather_data.json()['main']['temp'])
            print(f"The weather is: {weather}")
            print(f"The temperature is: {temp}")
            print(f'{weather_data.json()}')


# Función principal que ejecuta la lógica
def main():
    # Creamos una instancia de la clase Weather
    weather = Weather(initial_latitude,initial_longitude, open_weather_api_key)
    weather.get_weather()



if __name__ == '__main__':
    main()
    
    
    