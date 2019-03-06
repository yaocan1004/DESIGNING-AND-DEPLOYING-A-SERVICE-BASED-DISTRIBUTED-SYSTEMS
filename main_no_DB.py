from flask import Flask,render_template,request,jsonify
import requests
import json

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def map():
    if request.method == 'POST':
        key = "YourKey"
        orilist = request.form['from'].split()
        deslist = request.form['to'].split()
        mode = request.form.get('traffic_mode')
        ori = ""
        des = ""
        for word in orilist:
            ori = ori + word + "+"
        ori = ori[:-1]
        for word in deslist:
            des = des + word + "+"
        des=des[:-1]
        url = "https://maps.googleapis.com/maps/api/directions/json?origin="+ori+\
              "&destination="+des+"&key="+key
        # print ori,des,mode,url
        result = requests.get(url)
        direction = result.json()
        if direction['status'] == 'OK':
            #get weather information
            point_instruction = list()
            weather_url = "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&units=imperial&APPID=YourKey"
            route = direction['routes'][0]['legs'][0]["steps"]
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
                point_instruction.append(weather)
            return render_template('test.html', direction=direction, weather=point_instruction, method='POST')
        else:
            return("Not Found Correct Route, Please reopen the web and check your input information")
    else:
        print request.method
        return render_template('index.html',method='GET')



if __name__ == '__main__':
    app.run(debug = True)
