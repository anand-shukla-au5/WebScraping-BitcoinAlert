import sys
import requests
import json
from twilio.rest import Client
from bs4 import BeautifulSoup

ifttt_webhook_url = 'https://maker.ifttt.com/trigger/{}/with/key/oqIPU0KrD2hCrjPNmDnXA9oyrOO3HSHnVzBagrn6ej3'


def post_to_ifttt_webhook(event, value1, value2):
    # The payload that will be sent to IFTTT service
    data = {'value1': value1, 'value2': value2}
    ifttt_event_url = ifttt_webhook_url.format(
        event)  # Inserts our desired event
    # Sends a HTTP POST request to the webhook URL
    requests.post(ifttt_event_url, json=data)


def cryptoprices(usin, op_msg):
    convert = 1

    # Current USD to INR value
    if usin == '-INR':
        forex = requests.get(
            'https://economictimes.indiatimes.com/markets/forex')._content

        soil = BeautifulSoup(forex, 'lxml')
        trprice = soil.find("tr", {'data-curtype': 'USD/INR'})
        tdata = trprice.find('td', {'class': 'alignR price'})
        usdtoinr = float(tdata.text)
        convert = usdtoinr

    # Getting Bitcoin Value Web Scrapping
    print("Getting Crypto Rates.....")
    rates = {}
    res = requests.get('https://cryptoprices.com/')
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')
        tbody = soup.find('tbody')
        ba = tbody.findAll("span", {"data-currency": "USD"})
        for price in ba:
            rates[str(price['data-live-price'])
                  ] = round(float(price['data-price'])*convert, 3)

        print(rates)
        if op_msg == '-Twitter':
            print("Twitter Notifications.....")
            post_to_ifttt_webhook('bitcoin_alert', usin, rates)
        if op_msg == '-WhatsApp':
            print('Sending Message on WhatsApp.....')
            account_sid = 'ACd2650511cba3c67f6236e274ed6aba98'
            auth_token = '82530ea5158ab36a7844381f30100173'
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body='Your bitcoin and Etherrum value in {0} are {1} and {2}'.format(
                    usin, rates['bitcoin'], rates['ethereum']),
                from_='whatsapp:+14155238886',
                to='whatsapp:+917353125589'
            )
            print(message.sid, message.status, message.error_message)
        with open('crypto.json', 'w') as json_file:
            json.dump(rates, json_file)
    return print("Message Sent......")


if len(sys.argv) == 3:
    print(sys.argv[0], sys.argv[1], sys.argv[2])
    if sys.argv[1] == '-USD' or sys.argv[1] == '-INR':
        if sys.argv[2] == '-WhatsApp' or sys.argv[2] == '-Twitter':
            cryptoprices(sys.argv[1], sys.argv[2])
        else:
            print("Second Argument should be -WhatsApp or -Twitter")
            exit()
    else:
        print("Command Line first argumnet should be -INR or -USD in Capital and second argument as -WhatsApp or -Twitter")
        exit()
else:
    print("Pass Command line Argumnets as -USD or -INR and -WhatsApp or -Twitter")
