import requests

def send(message):

    print(message)
    token='6566877733:AAGOCmUmdRouSIg6ncYdXog4Ts-ifiphghA'
    channel_id = '-1002112427320'
    requests.post(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={channel_id}&text={message}')