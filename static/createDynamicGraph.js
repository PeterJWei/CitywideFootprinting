
	var $btn = document.getElementById("updateGraph");
	$btn.addEventListener("click", toggleButtonGraph);

	function toggleButtonGraph() {
		console.log(document.getElementById("updateGraph").value);
		if (document.getElementById("updateGraph").value=="ON") {
			document.getElementById("updateGraph").value="OFF";
			document.getElementById("updateGraph").style.background='#ff0000';
		} else {
			document.getElementById("updateGraph").value="ON";
			document.getElementById("updateGraph").style.background='#00ff00';
		}
	}

	function printElements(data) {
		var i = 0;
		for (i=0; i<data.length; i++) {
			console.log(data[i].id());
		}
	}

	function clearData() {
		var cy = window.value;
		var all = cy.$();
		var i = 0;
		for (i=0; i<all.length; i++) {
			if (all[i].isEdge()) {
				all[i].style({'line-color':'#D3C0CD'});
			} else {
				all[i].style({'background-color':'#E3DFFF'});
			}
		}
	}

	function updateGraphEdges() {
		var result = null;
		$.get("/graph/",{
			},
			function(data,status){
	    	console.log(data,status);
	    	paintGraph(data);
	    },'json').fail(function() {
		    alert('Error!'); // or whatever			    
		    //document.getElementById("cameraButton").reset();
		});

		

	}
	setInterval(updateGraphEdges, 10000);
	function hexToRgb(hex) {
	    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
	    return result ? {
	        r: parseInt(result[1], 16),
	        g: parseInt(result[2], 16),
	        b: parseInt(result[3], 16)
	    } : null;
	}
	function rgbToHex(r, g, b) {
    	return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
	}
	function paintGraph(data) {
		if (document.getElementById("updateGraph").value=="OFF") {
			clearData();
		} else {
			console.log(data.length);
			for (var k=0; k < data.length; k++) {
				var obj = data[k];
				console.log(obj.traffic);
				var cy = window.value;
				var N = cy.getElementById(obj.id);
				var neighborhood = cy.$('#'+obj.id).neighborhood();
				var oldNeighborhood = neighborhood.add(N);
				//printElements(oldNeighborhood);
				var newNeighborhood = oldNeighborhood.openNeighborhood();
				newNeighborhood = newNeighborhood.subtract(oldNeighborhood);
				//console.log("new Neighborhood");
				//#printElements(newNeighborhood);
				N.style({'background-color':'#FFDFFF'});
				var i = 0;
				setTimeout( function () {
					for (i=0; i < neighborhood.length; i++) {
						//console.log(neighborhood[i].id());
						if (neighborhood[i].isEdge()) {
							var lineColor = neighborhood[i].data('line-color');
							//console.log(lineColor);
							//console.log(hexToRgb(lineColor).r);
							neighborhood[i].style({'line-color':'#A3DFFF'});
						} else {
							neighborhood[i].style({'background-color':'#A3DFFF'});
						}
					}
				},1000);
				
				i = 0;
				setTimeout( function() {
					for (i=0; i < newNeighborhood.length; i++) {
						//console.log(newNeighborhood[i].id());
						if (newNeighborhood[i].isEdge()) {
							newNeighborhood[i].style({'line-color':'#73DFFF'});
						} else {
							newNeighborhood[i].style({'background-color':'#73DFFF'});
						}
					}
				},2000);
			}
		}
	}