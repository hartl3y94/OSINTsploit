import requests
import sys, os
import gmplot

template_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

heatmap = template_dir + "/templates/heatmap.html"
gpsmap = template_dir + "templates/gpsmap.html"

def heat_map(lats,lons, api_key):

		gmap3 = gmplot.GoogleMapPlotter(20.5937, 78.9629, 4)
		# Plot method Draw a line in
		# between given coordinates
		gmap3.heatmap(lats,lons)
		gmap3.scatter(lats,lons, '#FF0000', size=50, marker=False)
		gmap3.plot(lats,lons, 'cornflowerblue', edge_width = 3.0)
		gmap3.apikey = api_key
		gmap3.draw(heatmap)
		return gmap3

def gps_map(lats,lons, api_key):

		gmap3 = gmplot.GoogleMapPlotter(20.5937, 78.9629, 4)
		# Plot method Draw a line in
		# between given coordinates
		gmap3.heatmap(lats,lons)
		gmap3.scatter(lats,lons, '#FF0000', size=50, marker=False)
		gmap3.plot(lats,lons, 'cornflowerblue', edge_width = 3.0)
		gmap3.apikey = api_key
		gmap3.draw("templates/gpsmap.html")
		return gmap3

def loc(Location, api_key):
	lats=list()
	lons=list()
	for i in Location:
		response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+i+'&key='+api_key)
		resp_json_payload = response.json()
		try:
			lats.append(resp_json_payload['results'][0]['geometry']['location']['lat'])
			lons.append(resp_json_payload['results'][0]['geometry']['location']['lng'])
		except:
			continue
	#return heat_map(lats,lons, api_key)
	return (lats,lons)
