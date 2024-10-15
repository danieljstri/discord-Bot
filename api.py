import requests
import json
from datetime import datetime, timedelta
from keys import access_token


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

    date_published = jsonresponse['data'][0]['attributes']['publishAt'].split('T')[0]
    date_today = datetime.now().isoformat().split('T')[0]
    chapter_url = f'https://mangadex.org/chapter/{jsonresponse["data"][0]["id"]}'

    return {'have_new': date_published == date_today, 'chapter_url': chapter_url}