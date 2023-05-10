## fetching coordinates of datellite from N2YO API
from urllib.request import urlopen
import json
baseurl = "https://api.n2yo.com/rest/v1/satellite/positions/"
API_KEY="Q7R6AF-7SVN5R-PRPW2U-4YQX"
def getCoordinatesOfSatellite(name,noradid,observer_lat=41.702,observer_lng=-76.014,observer_alt=0,seconds=6000):
    layername="coordinates_"+str(name)
    url=baseurl+str(noradid)+"/"+str(observer_lat)+"/"+str(observer_lng)+"/"+str(observer_alt)+"/"+str(seconds)+"/&apiKey="+API_KEY
    response = urlopen(url)
    data_json = json.loads(response.read())
    positions=data_json['positions']
    coordinates=[]
    for i in positions:
        d={}
        d['latitude']=i['satlatitude']
        d['longitude']=i['satlongitude']
        coordinates.append(d)
      
    ## saving the data from api as .CSV file  
    import csv
    field_names = ['latitude','longitude']
    with open("coordinates_"+str(name)+".csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        writer.writerows(coordinates)
        
    ## displaying as a layer
    try:
        QgsProject.instance().removeMapLayer(QgsProject.instance().mapLayersByName("coordinates_"+str(name))[0])
        print("Yes")
    except Exception:
        print("No")
        pass
    uri = "file:///C:/Users/Krisha/Documents/coordinates_"+str(name)+".csv?encoding=UTF-8&delimiter=,&xField=longitude&yField=latitude&crs=epsg:4326"
    
    co_layer=QgsVectorLayer(uri,layername,"delimitedtext") 
    QgsProject.instance().addMapLayer(co_layer)

getCoordinatesOfSatellite("Sentinel-2A",40697,41.702,-76.014) # for Sentinel-2A
getCoordinatesOfSatellite("KOMPSAT-3A",40536,41.702,-76.014) # for KOMPSAT-3A
getCoordinatesOfSatellite("EROS-B",29079,41.702,-76.014) # for EROS-B
#print(coordinates)