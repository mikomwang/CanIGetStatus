from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/hello")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route("/okay")
@app.route("/hm")
def okay():
	resp = requests.get("http://www.fivestars.com/api/unified/businesses?embed=business_type.business_category&limit=10&near=29.7066028470064%2C-95.552716882803&span=0.0918042807329027%2C0.09206678174947068&format=json&business_type=ba9cdf9a8aa94b149a8e07912326e2c4")
	# what u want is resp.text
	return (resp.text, resp.status_code, resp.headers.items())
