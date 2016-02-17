from flask import Flask
from flask import render_template
from flask import request
from steamapiwrapper.Users import SteamUser
from steamapiwrapper.SteamGames import Games

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculator', methods=['GET', 'POST'])
def cal():
    if request.method == 'POST':
        userid = request.form['userid']
        user = SteamUser(userid, 'FC65FE32E5732FC54BC70256CDA122BB')
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
        return render_template('result.html', userid=userid, gamelist=gamelist, sumprice=sumprice)
    else:
        return render_template('calculator.html')

if __name__ == '__main__':
    app.run()
