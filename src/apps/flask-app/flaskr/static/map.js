
// location initialization

// cut US into cells where each cell has a fixed number of restaurants
// get position of current view
// determine which cells the view is within
// load all locations from db in global data store that are within the cell
// add all restaurants in view to DOM, up to top N, sorted by bayesian rating estimate
    // dirichlet(a1, a2, a3, a4, a5).update(rating, count)

// location onMapChange

// get position of current view
// determine which cells the view is within
// if any cell is not loaded, load it in to global data store
// if any cell is no longer in view, delete all dom elements, and entries in data store
// add all restaurants in view to DOM, up to top N, sorted by bayesian rating estimate


$.getScript('static/markerclusterer.js', function(){console.load('Imported marker clusterer!')})

// globals
var markers = []

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};

function destroyLoader(){

    loader = document.getElementById('loader')
    loader.parentNode.removeChild(loader);
}

function initMap() {


    const DEFAULT_POS = {'lat': 34.018142, 'lng': -118.437873}

    var restaurantPromise = new Promise((resolve, reject)=>{
        $.get(
        '/restaurants',
        function(results){
            resolve(JSON.parse(results))
        })
    })

    restaurantPromise.then((restaurants) => {


        destroyLoader()

        console.log("We have " + typeof(restaurants))
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 18,
          center: DEFAULT_POS,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        // Try HTML5 geolocation.
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };

            console.log('Location found.');

            map.setCenter(pos)
            map.setZoom(18)
            var listener = google.maps.event.addListenerOnce(map, "idle", function() {
                if (map.getZoom() < 18) map.setZoom(18);
            });
          }, function() {
            handleLocationError(true);
          });
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false);
        }
          function handleLocationError(browserHasGeolocation) {
            console.log("Could not get location")
        }

        restaurants.map(restaurant => {
            var lat = restaurant['coords']['lat']
            var lon = restaurant['coords']['lon']
            var name = restaurant['name']
            var content = "<img class='r-thumb' src='"+restaurant['image_url']+"'>"
            var id = restaurant['_id']

            var LatLng = {lat: lat, lng: lon};
            var marker = new google.maps.Marker({
              position: LatLng,
              map: null,
              title: name,
              id:id,
            });
            var infowindow = new google.maps.InfoWindow({
              content: "<div>" + name + "</div>"+ "<br>" //+ "<div>" + content + "</div>"
            });
            marker.addListener('click', function() {
              infowindow.open(map, marker);
            });
            markers.push(marker)
        })

        var options = {
            imagePath: 'static/images/m'
        };
        var markerCluster = new MarkerClusterer(map, markers, options);
    })


    var update = function() {
        console.log("UPDATING")
        var bounds = map.getBounds()
        lats = bounds['f']
        lons = bounds['b']
        west = lats['b']
        east = lats['f']
        north = lons['f']
        south = lons['b']

        data = {'west': west, 'east': east, 'south': south, 'north': north}
    };

    function getRestaurantsInBounds(){
        var bounds = map.getBounds()
        lats = bounds['f']
        lons = bounds['b']
        west = lats['b']
        east = lats['f']
        north = lons['f']
        south = lons['b']

        var data = {'west': west, 'east': east, 'south': south, 'north': north}

        $.post(
            '/restaurants/filter',
            data,
            function(results){console.log("Got " + results.length + " restaurants in current view")}
         )
    }

    google.maps.event.addListener(map, 'dragend', update)
    //document.onload = update
}


function geolocate(lat, lon){
    var url = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${lat},${lon}&key=AIzaSyA5_dtT8LKpUQH0drnSukH5TYQncEiezRg`
    $.get(
        url,
        function(response){console.log(response)}
    )

}