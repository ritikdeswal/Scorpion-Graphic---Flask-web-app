import os
from flask import Flask, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
import pyshorteners
from pytube import YouTube
import re
import random
from num2words import num2words
from numerizer import numerize
from faker import Faker
from newsapi import NewsApiClient

app = Flask(__name__)
app.debug = True

env = 'dev'

if env == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = '<paste your uri>'
else:
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = '<paste your uri>'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/url-shortener", methods=['GET', 'POST'])
def urlshortener():
    if (request.method == 'POST'):
        url = request.form.get('url')
        try:
            s = pyshorteners.Shortener()
            short = s.tinyurl.short(url)
            return render_template("url-shortener.html", para=short)
        except:
            return render_template("url-shortener.html", para="invalid")
    return render_template("url-shortener.html")


@app.route("/youtube-downloader", methods=['GET', 'POST'])
def youtube():
    global yturl
    if (request.method == 'POST'):

        yturl = request.form.get('url')
        try:
            yt = YouTube(yturl)
        except:
            return render_template("youtube-downloader.html", para="invalid")
        list1 = yt.streams.all()
        ytlinks = []
        for row in list1:
            column = str(row).split()
            if 'res="None"' in column:
                continue
            ytlinks.append(column[1:5])
        return render_template("youtube-downloader.html", ytlinks=ytlinks)
        # yt.streams.get_by_itag('251').download()
    else:
        return render_template("youtube-downloader.html")


@app.route("/downloading/<string:i>")
def downloading(i):
    path = os.listdir('newfolder')
    for i in path:
        os.remove("newfolder/{}".format(i))

    itag = ''.join(re.findall("\d", i))
    yt = YouTube(yturl)
    yt.streams.get_by_itag(itag).download(output_path='newfolder')
    redirect("/youtube-downloader")
    del itag
    del i
    for item in path:
        return send_file("newfolder/{}".format(item), as_attachment=True)


@app.route("/password-gen", methods=['GET', 'POST'])
def password():
    if (request.method == 'POST'):
        length = request.form.get('number')
        # necessary condition=2 uppercase, 2 lowercase, 2digit, 2 special char
        psw = []
        for i in range(0, 5):
            up = chr(random.randint(65, 90))
            low = chr(random.randint(97, 122))
            scar = str(random.choice("!@#$%^&*()?"))
            dg = str(random.randint(0, 9))
            psw2 = up + scar + low + dg
            psw.append(psw2)

        fpsw = "".join(psw)[0:int(length)]
        return render_template("password-gen.html", para=fpsw)

    return render_template("password-gen.html")


@app.route("/covid")
def covid():
    return render_template("covid.html")


@app.route("/num2word", methods=['GET', 'POST'])
def num2word():
    if (request.method == 'POST'):
        number = request.form.get('number')
        word = request.form.get('word')
        if number != '':
            wrd = num2words(number, lang="en_IN")
            return render_template("num2word.html", para2=wrd)
        elif word != '':

            b = "".join(word.split(" and"))
            a = "".join(b.split(","))
            c = a.split()
            print(c)
            sum = 0
            if 'crore' in c:
                val_index = c[:c.index('crore')]
                val2 = numerize(" ".join(val_index))
                sum += int(val2) * 10000000
            if 'lakh' in c:
                val_index = c[c.index('lakh') - 1]
                val3 = numerize("".join(val_index))
                sum += int(val3) * 100000
                try:
                    rest = " ".join(c[c.index('lakh') + 1:])
                    sum += int(numerize(rest))
                except:
                    pass
            else:
                sum = int(numerize(" ".join(c)))
            return render_template("num2word.html", para1=sum)
        elif number == "" and word == "":
            return render_template("num2word.html")
    else:
        return render_template("num2word.html")


@app.route("/faker", methods=['GET', 'POST'])
def faker():
    if (request.method == 'POST'):
        fake = Faker()
        fname = fake.first_name()
        lname = fake.last_name()
        fk_name = fname + " " + lname
        fk_email = lname.lower() + fname.lower() + fake.bothify("####") + "@" + fake.free_email_domain()
        fk_phone = fake.bothify("###-###-####")
        x = fake.profile()
        fk_DOB = fake.date()
        fk_blood = x["blood_group"]
        fk_address = x['address']
        fk_job = x['job']
        fk_cc_number = fake.credit_card_number()
        fk_cc_expiry = fake.credit_card_expire()

        return render_template("faker.html", fk_name=fk_name, fk_email=fk_email, fk_phone=fk_phone, fk_DOB=fk_DOB,
                               fk_blood=fk_blood, fk_address=fk_address, fk_job=fk_job, fk_cc_number=fk_cc_number,
                               fk_cc_expiry=fk_cc_expiry)

    return render_template("faker.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/news")
def news():
    newsapi = NewsApiClient(api_key='<paste your api key>')
    top_headlines = newsapi.get_top_headlines(sources='bbc-news,the-verge', language='en')
    articles = top_headlines['articles']
    # print(articles)
    context = []
    for item in articles:
        context2 = item['title'], item['description'], item['urlToImage'], item['url']
        context.append(context2)
    # print(context)
    return render_template("news.html", context=context)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(120), nullable=True)
    datetime = db.Column(db.String(60), nullable=False)

    def __init__(self, name, email, rating, comment, datetime):
        self.name = name
        self.email = email
        self.rating = rating
        self.comment = comment
        self.datetime = datetime


@app.route("/feedback", methods=['GET', 'POST'])
def feedback():
    import datetime
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        rating = request.form.get('rating')
        comment = request.form.get('comment')
        datetime = str(datetime.datetime.now()).split(".")[0]
        if name == '' or email == '':
            return render_template("feedback.html", message="* please enter required fields.", star="*")
        entry = Feedback(name=name, email=email, rating=rating, comment=comment, datetime=datetime)
        db.session.add(entry)
        db.session.commit()
    return render_template("feedback.html")


@app.route("/dashboard", methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        if username == "<set your username>" and password == "<set your password>":
            feedback = Feedback.query.all()
            return render_template("/dashboard.html", feedback=feedback)
        else:
            return render_template("login.html", para="invalid")
    return render_template("login.html")

@app.route("/delete/<string:n>",methods=['GET', 'POST'])
def delete(n):
    feedbk=Feedback.query.filter_by(sno=n).first()
    db.session.delete(feedbk)
    db.session.commit()
    return redirect("/dashboard")


@app.errorhandler(404)
def page_not_found(e):
    """
	for anyone trying different links or searching for images within the server
    """
    return (
        render_template(
            "error_template.html",
            title="error 404 bud",
            message="Time to make the chimi-fuckin'-changas. ",
            subline="404, not there",
        ),
        404,
    )


@app.errorhandler(400)
def bad_request(e):
    """
	For handling situations where the server doesn't know what to do with the browser's request
	"""
    return (
        render_template(
            "error_template.html",
            title="error 400",
            message=".??..>??<?..>???<",
            subline="Yeah, the server couldn't understand what you asked for, Sorry",
        ),
        400,
    )


@app.errorhandler(500)
def server_error(e):
    """
	error within server
	"""
    return (
        render_template(
            "error_template.html",
            title="error 500",
            message="INTERNAL SERVER ERROR 500",
            subline="They are just dumb machines....",
        ),
        400,
    )


if env == 'dev':
    app.run()
else:
    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
