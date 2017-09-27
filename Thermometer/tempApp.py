#!/usr/bin/python

from flask import Flask, render_template, request
import sqlite3 as sql
import time
import json
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clear')
def clearDb():
    con = sql.connect('temp.db')
    cur = con.cursor()
    cur.execute("DELETE FROM readings")
    con.commit()
    msg = "Contents deleted"
    return render_template('delete_all.html', msg = msg)
    con.close()

@app.route('/view', methods = ['GET'])
def viewData():
    if request.method == 'GET':
    	con = sql.connect('temp.db')
	cur = con.cursor()
    	cur.execute("SELECT * FROM readings")
    	vals = cur.fetchall()
	json_data = json.dumps(vals)
    	return render_template('view_Data.html', json_data = json_data)
    	con.close()	

@app.route('/home', methods = ['POST', 'GET'])
def hello():
    if request.method == 'POST':
    	try:
	    val = request.args.get('temp')
	    tm = time.time()
	    with sql.connect('temp.db') as con:
                cur = con.cursor()
    	        cur.execute("INSERT INTO readings(temp,time) VALUES (?,?)",(tm, val))
	        con.commit()
	        msg = "Added"
	except:
	    con.rollback()
            msg = "Error"
        finally:
    	    return ('', 200)
	    con.close()
	    

app.run (host='0.0.0.0')

