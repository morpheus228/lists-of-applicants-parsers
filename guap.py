from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import xlsxwriter

pd.options.mode.chained_assignment = None


def get_sorted_list(code):
    url = f'https://priem.guap.ru/_lists/List_{code}_14'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    name = soup.find_all('h3')[1].text.strip()
    name = list(name.split('"'))[1]
    name = name[:31]
    places = soup.find_all('h4')[0].text.strip()
    places = list(list(places.split(' ('))[0].split('- '))[1]

    table = soup.find('table', attrs={'class': "table table-hover"})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)

    df = pd.DataFrame(data, columns=['СНИЛС', 'Баллы', 'Сумма ЕГЭ',
                                     'ИД', 'Сумма баллов', 'Преимущественное право',
                                     'Согласие', 'Оригинал'])

    df = df.drop(columns=['Баллы', 'Согласие', 'Оригинал'])
    for column in ['Сумма ЕГЭ', 'ИД', 'Сумма баллов']:
        df = df[df[column].str.isdigit()]
        df[column] = df[column].astype(int)

    df['real_scores'] = df['Преимущественное право'].apply(lambda x: x == 'Да')
    for index in range(len(df)):
        if df['real_scores'].iloc[index] == True:
            df['real_scores'].iloc[index] = float('inf')
        else:
            df['real_scores'].iloc[index] = df['Сумма баллов'].iloc[index]

    df = df.sort_values(by='real_scores', ascending=False)
    df.index = np.arange(len(df)) + 1
    df = df.drop(columns=['real_scores'])

    return df, name, places


writer = pd.ExcelWriter('ГУАП.xlsx', engine='xlsxwriter')

codes = ['1400', '1413', '1694', '1370', '1698']
for code in codes:
    df, name, places = get_sorted_list(code)
    df.to_excel(writer, sheet_name=name)

writer.save()