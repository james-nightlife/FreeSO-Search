from flask import current_app, Blueprint, render_template, request, redirect
import requests, json, plotly
import plotly.graph_objs as go
import numpy as np
from datetime import datetime

search_neighborhood = Blueprint('search_neighborhood', __name__)

@search_neighborhood.route('/search-neighborhood', methods=['GET'])
def index():
    if request.args.get('searchfield'):
        name = request.args.get('searchfield').replace(" ","%20").replace("'","%27").replace(".","%2E")
        url = '{}/userapi/city/1/neighborhoods/name/{}'.format(current_app.config['FREESO_API_BASE_URL'], name)
        data = requests.get(url).json()
        if 'name' in data:
            if data['mayor_id'] is None:
                data['mayor_id'] = "Vacant"
            else:
                data['mayor_id'] = id2Name(data['mayor_id'])

            data['mayor_elected_date'] = unixdate(data['mayor_elected_date'])
            data['description'] = data['description'].split("\n")
            return render_template('search-neighborhood/search-neighborhood.html', data=data)
        else:
            return render_template('search-neighborhood/search-neighborhood.html', error=1)
    else:
        url = '{}/userapi/city/1/lots/online'.format(current_app.config['FREESO_API_BASE_URL'])
        data = requests.get(url).json()
        newdata = neighborhoodPeopleDict(data)
        graph = [
            {
                'data':[{'x':list(newdata.keys()), 'y':list(newdata.values()), 'type':'bar', 'marker': {'color': list(newdata.values()), 'colorscale': 'Viridis'}}], 
                'layout':{'title':'Total Active Sim In Each Neighborhood', 'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)'}
            }
        ]

        ids = ['Graph-{}'.format(i) for i, _ in enumerate(graph)]
        graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('search-neighborhood/search-neighborhood.html', ids = ids, graphJSON=graphJSON)

def unixdate(num):
    dob = int(num)
    return datetime.utcfromtimestamp(dob).strftime('%A, %d %B %Y')

def id2Name(id):
    url = '{}/userapi/avatars/{}'.format(current_app.config['FREESO_API_BASE_URL'], id)
    data = requests.get(url).json()['name']
    return data

def neighborhoodPeopleDict(data):
    ret = {}
    for i in data['lots']:
        if str(i['neighborhood_id']) not in list(ret.keys()):
            ret[str(i['neighborhood_id'])] = i["avatars_in_lot"]
        else:
            ret[str(i['neighborhood_id'])] += i["avatars_in_lot"] 
    ret_new = {}
    url = '{}/userapi/city/1/neighborhoods/all'.format(current_app.config['FREESO_API_BASE_URL'])
    data = requests.get(url).json()['neighborhoods']   
    for i in list(ret.keys()):
        for j in data:
            if int(i) == j['neighborhood_id']:
                ret_new[j['name']] = ret[i]
                break      
    return ret_new

