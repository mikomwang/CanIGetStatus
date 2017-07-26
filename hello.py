from flask import Flask, render_template
import requests
import json
import urllib
import random
import rauth
from yelpapi import YelpAPI

app = Flask(__name__)
app.jinja_env.auto_reload = True

client_id = "JvLkoebzB1-OWop1WVbq7w"
client_secret = "i4lVewbF6uDPHgtP2KXERAh0843t5gckBi9ox04yOtatOJcVRpRTH8HNTLZHjjHr"

uidmappings = {"Kale Smoothies": "ba9cdf9a8aa94b149a8e07912326e2c4",
            "Thai Tea Bobas": "ba9cdf9a8aa94b149a8e07912326e2c4",
            "Cups of just Lychee Toppings": "ba9cdf9a8aa94b149a8e07912326e2c4",
            "Cups of Coffee": "a4a71403d3ac4a91a326f9b968ef2d25",
            "Gallons Of Paint": "d9fd679597ea4d4d99cb10f5a62a77ac",
            "Apples": "d2a8e7b49ad7449b999f43f6b1500d46",
            "Heads Of Brocolli": "d2a8e7b49ad7449b999f43f6b1500d46",
            "Dog Treats": "a5027fce458e454781e4aef5104e4a97",
            "Dog Bones": "a5027fce458e454781e4aef5104e4a97",
            "Copies of Atlas Shrugged by Ayn Rand": "0d4fec3109554da3841dbc5516e2b66e",
            "Twilight Novels": "0d4fec3109554da3841dbc5516e2b66e",
            "Shots of Vodka": "17edb070fc284d9b9f813f8113fb8b2b",
            "Sets of Monopoly": "29f3078de407483eaeb082f21026051a",
            "Vape Pens": "0e409314cadd4776a8e6768b314b7e95",
            "Loose Grapes": "d2a8e7b49ad7449b999f43f6b1500d46"
}

pricemappings = {"Kale Smoothies": 7,
                 "Cups of just Lychee Toppings": 0.2,
                 "Twilight Novels": 13,
                 "Thai Tea Bobas": 6,
                 "Apples": 0.5,
                 "Heads Of Brocolli": 0.8,
                 "Gallons Of Paint": 10,
                 "Cups of Coffee": 4,
                 "Dog Treats": 1,
                 "Dog Bones": 1.5,
                 "Copies of Atlas Shrugged by Ayn Rand": 14,
                 "Shots of Vodka": 8,
                 "Sets of Monopoly": 18,
                 "Vape Pens": 22,
                 "Loose Grapes": 0.1
}

STATUS_THRESHOLD = 300

@app.route("/status")
def main():
    item = random.choice(uidmappings.keys())
    if uidmappings.get(item):
        business_type = "business_type=" + uidmappings.get(item)
    else:
        return "Fail!"

    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    area = "near=" + str(lat) + "%2C" + str(lon)

    business_search_string = "http://www.fivestars.com/api/unified/businesses?embed=business_type.business_category&limit=10&" + area + "&span=0.9918042807329027%2C0.99206678174947068&format=json&" + business_type
    response = requests.get(business_search_string)
    business_dict = json.loads(response.text)
    if not (business_dict["items"]):
        return main()
    business = random.choice(business_dict["items"])
    business_name = business["name"]
    desc = business["description"]
    pic = business["picture"]
    if pic:
        urllib.urlretrieve(pic, 'static/picture.jpg')

    amount = int(STATUS_THRESHOLD / pricemappings[item])

    phone = "+1" + business["phone"]
    yelp_api = YelpAPI(client_id, client_secret)
    phone_query = yelp_api.phone_search_query(phone=phone)['businesses']
    reviews = None
    if phone_query:
        biz_id = phone_query[0]['id']
        search_results = yelp_api.reviews_query(id=biz_id)
        reviews = search_results['reviews']

    return render_template('hello.html', reviews=reviews if reviews else {}, desc=desc, name=business_name, amount=amount , item=item, origin="Fivestars", dest=business_name)


@app.route("/okay")
@app.route("/hm")
def okay():
    resp = requests.get("http://www.fivestars.com/api/unified/businesses?embed=business_type.business_category&limit=10&near=29.7066028470064%2C-95.552716882803&span=0.0918042807329027%2C0.09206678174947068&format=json&business_type=ba9cdf9a8aa94b149a8e07912326e2c4")
    # what u want is resp.text
    print resp.text
    dictio = json.loads(resp.text)
    print dictio['items']
    #return (resp.text, resp.status_code, resp.headers.items())
    return main()

@app.route("/uh")
def fuck():
    consumer_key = "JvLkoebzB1-OWop1WVbq7w"
    consumer_secret = "i4lVewbF6uDPHgtP2KXERAh0843t5gckBi9ox04yOtatOJcVRpRTH8HNTLZHjjHr"

    session = rauth.OAuth1Session(
        consumer_key = consumer_key,
        consumer_secret = consumer_secret
    )
    params = {"phone": "14157492060",
    "consumer_key": "JvLkoebzB1-OWop1WVbq7w",
    "consumer_secret": "i4lVewbF6uDPHgtP2KXERAh0843t5gckBi9ox04yOtatOJcVRpRTH8HNTLZHjjHr"
    }
    resp = session.get("https://api.yelp.com/v3/businesses/search/phone", params=params)

    #Transforms the JSON API response into a Python dictionary
    return (resp.text, resp.status_code, resp.headers.items())

@app.route("/yelp")
def poop():
    yelp_api = YelpAPI(client_id, client_secret)
    biz_id= yelp_api.phone_search_query(phone='+13193375512')['businesses'][0]['id']
    search_results = yelp_api.reviews_query(id=biz_id)
    for i in search_results['reviews']:
        print i['text']
    return "wot"

