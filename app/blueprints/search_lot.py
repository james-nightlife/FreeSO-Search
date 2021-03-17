from flask import current_app, Blueprint, render_template, request
import requests, json, plotly
import plotly.graph_objs as go
import numpy as np
from datetime import datetime

search_lot = Blueprint('search_lot', __name__)

@search_lot.route('/search-lot', methods=['GET'])
def index():
    if request.args.get('searchfield'):
        name = request.args.get('searchfield').replace(" ","%20").replace("'","%27").replace(".","%2E")
        url = '{}/userapi/city/1/lots/name/{}'.format(current_app.config['FREESO_API_BASE_URL'], name)
        data = requests.get(url).json()
        if 'name' in data:
            data['created_date'] = unixdate(data['created_date'])
            data['roommates'] = roommateList(data['roommates'] ,data['owner_id'])
            data['owner_id'] = id2Name(data['owner_id'])
            data['description'] = data['description'].split("\n")
            return render_template('search-lot/search-lot.html', data=data)
        else:
            return render_template('search-lot/search-lot.html', error=1)
    else:
        url = '{}/userapi/city/1/lots/online'.format(current_app.config['FREESO_API_BASE_URL'])
        data = requests.get(url).json()
        newdata = lotPeopleDict(data)
        graph = [
            {
                'data':[{'x':list(newdata.keys()), 'y':list(newdata.values()), 'type':'bar', 'marker': {'color': list(newdata.values()), 'colorscale': 'Viridis'}}], 
                'layout':{'title':'Total Active Sim In Each Lot ', 'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)'}
            }
        ]

        ids = ['Graph-{}'.format(i) for i, _ in enumerate(graph)]
        graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('search-lot/search-lot.html', ids = ids, graphJSON=graphJSON)

def unixdate(num):
    dob = int(num)
    return datetime.utcfromtimestamp(dob).strftime('%A, %d %B %Y')

def id2Name(id):
    url = '{}/userapi/avatars/{}'.format(current_app.config['FREESO_API_BASE_URL'], id)
    data = requests.get(url).json()['name']
    return data

def roommateList(rm, owner):
    try:
        rm.remove(owner)
    except ValueError:
        print("Owner isn't in the roommate list.")
    rm_new = []
    if len(rm) != 0:
        url = '{}/userapi/avatars?ids='.format(current_app.config['FREESO_API_BASE_URL'])
        for i in range(len(rm)):
            url += str(rm[i])
            if i < len(rm)-1:
                url += ','
        data = requests.get(url).json()['avatars']
        for i in range(len(rm)):
            rm_new.append(data[i]['name'])
    return rm_new

def lotPeopleDict(data):
    ret = {}
    for i in data['lots']:
        ret[i['name']] = i['avatars_in_lot']
    return ret