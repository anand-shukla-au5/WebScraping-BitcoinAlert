# WebScraping-BitcoinAlert
Bitcoin Alert : Sends you Bitcon Alert on WhatsApp or Twitter by WebScrapping (https://cryptoprices.com/) 

## Build With

- [Python](https://www.python.org/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Twilio](https://www.twilio.com/)

## How to Run

Program can be started with parameters.For running the program according to user requirements user need to provide two parameters (-INR or -USD) and the second parameter is (-Twitter or -WhatsApp)

- Running with user provided parameters.
  Here User will need provide parameter in the manner described below.

```shell
$ python scrapy.py -INR -WhatsApp

```
## Code Usage
- For Sending data to [IFTTT](https://ifttt.com/join) webhooks and running required applets.

```python
ifttt_webhook_url = 'https://maker.ifttt.com/trigger/{}/with/key/oqIPU0KrD2hCrjPNmDnXA9oyrOO3HSHnVzBagrn6ej3'


def post_to_ifttt_webhook(event, value1, value2):
    # The payload that will be sent to IFTTT service
    data = {'value1': value1, 'value2': value2}
    ifttt_event_url = ifttt_webhook_url.format(
        event)  # Inserts our desired event
    # Sends a HTTP POST request to the webhook URL
    requests.post(ifttt_event_url, json=data)
```

- Using [Twilio Api](https://www.twilio.com/) to send WhatsApp notification
```python
    print('Sending Message on WhatsApp.....')
    account_sid = 'account_sid_from_twilio'
    auth_token = 'account_toke_twilio'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    body='Your bitcoin and Etherrum value in {0} are {1} and {2}'.format(
            usin, rates['bitcoin'], rates['ethereum']),
            from_='whatsapp:+14155238886',
            to='whatsapp:+91_mobile_no'
        )
    print(message.sid, message.status, message.error_message)
```
- Webscraping [Live Crypto Currency](https://cryptoprices.com/) to get Crypto Prices.
```python
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
```

## Learnings
- How to use python requests module.
- How to create IFTTT applets and use Webhooks and other platforms to receive notifications.
- Webscrapping a website and getting data you want.
- Creating a python program with various different modules.
- Using command line parameters.

## Author
Anand Shukla
