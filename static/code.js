fetch('data.json', {mode: 'no-cors'})
  .then(function(res) {
    return res.json()
  })
  .then(function(data) {
    var cy = window.cy = cytoscape({
      container: document.getElementById('cy'),
      boxSelectionEnabled: false,

      layout: {
        name: 'preset'
      },

      style: [
        {
          selector: 'node',
          style: {
            'height': 0.0005,
            'width': 0.0005,
            'background-color': '#E3DFFF'
          }
        },

        {
          selector: 'edge',
          style: {
            'curve-style': 'haystack',
            'haystack-radius': 0,
            'width': 0.00025,
            'opacity': 0.5,
            'line-color': '#D3C0CD'
          }
        }
      ],
      motionBlur: true,
      elements: data
    });
    window.value = cy;
  });