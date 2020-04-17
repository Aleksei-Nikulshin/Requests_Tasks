import requests
import os
#  документация https://yandex.ru/dev/translate/doc/dg/reference/translate-docpage/

API_KEY = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

def translate_it(text, to_lang):
    """
    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]
    :param to_lang:
    :return:
    """

    start_path = input("Укажите путь к файлу для перевода: ")
    file_name = input("Введите имя файла для перевода: ")
    from_language = input("Укажите язык, с которого перевести, кодом (например, английский - en, немецкий - de, испанский - es, французский - fr, русский - ru): ")
    to_language = input(
        "Укажите язык, на который перевести, кодом (например, английский - en, немецкий - de, испанский - es, французский - fr, русский - ru): ")
    new_file_name = file_name[:2] + f"-{to_language}." + file_name[3:]

    with open(os.path.join(start_path, file_name), encoding="utf-8") as f:
        data = f.read()
        # print(data)

    params = {
        'key': API_KEY,
        'text': data,
        'lang': f"{from_language}-{to_language}",
    }

    response = requests.get(URL, params=params)
    json_ = response.json()

    end_path = input("Укажите путь для сохранения файла с переводом: ")

    with open(os.path.join(end_path, new_file_name), 'w', encoding="utf-8") as f:
        b = json_['text']
        for element in b:
            f.write(element)

    headers = {"Authorization": "OAuth AgAAAAAp25VPAADLWxVyTv1sVkOppvnWwL3HS88"}
    params = {'path': new_file_name, 'overwrite': 'True'}

    response = requests.get("https://cloud-api.yandex.net/v1/disk/resources/upload", headers=headers, params=params)
    send_url = response.json()['href']
    files = {'file': open(new_file_name, 'rb')}
    requests.put(send_url, files=files)


    return ''.join(json_['text'])


# print(translate_it('В настоящее время доступна единственная опция — признак включения в ответ автоматически определенного языка переводимого текста. Этому соответствует значение 1 этого параметра.', 'no'))

if __name__ == '__main__':
    translate_it('text', 'ru')




