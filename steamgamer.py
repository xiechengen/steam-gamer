import sqlite3
from flask import Flask, request, session, g, redirect
from flask import url_for, abort, render_template, flash
import urllib2
import json

from steamapiwrapper.Users import SteamUser
from steamapiwrapper.SteamGames import Games


# configuration
DATABASE = 'steam-gamer.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'



app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculator', methods=['GET', 'POST'])
def cal():
    if request.method == 'POST':
        userid = request.form['userid']

        urloutput = urllib2.urlopen('http://api.steampowered.com/ISteamUser'
            '/ResolveVanityURL/v0001/?key=FC65FE32E5732FC54BC70256CDA122BB&'
            'vanityurl=' + userid)
        print urloutput
        steamid = json.load(urloutput)['response']['steamid']
        user = SteamUser(steamid, 'FC65FE32E5732FC54BC70256CDA122BB')
        games = user.get_games()

        gamelist = []
        appid_list = []
        for i in games:
            gamelist.append(i['name'])
            appid_list.append(i['appid'])

        gameapi = Games()
        g = gameapi.get_info_for(appid_list, 'CN')

        sumprice = 0
        '''
        for i in g:
            sumprice += int(i.price)
        print sumprice
        '''
        return render_template('result.html',
                                userid=userid,
                                gamelist=gamelist,
                                sumprice=sumprice)
    else:
        return render_template('calculator.html')

if __name__ == '__main__':
    app.run()