import requests
import json
from bs4 import BeautifulSoup

def parse_games():
    url = ''
    term = input('Введите вид контента, или ссылку на запрос: ')
    count = input('Введите количество страниц с игрой: ')
    if 'https' in url:
        url = term
    else:
    # URL страницы для парсинга
        url = (
        'https://store.steampowered.com/search/results/?'
        'query&'
        'start=0&'
        'count={count}&'
        'dynamic_data=&'
        'sort_by=_ASC&'
        'term={term}&'
        'snr=1_7_7_151_7&'
        'infinite=1'
        )

    # Параметры запроса
    params = {
        "term": term,
        "count": count
    }

    try:
        # Выполняем GET-запрос с указанными параметрами
        response = requests.get(url.format(**params)).json()
        response['results_html'] = response['results_html'].replace('\\', '')
        # Создаем объект BS для парсинга HTML страницы
        soup = BeautifulSoup(response['results_html'], 'html.parser')
        
        

        # Находим все элементы с названиями игр
        game_titles = soup.find_all("span", attrs={'class': 'title'})
        game_links = soup.find_all("a", attrs={'class': 'search_result_row'})

        game_data = [] #Список куда запишем результат

        # Перебираем найденные элементы и выводим результаты
        for title, link in zip(game_titles, game_links):
            title = title.text.strip()
            link = link['href']
            data = {
                'title': title,
                'link': link,
            }
            game_data.append(data)
        #Записываем в json файл
        with open('games.json', 'w') as file:
            json.dump(game_data, file)
        #Выводим результат
        for game in game_data:
            print(f'Game: {game["title"]}')
            print(f'Link: {game["link"]}' + '\n')

    except Exception as e:
        print(f"Error: {e}")

# Вызываем функцию для парсинга
parse_games()