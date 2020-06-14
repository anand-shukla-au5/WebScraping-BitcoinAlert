import sys
import requests
import json
import progress
from twilio.rest import Client
from bs4 import BeautifulSoup


def cryptoprices(usin):
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
        print('Sending Message.....')
        # msg_body
        account_sid = 'ACd2650511cba3c67f6236e274ed6aba98'
        auth_token = '5eab77c3d85b6ef0a2c4b3d3b88dc389'
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body='Your bitcoin and Etherrum value in {0} are {1} and {2}'.format(
                usin, rates['bitcoin'], rates['ethereum']),
            from_='whatsapp:+14155238886',
            to='whatsapp:+917018497957'
        )
        print(message.sid, message.status, message.error_message)

    with open('crypto.json', 'w') as json_file:
        json.dump(rates, json_file)


if len(sys.argv) == 2:
    print(sys.argv[0], sys.argv[1])
    if sys.argv[1] == '-USD' or sys.argv[1] == '-INR':
        cryptoprices(sys.argv[1])
    else:
        print("Command Line argumnet should be -INR or -USD in Capital")
        exit()
else:
    print("Pass Command line Argumnets as -USD or -INR")