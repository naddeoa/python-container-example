import requests
import pandas as pd

container_url = 'http://localhost:8000/log'
password = 'password'

cars = {'Brand': ['Honda Civic','Toyota Corolla','Ford Focus','Audi A4'],
      'Price': [22000,25000,27000,35000] }


df = pd.DataFrame(cars, columns = ['Brand', 'Price'])
multiple = df.to_dict(orient="split")
del multiple['index'] # min/max request size
payload = {
    'datasetId': 'model-33',
    'multiple': multiple,
    'timestamp': 1678997916000 # Optional. leave out for "now"
}

response = requests.post(container_url, json = payload, headers={'Authorization': f'Bearer {password}'})
print(response)