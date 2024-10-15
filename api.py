import requests


url = 'https://api.mangadex.org/manga'
params = {'title': 'One Piece'}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    data1 = data['data']
    lendata = len(data1)
    for i in range (lendata):
        data_json = data1[i]
        title = data_json['attributes']['title']['en']
        print('Title:', title)

else:
    print('Erro:', response.status_code)
