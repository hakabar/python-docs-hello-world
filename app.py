from flask import Flask
import time

def get_tides_extremes():
	url = "https://tides.p.rapidapi.com/tides"
	myPos={'latitude': 38.692376, 'longitude': -9.359103}

	querystring = {"latitude":str(myPos['latitude']),"longitude":str(myPos['longitude']),"interval":"60","duration":"1440"}
	#querystring = {"latitude":"44.414","longitude":"-2.097","interval":"60","duration":"1440"}

	headers = {
		'x-rapidapi-key': "34f2717bf1msh9dd827225f80f5fp16da05jsne62d0e935898",
		'x-rapidapi-host': "tides.p.rapidapi.com"
		}

	data = requests.request("GET", url, headers=headers, params=querystring)

	dataDict= json.loads(data.text)

	print('High and Low tides: ')
	for dataEntry in dataDict['extremes']:
		dateSplited= dataEntry['datetime'].split('T')
		print('  - %s	on %s	at %s '%(dataEntry['state'], dateSplited[0], dateSplited[1][0:7]))

	currTime= time.time()
	tmpData=[0,abs(dataDict['heights'][0]['timestamp'] - currTime)]
	for i, dataEntry in enumerate(dataDict['heights'][1:]):
		tmp=  abs(dataEntry['timestamp'] - currTime)
		if tmp < tmpData[1]:
			tmpData[0]= i
			tmpData[1]= tmp
	print('\n  --> Current situation at %s --> %s'%(dataDict['heights'][tmpData[0]]['datetime'], dataDict['heights'][tmpData[0]]['state']))


app = Flask(__name__)

@app.route("/")
def hello():
    get_tides_extremes()
    return "Hello, World!"
