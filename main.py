import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import argparse

VK_URL = 'https://api.vk.ru/method/{}'


def create_parser():
    parser = argparse.ArgumentParser(description='Shortening a link and counting clicks on the shortened link')
    parser.add_argument('url', type=str, help='Input link for manipulation')
    args = parser.parse_args()
    return args.url

def shorten_link(token, url):
    method = 'utils.getShortLink'
    params = {
        'url': url,
        'private': 0,
        'access_token': token,
        'v': '5.199'
    }

    vk_response = requests.post(VK_URL.format(method), data=params)
    vk_response.raise_for_status()
    response_payload = vk_response.json()

    if 'error' in vk_response.text:
        error_code = response_payload['error']['error_code']
        error_msg = response_payload['error']['error_msg']
        error_message = f'Не получилось сократить ссылку, возникла ошибка: {error_msg}, код ошибки {error_code}'
        raise Exception(error_message)
    else:
        short_url = response_payload['response']['short_url']
        return short_url



def count_clicks(token, url):
    parsed_url = urlparse(url)
    key_for_request = parsed_url.path.lstrip('/')

    method = 'utils.getLinkStats'
    params = {
        'key': key_for_request,
        'extended': 0,
        'interval': 'forever',
        'access_token': token,
        'v': '5.199'
    }

    vk_response = requests.post(VK_URL.format(method), data=params)
    vk_response.raise_for_status()
    response_payload = vk_response.json()

    if 'error' in vk_response.text:
        error_code = response_payload['error']['error_code']
        error_msg = response_payload['error']['error_msg']
        error_message = f'Не получилось посчитать кол-во переходов по ссылке, возникла ошибка: {error_msg}, код ошибки {error_code}'
        raise Exception(error_message)
    else:
        url_clicks = response_payload['response']['stats'][0]['views']
        return url_clicks


def is_shorten_link(token, url):
    method = 'utils.checkLink'
    params = {
        'url': url,
        'access_token': token,
        'v': '5.199'
    }

    vk_response = requests.post(VK_URL.format(method), data=params)
    vk_response.raise_for_status()
    response_payload = vk_response.json()

    if 'error' in vk_response.text:
        error_code = response_payload['error']['error_code']
        error_msg = response_payload['error']['error_msg']
        error_message = f'Что-то пошло не так и случилась ошибка: {error_msg}, код ошибки {error_code}'
        raise Exception(error_message)
    else:
        vk_check_link = response_payload['response']['link']
        comparison_result = url not in vk_check_link
        return comparison_result



if __name__ == "__main__":
    user_url = createParser()
    load_dotenv()
    vk_token = os.environ['VK_TOKEN']


    try:
        if is_shorten_link(vk_token, user_url):
            url_clicks = count_clicks(vk_token, user_url)
            print(f'Кол-во переходов по короткой ссылке: {url_clicks}')
        elif not is_shorten_link(vk_token, user_url):
            short_url = shorten_link(vk_token, user_url)
            print(f'Короткая ссылка сайта: {short_url}')
    except requests.exceptions.HTTPError as er:
        print(f'Вы ввели неправильную ссылку или неверный токен:\n{er}')
    except requests.exceptions.ConnectionError:
        print('Не удалось установить соединение с сайтом')
    except Exception as er:
        print(er)