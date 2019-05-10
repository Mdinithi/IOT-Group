from flask import Flask, render_template, request
import requests
import serial
import MySQLdb
import RPi.GPIO as GPIO # Importing the GPIO library to use the GPIO pins of Raspberry pi

app = Flask(__name__)
device = "/dev/ttyUSB0"
arduino = serial.Serial(device, 9600)
ledPin = 21  # Initializing pin 21 for led


@app.route('/player', methods=['POST'])
def player():
    playercode = request.form['playerId']
    #get the player details
    dbConn = MySQLdb.connect("localhost","root","password","tempdb") or die ("Could not connect to database")
    print(dbConn)

    with dbConn:
        
        cursor = dbConn.cursor()
        cursor.execute("SELECT PlayerId,PlayerName,GameLevel FROM playerLog WHERE PlayerId=(%s)",[playercode])
        record= cursor.fetchall()
        dbConn.commit()
        cursor.close()
        playerID=record[0]
        playerName=record[1]
        gameLevel=record[2]
        GPIO.output(ledPin,0)
        GameLevel= arduino.readline()
        print(GameLevel)
        if(GameLevel == 1):
            with dbConn:
                cursor = dbConn.cursor()
                cursor.execute("UPDATE playerLog (GameLevel=GameLevel+1) WHERE playerId= (%s)" ,[playerID])
                record= cursor.fetchall()
                dbConn.commit()
                cursor.close()
             
                    
    return render_template('player.html', playerName=playerName)
@app.route('/NewPlayer', methods=['POST'])
def NewPlayer():
    playerName = request.form['playerName']
    dbConn = MySQLdb.connect("localhost","root","password","tempdb") or die ("Could not connect to database")
    with dbConn:
        cursor = dbConn.cursor()
        cursor.execute("INSERT INTO playerLog (PlayerName,GameLevel) VALUES (%s,%s)" ,[playerName],[0])
        dbConn.commit()
        cursor.close()
    return render_template('player.html', playerName=playerName)

@app.route('/')
def index():

    
        return render_template('index.html')
                               


if __name__== "__main__":
    app.run(debug=True)


