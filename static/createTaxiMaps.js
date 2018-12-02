require([
  "esri/Map",
  "esri/layers/CSVLayer",
  "esri/views/MapView",
  "esri/widgets/Legend",
  "esri/widgets/Home",
  "esri/layers/support/Field"
], function(Map, CSVLayer, MapView, Legend, Home, Field) {
	var url = "http://icsl.ee.columbia.edu:8001/static/startLocations.csv";
	var csvLayer = new CSVLayer({
	 	url: url,
	 	copyright: "NYC Taxi Data",
	 	fields: [new Field({"name":"hour", "alias":"hour", "type":"Number"})]
	});
	console.log(csvLayer.fields);

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
  	console.log("Hello World");

	var slider = document.getElementById("slider");
	var sliderValue = document.getElementById("sliderValue");
	var playButton = document.getElementById("playButton");
	var animation = null;

	function inputHandler() {
		stopAnimation();
		setYear(parseInt(slider.value));
	}
	slider.addEventListener("input", inputHandler);
	slider.addEventListener("change", inputHandler);


	// Toggle animation on/off when user
	// clicks on the play button
	playButton.addEventListener("click", function () {
		if (playButton.classList.contains("toggled")) {
			stopAnimation();
		} else {
			startAnimation();
		}
	});

	// view.ui.empty("top-left");
	// view.ui.add(new Home({view: view}), "top-left");
	view.ui.add(new Legend({view: view}), "bottom-left");



function createRenderer(year) {
	console.log(year)
	var opacityStops = [{
		opacity: 0,
		value: year - 4
	},{
		opacity: 1,
		value: year
	},{
		opacity: 0,
		value: year + 1
	}];

    return {
    	type: "simple",  // autocasts as new SimpleRenderer()
		  symbol: {
		    type: "simple-marker",  // autocasts as new SimpleMarkerSymbol()
		    size: 2
		  },
      visualVariables: [{
        type: "opacity",
        field: "hour",
        stops: opacityStops,
        legendOptions: {
          showLegend: false
        }
      }, {
        type: "color",
        field: "hour",
        legendOptions: {
          title: "Hour:"
        },
        stops: [{
          value: year,
          color: "#ff0",
          label: Math.floor(year) + ":00"
        }, {
          value: year - 2,
          color: "#0f0",
          label: Math.max(0, (Math.floor(year) - 2))+":00"
        }, {
          value: year - 4,
          color: "#040",
          label: Math.max(0, (Math.floor(year) - 4))+":00"
        }]
      }]
    };
  }
  function createRenderer2(year) {
	console.log(year)
	var opacityStops = [{
		opacity: 0,
		value: year - 4
	},{
		opacity: 1,
		value: year
	},{
		opacity: 0,
		value: year + 1
	}];

    return {
    	type: "simple",  // autocasts as new SimpleRenderer()
		  symbol: {
		    type: "simple-marker",  // autocasts as new SimpleMarkerSymbol()
		    size: 2
		  },
      visualVariables: [{
        type: "opacity",
        field: "hour",
        stops: opacityStops,
        legendOptions: {
          showLegend: false
        }
      }, {
        type: "color",
        field: "hour",
        legendOptions: {
          title: "Hour:"
        },
        stops: [{
          value: year,
          color: "#0ff",
          label: Math.floor(year) + ":00"
        }, {
          value: year - 2,
          color: "#f0f",
          label: Math.max(0, (Math.floor(year) - 2))+":00"
        }, {
          value: year - 4,
          color: "#404",
          label: Math.max(0, (Math.floor(year) - 4))+":00"
        }]
      }]
    };
  }

	function startAnimation() {
		stopAnimation();
		animation = animate(parseFloat(slider.value));
		playButton.classList.add("toggled");
	}

      /**
       * Stops the animations
       */
      function stopAnimation() {
        if (!animation) {
          return;
        }

        animation.remove();
        animation = null;
        playButton.classList.remove("toggled");
      }

      /**
       * Animates the color visual variable continously
       */
      function animate(startValue) {
        var animating = true;
        var value = startValue;

        var frame = function (timestamp) {
          if (!animating) {
            return;
          }

          value += 0.5;
          if (value >= 24) {
            value = 0;
          }

          setYear(value);

          // Update at 30fps
          setTimeout(function () {
            requestAnimationFrame(frame);
          }, 1000 / 30);
        };

        frame();

        return {
          remove: function () {
            animating = false;
          }
        };
      }

	var url2 = "http://icsl.columbia.edu:8001/static/endLocations.csv";
	var csvLayer2 = new CSVLayer({
	 	url: url2,
	 	copyright: "NYC Taxi Data",
	 	fields: [new Field({"name":"hour", "alias":"hour", "type":"Number"})]
	});
	console.log(csvLayer2.fields);

  	var map2 = new Map({
    	basemap: "dark-gray",
    	layers: [csvLayer2]
  	});

  	var view2 = new MapView({
    	container: "viewDiv2",  // Reference to the DOM node that will contain the view
    	center: [-74.006,40.7128],
    	zoom:11,
    	map: map2               // References the map object created in step 3
  	});
  	view2.ui.add(new Legend({view: view2}), "bottom-left");
  	setYear(0);

	function setYear(value) {
		sliderValue.innerHTML = Math.floor(value)+":00";
		slider.value = Math.floor(value);
		var rend = createRenderer(value);
		csvLayer.renderer = rend;
		var rend2 = createRenderer2(value);
		csvLayer2.renderer = rend2;
	}
});
