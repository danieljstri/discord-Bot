import requests
import json
from datetime import datetime
# from keys import access_token


def get_new_chapters(manga_id):
    # URL da API MangaDex para capítulos
    url = 'https://api.mangadex.org/chapter'

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Parâmetros para a requisição
    params = {
        'manga': manga_id,
        'translatedLanguage[]': ['pt-br', 'en'],
        'order[publishAt]': 'desc',
    }

    response = requests.get(url, headers=headers, params=params)
    jsonresponse = response.json()
    with open('response.json', 'w') as f:
        json.dump(jsonresponse, f)

    date_published = jsonresponse['data'][0]['attributes']['publishAt'].split('T')[0]
    date_today = datetime.now().isoformat().split('T')[0]
    chapter_url = f'https://mangadex.org/chapter/{jsonresponse["data"][0]["id"]}'

    return {'have_new': date_published == date_today, 'chapter_url': chapter_url}

def get_manga(manga_name):
    url = 'https://api.mangadex.org/manga'

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    params = {
        'title': manga_name,
    }

    response = requests.get(url, headers=headers, params=params)   
    jsonresponse = response.json()
    return jsonresponse['data']

def escolhe_manga(manga_name):
    mangas = get_manga(manga_name)
    message = f'''Escolha o mangá que deseja adicionar:\n'''
    for index in range(len(mangas)):
        message += f'[{index}] - {mangas[index]['attributes']['title']['en']}\n'
    
    return message