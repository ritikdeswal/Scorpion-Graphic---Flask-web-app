# Scorpion-Graphic---Flask-web-app

This web app is created by me during summer training .

```bash
https://scorpion-graphic.herokuapp.com/
```
## Software used in development
- Pycharm
- Sublime text 4
- PgAdmin 4

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install python libraries given in the  **requirements.txt** .


## Usage

```python
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
```


## Homepage
```python
@app.route("/")
def index():
    return render_template("index.html")
```

![navbar](https://github.com/ritikdeswal/Scorpion-Graphic---Flask-web-app/blob/master/scrnli_11_2_2020_2-38-45%20AM.png)

## URL shortner
```python
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
```

![URl-shortner](https://github.com/ritikdeswal/Scorpion-Graphic---Flask-web-app/blob/master/scrnli_11_2_2020_2-40-15%20AM.png)


## News API
```python
@app.route("/news")
def news():
    newsapi = NewsApiClient(api_key='<paste your api key>')
    top_headlines = newsapi.get_top_headlines(sources='bbc-news,the-verge', language='en')
    articles = top_headlines['articles']
```

![](https://github.com/ritikdeswal/Scorpion-Graphic---Flask-web-app/blob/master/scrnli_11_2_2020_2-54-10%20AM.png)


## COVID stats
```javascript
document.getElementById("stats2").disabled = true;
        document.getElementById("stats1").disabled = true;
        document.getElementById("stats4").disabled = true;
        
        function getData() {
          var country = document.getElementById('country').value;
          var xhttp = new XMLHttpRequest();
          xhttp.open("GET", "https://covid19.mathdro.id/api/countries/" + country, true);
          xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.myform.stats1.value='Confirmed Cases - ' + JSON.parse(this.responseText)['confirmed'].value
                document.myform.stats2.value='Recovered - ' + JSON.parse(this.responseText)['recovered'].value
               
                document.myform.stats4.value='Death(s) - ' + JSON.parse(this.responseText)['deaths'].value
            }
          };
          
          xhttp.send();
```
![](https://github.com/ritikdeswal/Scorpion-Graphic---Flask-web-app/blob/master/scrnli_11_2_2020_2-44-45%20AM.png)

# Other screenshots
## Random password generator

![random password generator](https://github.com/ritikdeswal/Scorpion-Graphic---Flask-web-app/blob/master/scrnli_11_2_2020_2-43-16%20AM.png)

## Fake data generator

![](https://github.com/ritikdeswal/Scorpion-Graphic---Flask-web-app/blob/master/scrnli_11_2_2020_2-49-43%20AM.png)

## Feedback Form

![](https://github.com/ritikdeswal/Scorpion-Graphic---Flask-web-app/blob/master/scrnli_11_2_2020_3-06-41%20AM.png)

## Feedback responses

![](https://github.com/ritikdeswal/Scorpion-Graphic---Flask-web-app/blob/master/scrnli_11_2_2020_3-13-53%20AM.png)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
