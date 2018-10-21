require([
  "esri/Map",
  "esri/layers/CSVLayer",
  "esri/views/MapView"
], function(Map, CSVLayer, MapView) {
	var url = "http://localhost:8001/static/startLocations.csv";
	var csvLayer = new CSVLayer({
	 	url: url,
	 	copyright: "NYC Taxi Data"
	});
	csvLayer.renderer = {
        type: "simple", // autocasts as new SimpleRenderer()
        symbol: {
		  type: "simple-marker",  // autocasts as new SimpleMarkerSymbol()
		  style: "circle",
		  color: "blue",
		  size: "2px",  // pixels
		  outline: {  // autocasts as new SimpleLineSymbol()
		    color: [ 255, 255, 255 ],
		    width: 1  // points
		  }
		}
    };

  	var map = new Map({
    	basemap: "dark-gray",
    	layers: [csvLayer]
  	});

  	var view = new MapView({
    	container: "viewDiv1",  // Reference to the DOM node that will contain the view
    	center: [-74.006,40.7128],
    	zoom:11,
    	map: map               // References the map object created in step 3
  	});
});

require([
  "esri/Map",
  "esri/layers/CSVLayer",
  "esri/views/MapView"
], function(Map, CSVLayer, MapView) {
	var url = "http://localhost:8001/static/endLocations.csv";
	var csvLayer = new CSVLayer({
	 	url: url,
	 	copyright: "NYC Taxi Data"
	});
	csvLayer.renderer = {
        type: "simple", // autocasts as new SimpleRenderer()
        symbol: {
		  type: "simple-marker",  // autocasts as new SimpleMarkerSymbol()
		  style: "circle",
		  color: "red",
		  size: "2px",  // pixels
		  outline: {  // autocasts as new SimpleLineSymbol()
		    color: [ 255, 255, 255 ],
		    width: 1  // points
		  }
		}
    };

  	var map = new Map({
    	basemap: "dark-gray",
    	layers: [csvLayer]
  	});

  	var view = new MapView({
    	container: "viewDiv2",  // Reference to the DOM node that will contain the view
    	center: [-74.006,40.7128],
    	zoom:11,
    	map: map               // References the map object created in step 3
  	});
});