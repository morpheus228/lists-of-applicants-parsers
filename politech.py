import requests
import json
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

url = 'https://enroll.spbstu.ru/back/api/statements/lists-applicants?training_level=2&form_education=5&form_payment=4&faculty=4&direction_training=182&benefits=0&page=1&per_page=10&trajectory=1'
page = requests.get(url, verify=False)

data = json.loads(page.text)['data']

results = []

for user_data in data:
    print(user_data['ege'])
# df = pd.DataFrame(data)
# df.to_excel('test.xlsx')
