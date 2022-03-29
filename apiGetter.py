import requests

apiId = 'b5c29c0d0cd7e9968a4f36e5501afb72'
lat = 39.4833
long = 87.3241
request = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={apiId}"


def get_temp():
    response = requests.get(request)
    json_data = response.json()

    current_temp_in_k = json_data['main']['temp']

    current_temp = k_to_f(current_temp_in_k)
    print(current_temp)


def k_to_f(temp_in_k):
    return temp_in_k * 1.8 - 459.67
