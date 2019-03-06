from flask import Flask,render_template,request
import requests
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy import and_
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://MySQL_user:MySQL_password@127.0.0.1/database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class googleMap(db.Model):
    __tablename__ = 'route'
    id = db.Column(db.INTEGER,primary_key=True)
    start_point = db.Column(db.Text,unique = False)
    end_point = db.Column(db.Text,unique = False)
    routes = db.Column(db.Text(length=(2**32)-1),unique = False)
    weathers = db.Column(db.Text(length=(2**32)-1),unique = False)

    def __repr__(self):
        return self.start_point + " to "+ self.end_point + ": details"

@app.route('/', methods = ['GET','POST'])
def map():
    if request.method == 'POST':
        orilist = request.form['from'].split()
        deslist = request.form['to'].split()
        ori = ""
        des = ""
        for word in orilist:
            ori = ori + word + "+"
        ori = ori[:-1]
        for word in deslist:
            des = des + word + "+"
        des=des[:-1]
        start_time = time.time()
        if findInDatabase(ori,des) != 'None':
            route_info,weather_info = findInDatabase(ori,des)
            direction = json.loads(route_info)
            point_instruction = json.loads(weather_info)
            finish_time = time.time()
            during = (finish_time - start_time)
            print "Getting route&weather information from database cost %s s" % during
        else:
            direction = getRoute(ori,des)
            if direction['status'] == 'OK':
                #get weather information
                point_instruction = getWeather(direction)
                addToDatabase(ori, des, direction,point_instruction)
            else:
                weathers = list()
                addToDatabase(ori, des, direction, weathers)
        if direction['status'] != 'OK':
            return "Can not find routes. Please reopen the web, then check your start & end address!"
        else:
            return render_template('test.html', direction=direction, weather=point_instruction, method='POST')

    else:
        print request.method
        return render_template('index.html',method='GET')


def getRoute(ori,des):
    start_time = time.time()
    key = "YourKey"
    url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + ori + \
          "&destination=" + des + "&key=" + key
    print ori, des, url
    result = requests.get(url)
    route = result.json()
    finish_time = time.time()
    during = (finish_time - start_time)
    print "Getting route information from google cost %s s" % during
    return route

def getWeather(route):
    point_instruction = list()
    start_time = time.time()
    weather_url = "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&units=imperial&APPID=YourKey"
    route = route['routes'][0]['legs'][0]["steps"]
    for step in route:
        step_lat = step["start_location"]['lat']
        step_lon = step["start_location"]['lng']
        weather_json = requests.get(weather_url % (step_lat, step_lon)).json()
        weather_information = weather_json['weather'][0]['main']
        weather_min_temp = weather_json['main']['temp_min']
        weather_max_temp = weather_json['main']['temp_max']
        weather_city = weather_json['name']
        weather = "City:" + weather_city + "\n" + "Weather: " + weather_information + "\n" + "Temperature: " + repr(
            weather_min_temp) + "~" + repr(weather_max_temp)
        # print weather
        point_instruction.append(weather)

    finish_time = time.time()
    during = (finish_time - start_time)
    print "Getting weather information from API cost %s s" % during
    return point_instruction

def findInDatabase(ori,des):
    result = googleMap.query.filter(and_(googleMap.start_point == ori, googleMap.end_point == des)).first()
    if(result != None):
        print "Find it!", result
        return result.routes, result.weathers
    else:
        print "Not found"
        return "None"

def addToDatabase(ori,des,response,weather):
    responseStr = json.dumps(response)
    weatherStr = json.dumps(weather)
    routeInfo = googleMap(start_point = ori, end_point = des, routes = responseStr, weathers = weatherStr)
    db.session.add(routeInfo)
    db.session.commit()
    print "Add %s to %s successfully" % (ori,des)

if __name__ == '__main__':
    # db.drop_all()
    db.create_all()
    # print 1
    app.run(debug = True)
