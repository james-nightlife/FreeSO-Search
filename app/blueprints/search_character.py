from flask import current_app, Blueprint, render_template, request
import requests
from datetime import datetime


search_character = Blueprint('search_character', __name__)

@search_character.route('/search-character', methods=['GET'])
def index():
    if request.args.get('searchfield'):
        name = (request.args.get('searchfield')).replace(" ", "%20")  
        url = '{}/userapi/city/1/avatars/name/{}'.format(current_app.config['FREESO_API_BASE_URL'], name)
        data = requests.get(url).json()
        if 'name' in data:
            data['gender'] = genderDeclare(data['gender'])
            data['date'] = unixdate(data['date'])
            data['current_job'] = job(data['current_job'])
            data['description'] = data['description'].split("\n")
            return render_template('search-character/search-character.html', data=data)
        else:
            return render_template('search-character/search-character.html', error=1)
    else:
        url = '{}/userapi/avatars/online'.format(current_app.config['FREESO_API_BASE_URL'])
        data = requests.get(url).json()

        online_num = data['avatars_online_count']
        online_list = data['avatars']

        url = '{}/userapi/city/1/lots/online'.format(current_app.config['FREESO_API_BASE_URL'])
        location = requests.get(url).json()['lots']

        for i in range(len(online_list)):
            if online_list[i]['privacy_mode'] == 0:
                if online_list[i]['location'] != 0:
                    for j in location:
                        if online_list[i]['location'] == j['location']:
                            online_list[i]['location'] = j['name']
                            break
                    else:
                        online_list[i]['location'] = 'Workplace'
                else:
                    online_list[i]['location'] = 'Map'
                    
        return render_template('search-character/search-character.html', num=online_num, online_list=online_list)

def genderDeclare(num):
    if num == 0:
        return "Male"
    else:
        return "Female"

def unixdate(num):
    dob = int(num)
    return datetime.utcfromtimestamp(dob).strftime('%A, %d %B %Y')

def job(num):
    if num == 0:
        return 'Unemployed'
    elif num == 1:
        return 'Robot Factory'
    elif num == 2:
        return 'Restaurant'
    elif num == 4:
        return 'DJ'
    elif num == 5:
        return 'Dancer'
