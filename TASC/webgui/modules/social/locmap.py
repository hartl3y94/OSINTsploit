import requests
import gmplot

def heat_map(lats,lons):
    print(lats,lons)
    gmap3 = gmplot.GoogleMapPlotter(20.5937, 78.9629, 5)
    # Plot method Draw a line in
    # between given coordinates
    gmap3.heatmap(lats,lons)
    '''for i in range(len(lats)):
        gmap3.marker(lats[i],lons[i], 'cornflowerblue')'''
    gmap3.scatter(lats,lons, '#FF0000', size=50, marker=False)
    #gmap3.plot(lats,lons, 'cornflowerblue', edge_width = 3.0)
    gmap3.apikey = "AIzaSyBnIrhidN5aiBFBVK9kgPDrISe0_MePQpw"
    gmap3.draw("templates/heatmap.html")
    return gmap3

def loc(Location):
	lats=list()
	lons=list()
	for i in Location:
		response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+i+'&key=AIzaSyA4KKZm2o6ZYDa0oTYJUqrjw8akzbS62Yk')
		resp_json_payload = response.json()
		lats.append(resp_json_payload['results'][0]['geometry']['location']['lat'])
		lons.append(resp_json_payload['results'][0]['geometry']['location']['lng'])
	return heat_map(lats,lons)
