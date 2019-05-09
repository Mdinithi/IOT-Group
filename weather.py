from flask import Flask, render_template, request
import requests
import serial
import MySQLdb


app = Flask(__name__)
device = "/dev/ttyUSB1"


@app.route('/temperature', methods=['POST'])
def temperature():
    zipcode = request.form['zip']
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?zip='+zipcode+',AU&appid=4083a032ffd8ce8fb1c5fa95e780c5ba')
    json_object = r.json()
    temp_k = float(json_object['main']['temp'])
    temp_c = float(temp_k-273)
    return render_template('temperature.html', temp=temp_c)
@app.route('/fan', methods=['POST'])
def fan():
    #get the room temperature
    dbConn = MySQLdb.connect("localhost","root","password","tempdb") or die ("Could not connect to database")
    print(dbConn)
    arduino = serial.Serial(device, 9600)
      
    with dbConn:
        cursor = dbConn.cursor()
        cursor.execute("SELECT Temperature FROM tempLog ORDER BY TempId DESC LIMIT 1")
        record= cursor.fetchall()
        dbConn.commit()
        cursor.close()
    #check the threshold value
        threshold = request.form['threshold']
        fanStatus =""
    # determine to turn on or off according to the value
    #0 to turn off the fan and 1 to turn on the fan
        if(threshold<record[0]):
            arduino.write('%d'%1)# turn on the fan if room temp is higher than outside temp
            fanStatus = "Off"
        else:
            arduino.write('%d'%0)# turn off fan if the room temp is higher than outside temp
            fanStatus = "On"
    return render_template('fan.html', status=fanStatus , record=record[0])    
            
@app.route('/')
def index():
        arduino = serial.Serial(device, 9600)
        data = arduino.readline()
        print(data)
        dbConn = MySQLdb.connect("localhost","root","password","tempdb") or die ("Could not connect to database")
        with dbConn:
            cursor = dbConn.cursor()
            cursor.execute("INSERT INTO tempLog (Temperature) VALUES (%s)" ,[data])
            dbConn.commit()
            cursor.close()
       

    
        return render_template('index.html')
                               


if __name__== "__main__":
    app.run(debug=True)


