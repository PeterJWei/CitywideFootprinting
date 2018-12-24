require([
  "esri/Map",
  "esri/layers/CSVLayer",
  "esri/views/MapView",
  "esri/widgets/Legend",
  "esri/widgets/Home",
  "esri/layers/support/Field"
], function(Map, CSVLayer, MapView, Legend, Home, Field) {
	var url3 = "http://icsl.ee.columbia.edu:8001/static/venueLocations.csv";
	var csvLayer3 = new CSVLayer({
	 	url: url3,
	 	copyright: "Foursquare Data",
	 	fields: [new Field({"name":"hour", "alias":"hour", "type":"Number"})]
	});
	console.log(csvLayer3.fields);

  	var map3 = new Map({
    	basemap: "dark-gray",
    	layers: [csvLayer3]
  	});

  	var view3 = new MapView({
    	container: "viewDiv3",  // Reference to the DOM node that will contain the view
    	center: [-74.006,40.7128],
    	zoom:11,
    	map: map3               // References the map object created in step 3
  	});
  	console.log("Hello World");

	var slider3 = document.getElementById("slider3");
	var sliderValue3 = document.getElementById("sliderValue3");
	var playButton3 = document.getElementById("playButton3");
	var animation3 = null;

	function inputHandler3() {
		stopAnimation3();
		setYear3(parseInt(slider3.value));
	}
	slider3.addEventListener("input", inputHandler3);
	slider3.addEventListener("change", inputHandler3);


	// Toggle animation on/off when user
	// clicks on the play button
	playButton3.addEventListener("click", function () {
		if (playButton3.classList.contains("toggled")) {
			stopAnimation3();
		} else {
			startAnimation3();
		}
	});

	// view.ui.empty("top-left");
	// view.ui.add(new Home({view: view}), "top-left");
	view3.ui.add(new Legend({view: view3}), "bottom-left");



function createRenderer3(year) {
	console.log(year)
	var opacityStops = [{
    opacity: 0,
    value: year - 2},{
 //  },{
	// 	opacity: 1,
	// 	value: year - 1
	// },{
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
          color: "#f00",
          label: Math.floor(year) + ":00"
        }, {
          value: year - 1,
          color: "#880",
          label: mod((Math.floor(year) - 1),24)+":00"
        }, {
          value: year - 2,
          color: "#0f0",
          label: mod((Math.floor(year) - 2),24)+":00"
        }]
      }]
    };
  }
  function mod(n, m) {
    return ((n % m) + m) % m;
  }

	function startAnimation3() {
		stopAnimation3();
		animation3 = animate3(parseFloat(slider3.value));
		playButton3.classList.add("toggled");
	}

      /**
       * Stops the animations
       */
      function stopAnimation3() {
        if (!animation3) {
          return;
        }

        animation3.remove();
        animation3 = null;
        playButton3.classList.remove("toggled");
      }

      /**
       * Animates the color visual variable continously
       */
      function animate3(startValue) {
        var animating = true;
        var value = startValue;

        var frame3 = function (timestamp) {
          if (!animating) {
            return;
          }

          value += 0.5;
          if (value >= 24) {
            value = 0;
          }

          setYear3(value);

          // Update at 30fps
          setTimeout(function () {
            requestAnimationFrame(frame3);
          }, 1000 / 30);
        };

        frame3();

        return {
          remove: function () {
            animating = false;
          }
        };
      }
  	setYear3(0);

	function setYear3(value) {
		sliderValue3.innerHTML = Math.floor(value)+":00";
		slider3.value = Math.floor(value);
		var rend = createRenderer3(value);
		csvLayer3.renderer = rend;
	}
});