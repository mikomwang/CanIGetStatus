from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

uidmappings = {"Juice": "ba9cdf9a8aa94b149a8e07912326e2c4",
            "Smoothie": "ba9cdf9a8aa94b149a8e07912326e2c4",
            "Piercing": "421a21b9de57485886e1504f3b345007",
            "Tattoo": "421a21b9de57485886e1504f3b345007",
            "Coffee": "a4a71403d3ac4a91a326f9b968ef2d25",
            "Tea": "a4a71403d3ac4a91a326f9b968ef2d25"
}

pricemappings = {"Juice": 7,
                 "Smoothie": 6,
                 "Piercing": 30,
                 "Tattoo": 40,
                 "Coffee": 4,
                 "Tea": 5,
}

STATUS_THRESHOLD = 1500

@app.route("/lookup/<item>")
def main(item=None):
    if uidmappings.get(item):
        business_type = "business_type=" + uidmappings.get(item)
    else:
        return "Fail!"
    business_search_string = "http://www.fivestars.com/api/unified/businesses?embed=business_type.business_category&limit=10&near=29.7066028470064%2C-95.552716882803&span=0.9918042807329027%2C0.99206678174947068&format=json&" + business_type
    response = requests.get(business_search_string)
    business_dict = json.loads(response.text)
    business_name = business_dict["items"][0]["name"]
    pic = business_dict["items"][0]["picture"]
    amount = STATUS_THRESHOLD / pricemappings[item]
    print business_name
    return render_template('hello.html', name=business_name, amount=amount , item=item+"s", pic=pic)


@app.route("/okay")
@app.route("/hm")
def okay():
    resp = requests.get("http://www.fivestars.com/api/unified/businesses?embed=business_type.business_category&limit=10&near=29.7066028470064%2C-95.552716882803&span=0.0918042807329027%2C0.09206678174947068&format=json&business_type=ba9cdf9a8aa94b149a8e07912326e2c4")
    # what u want is resp.text
    print resp.text
    dictio = json.loads(resp.text)
    print dictio['items']
    return (resp.text, resp.status_code, resp.headers.items())
