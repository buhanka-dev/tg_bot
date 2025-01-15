import requests
client_id = 'aad7942d3c39434'


def upload_to_imgur(image_url):
    # Загружаем изображение по URL
    response = requests.get(image_url, timeout=10000)

    if response.status_code == 200:
        print(200)
        # Если изображение успешно загружено, загружаем на Imgur
        headers = {
            'Authorization': f'Client-ID {client_id}',
        }

        # Подготовим данные для отправки
        data = {
            'image': response.content,
            'type': 'file',
        }

        # Отправляем POST-запрос на загрузку изображения
        upload_response = requests.post('https://api.imgur.com/3/image', headers=headers, files=data)

        if upload_response.status_code == 200:
            json_response = upload_response.json()
            print(json_response['data']['link'])
            return json_response['data']['link']
        else:
            print('Error uploading image:', upload_response.json)