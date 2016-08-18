import requests, re
from bs4 import BeautifulSoup

def getIP():
	soup = BeautifulSoup(requests.get('http://checkip.dyndns.org/').text)
	return soup.find('body').string[20:]

sp = '\n'

base = 'http://api.worldweatheronline.com/free/v2/weather.ashx?key='
key = ''	#Get your API key from the website. 
query = '&q='

print('1 to get weather by entering a city and 2 to get weather by your IP address.')
flag = 0
while flag not in range(1, 3):
	flag = int(raw_input('Choice? (1 or 2)'))

if flag == 1:
	city = raw_input('City?')
	citylist = city.split()
	query += '+'.join(citylist)
elif flag == 2:
	query += str(getIP())

url = base + key + query
data = requests.get(url).text
soup = BeautifulSoup(data, 'xml')

print(sp + 'Weather Details: ' + sp)
print('Temperature: ' + soup.find('temp_C').string + sp)
print('Weather Description: ' + soup.find('weatherDesc').string + sp)
print('Humidity: ' + soup.find('humidity').string + ' Percent' + sp)
print('Pressure: ' + soup.find('pressure').string + ' mb' + sp)
print('P.O.P: ' + soup.find('precipMM').string + ' Percent' + sp)
print('Visibility: ' + soup.find('visibility').string + ' km' + sp)
print('Cloud Cover: ' + soup.find('cloudcover').string + ' Percent' + sp)
print('Sunrise: ' + soup.find('sunrise').string + sp)
print('Sunset: ' + soup.find('sunset').string + sp)
print('Moonrise: ' + soup.find('moonrise').string + sp)
print('Moonset: ' + soup.find('moonset').string + sp)


