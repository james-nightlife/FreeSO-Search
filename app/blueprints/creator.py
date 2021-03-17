from flask import current_app, Blueprint, render_template
import pymysql

creator = Blueprint('creator', __name__)

@creator.route('/creator')
def index():
    creator_dict = importData()
    return render_template('creator/creator.html', creator=creator_dict)

def importData():
    row = []
    con = pymysql.connect(host = 'bh8cpy3zqogyrijhhevy-mysql.services.clever-cloud.com', user ='uvekty1c9ako2iaz', password = 'jly1Sx4f4cLloVSJ8FSI', database = 'bh8cpy3zqogyrijhhevy')
    try:
        with con.cursor() as cur:
            cur.execute('SELECT * FROM creator')
            rows = cur.fetchall()
            for i in rows:
                row.append(i)
    finally:
        con.close()
    return row