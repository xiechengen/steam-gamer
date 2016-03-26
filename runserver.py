import sqlite3
from flask import Flask, request, session, g, redirect
from flask import url_for, abort, render_template, flash
import urllib2
import json
import re

from steamapiwrapper.Users import SteamUser
from steamapiwrapper.SteamGames import Games


from flask_sqlalchemy import SQLAlchemy
from flask_openid import OpenID

app = Flask(__name__)
#app.config.from_pyfile('settings.cfg')
db = SQLAlchemy(app)
oid = OpenID(app)

# configuration
DATABASE = 'steam-gamer.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'



app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steam_id = db.Column(db.String(40))
    nickname = db.String(80)

    @staticmethod
    def get_or_create(steam_id):
        rv = User.query.filter_by(steam_id=steam_id).first()
        if rv is None:
            rv = User()
            rv.steam_id = steam_id
            db.session.add(rv)
        return rv

'''
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

'''
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signin', methods=['GET', 'POST'])
def sigin():
    return render_template('signin.html')






_steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')

@app.route('/login')
@oid.loginhandler
def login():
    print oid.get_next_url
    if g.user is not None:
        return redirect(oid.get_next_url())
    return oid.try_login('http://steamcommunity.com/openid')


def get_steam_userinfo(steam_id):
    options = {
        'key': 'FC65FE32E5732FC54BC70256CDA122BB',
        'steamids': steam_id
    }
    url = 'http://api.steampowered.com/ISteamUser/' \
          'GetPlayerSummaries/v0001/?%s' % url_encode(options)
    rv = json.load(urllib2.urlopen(url))
    return rv['response']['players']['player'][0] or {}

@oid.after_login
def create_or_login(resp):
    match = _steam_id_re.search(resp.identity_url)
    g.user = User.get_or_create(match.group(1))
    steamdata = get_steam_userinfo(g.user.steam_id)
    g.user.nickname = steamdata['personaname']
    db.session.commit()
    session['user_id'] = g.user.id
    flash('You are logged in as %s' % g.user.nickname)
    return redirect(oid.get_next_url())

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(oid.get_next_url())

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