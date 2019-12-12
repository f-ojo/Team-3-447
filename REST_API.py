from flask import Flask, request, jsonify, Response
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'umbc-team-3-mysql.c3kav9ktnn4z.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'ZxdkCBNxZRy82aXOPrtD'
app.config['MYSQL_DB'] = 'team3_crime_database'
mysql = MySQL(app)

# FUNCTION TO CONVERT LIST TO TUPLE
def str_to_tup(l):
    wow = "(\""
    for i in range(len(l)):
        wow += l[i]
    wow += "\")"
    str(wow)
    return wow

# FUNCTION TO CONVERT LIST TO TUPLE JUST FOR DATE AND TIME
def str_to_tup_date(l):
    wow = ""
    add = " and "
    for i in range(len(l)):
        if i != 1:
            wow = wow + "'" + l[i] + "'"
        else:
            wow += add
            wow = wow + "'" + l[i] + "'"
    str(wow)
    return wow


@app.route('/api', methods = ['GET'])
def crime_data():
    try:
        cur = mysql.connection.cursor()
        count = 0
        query_string = "select * " \
                       "from crime2 " \
                       "where "

        if 'weapon' in request.args:
            if count == 1:
                weapon = request.args.get('weapon').split("_")
                if len(weapon) == 1:
                    query_string = query_string + " and weapon in " + str_to_tup(weapon)
                else:
                    query_string = query_string + " and weapon in " + str(tuple(weapon))
            else:
                count += 1
                weapon = request.args.get('weapon').split("_")
                if len(weapon) == 1:
                    query_string = query_string + " weapon in " + str_to_tup(weapon)
                else:
                    query_string = query_string + " weapon in " + str(tuple(weapon))

        if 'district' in request.args:
            if count == 1:
                district = request.args.get('district').split("_")
                if len(district) == 1:
                    query_string = query_string + " and District in " + str_to_tup(district)
                else:
                    query_string = query_string + " and District in " + str(tuple(district))
            else:
                count += 1
                district = request.args.get('district').split("_")
                if len(district) == 1:
                    query_string = query_string + " District in " + str_to_tup(district)
                else:
                    query_string = query_string + " District in " + str(tuple(district))

        if 'Inside/Outside' in request.args:
            if count == 1:
                io = request.args.get('Inside/Outside').split("_")
                if len(io) == 1:
                    query_string = query_string + "and `Inside/Outside` in " + str_to_tup(io)
                else:
                    query_string = query_string + "and `Inside/Outside` in " + str(tuple(io))
            else:
                count += 1
                io = request.args.get('Inside/Outside').split("_")
                if len(io) == 1:
                    query_string = query_string + "`Inside/Outside` in " + str_to_tup(io)
                else:
                    query_string = query_string + "`Inside/Outside` in " + str(tuple(io))

        if 'description' in request.args:
            if count == 1:
                description = request.args.get('description').split("_")
                if len(description) == 1:
                    query_string = query_string + "and Description in " + str_to_tup(description)
                else:
                    query_string = query_string + "and Description in " + str(tuple(description))
            else:
                count += 1
                description = request.args.get('description').split("_")
                if len(description) == 1:
                    query_string = query_string + "  Description in " + str_to_tup(description)
                else:
                    query_string = query_string + " Description in " + str(tuple(description))

        if 'dateandtime' in request.args:
            if count == 1:
                dateandtime = request.args.get('dateandtime').split("_")
                if len(dateandtime) == 1:
                    query_string = query_string + " and (`DateTime` between " + str_to_tup_date(dateandtime) + ")"
                else:
                    query_string = query_string + " and (`DateTime` between " + str_to_tup_date(dateandtime) + ")"
            else:
                count += 1
                dateandtime = request.args.get('dateandtime').split("_")
                query_string = query_string + "  (`DateTime` between " + str_to_tup_date(dateandtime) + ")"

        cur.execute(query_string)
        rv = cur.fetchall()
        payload = []
        content = {}
        for result in rv:
            content = {'CrimeCode': result[0], 'Location': result[1], 'Description': result[2], 'Inside/Outside': result[3],
                       'Weapon': result[4], 'Post': result[5], 'District': result[6], 'Neighborhood': result[7],
                       'Longitude': result[8], 'Latitude': result[9], 'Location 1': result[10], 'Premise': result[11],
                       'vri_name 1': result[12], 'Total_incident': result[13], 'DateTime': result[14]}
            payload.append(content)
            content = {}
        resp = jsonify(payload)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
        #return query_string
    except Exception as e:
        print(e)
    finally:
        cur.close()


def not_found(error = None):
    message = {
        'status': 404,
        'message': 'Not Found' + request.url,
    }
    return jsonify(message)


if __name__ == '__main__':
    app.run(debug=True,port=5000)
