from flask import current_app, Blueprint, render_template, request
import requests


home = Blueprint('home', __name__)

@home.route('/')
def index():
    online_lot_url = '{}/userapi/city/1/lots/online'.format(current_app.config['FREESO_API_BASE_URL'])
    online_lot_data = requests.get(online_lot_url).json()
    online_lot_display = getLotOnline(online_lot_data['lots'])

    online_account_url = '{}/userapi/avatars/online'.format(current_app.config['FREESO_API_BASE_URL'])
    online_account_data = requests.get(online_account_url).json()
    total_account = online_account_data['avatars_online_count']
    online_account_display = getOldAccountOnline(online_account_data['avatars'])

    return render_template('home/home.html', lotdata = online_lot_display, accountdata = online_account_display, accountnum = total_account)


def getLotOnline(data):
    newdata = sorted(data, key = lambda i: i['avatars_in_lot'], reverse=True)
    while(len(newdata) > 4):
        newdata.pop()
    return newdata

def getOldAccountOnline(data):
    newdata = sorted(data, key = lambda i: i['avatar_id'])
    while(len(newdata) > 10):
        newdata.pop()
    return newdata