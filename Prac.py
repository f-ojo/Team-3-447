from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

# app = Flask(__name__)
# app.config['MYSQL_HOST'] = 'umbc-team-3-mysql.c3kav9ktnn4z.us-east-2.rds.amazonaws.com'
# app.config['MYSQL_USER'] = 'admin'
# app.config['MYSQL_PASSWORD'] = 'ZxdkCBNxZRy82aXOPrtD'
# app.config['MYSQL_DB'] = 'team3_crime_database'
# mysql = MySQL(app)

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Put your own password'
app.config['MYSQL_DB'] = 'crime(Whatever your database name)'
mysql = MySQL(app)

@app.route('/')
def cats():
    try:
        cur = mysql.connection.cursor()
        cur.execute('''select *
from crime.bpd_part_1_victim_based_crime_data LIMIT 50''')
        rv = cur.fetchall()
        payload = []
        content = {}
        for result in rv:
            content = {'Date': result[0], 'CrimeTime': result[1], 'CrimeCode': result[2], 'Location' : result[3],
                       'Description':result[4],'Inside/Outside':result[5],'Weapon':result[6], 'Post':result[7], 'District':result[8],
                       'Neighbourhood':result[9],'Longitude':result[10], 'Latitude':result[11], 'Location 1':result[12], 'Premise':result[13],
                       'vri_name 1':result[14], 'Total Incidents':result[15]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        print(e)
    finally:
        cur.close()

@app.route('/knife')
def knife():
    try:
        cur = mysql.connection.cursor()
        cur.execute('''select * from crime.bpd_part_1_victim_based_crime_data where Weapon = "KNIFE" 
LIMIT 50;''')
        rv = cur.fetchall()
        payload = []
        content = {}
        for result in rv:
            content = {'Date': result[0], 'CrimeTime': result[1], 'CrimeCode': result[2], 'Location': result[3],
                       'Description': result[4], 'Inside/Outside': result[5], 'Weapon': result[6], 'Post': result[7],
                       'District': result[8], 'Neighbourhood': result[9], 'Longitude': result[10],
                       'Latitude': result[11], 'Location 1': result[12], 'Premise': result[13],
                       'vri_name 1': result[14], 'Total Incidents': result[15]}
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        print(e)
    finally:
        cur.close()


def not_found(error = None):
    message = {
        'status' : 404,
        'message' : 'Not Found' + request.url,
    }
    return jsonify(message)

if __name__ == '__main__':
   app.run(debug = True)