
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

//global

var markers = [];

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

    google.maps.event.addListenerOnce(map, 'tilesloaded', function() {
      //displayRestaurantsInBounds(map.getBounds());
      // Create the DIV to hold the control and call the CenterControl()
      // constructor passing in this DIV.
      var centerControlDiv = document.createElement('div');
      var centerControl = new RedoSearch(centerControlDiv, map);

      centerControlDiv.index = 1;
      map.controls[google.maps.ControlPosition.BOTTOM_CENTER].push(centerControlDiv);

      var centerControlDiv2 = document.createElement('div');
      var placesFilter1 = new placesIveNeverBeenFilter(centerControlDiv2, map);

      centerControlDiv2.index = 2;
      map.controls[google.maps.ControlPosition.RIGHT_CENTER].push(centerControlDiv2);

      var centerControlDiv3 = document.createElement('div');
      var placesFilter2 = new criticRecommendedFilter(centerControlDiv3, map);

      centerControlDiv2.index = 3;
      map.controls[google.maps.ControlPosition.RIGHT_CENTER].push(centerControlDiv3);


      var centerControlDiv4 = document.createElement('div');
      var placesFilter3 = new highYelpRatingFilter(centerControlDiv4, map);

      centerControlDiv4.index = 3;
      map.controls[google.maps.ControlPosition.RIGHT_CENTER].push(centerControlDiv4);


    });

      var options = {
          imagePath: 'static/images/m'
      };
}


function RedoSearch(controlDiv, map) {

      // Set CSS for the control border.
      var controlUI = document.createElement('div');
      controlUI.style.backgroundColor = '#fff';
      controlUI.style.border = '2px solid #fff';
      controlUI.style.borderRadius = '3px';
      controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
      controlUI.style.cursor = 'pointer';
      controlUI.style.marginBottom = '22px';
      controlUI.style.textAlign = 'center';
      controlUI.title = 'Click to redo search in this area';
      controlDiv.appendChild(controlUI);

      // Set CSS for the control interior.
      var controlText = document.createElement('div');
      controlText.style.color = 'rgb(25,25,25)';
      controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
      controlText.style.fontSize = '16px';
      controlText.style.lineHeight = '38px';
      controlText.style.paddingLeft = '5px';
      controlText.style.paddingRight = '5px';
      controlText.innerHTML = 'Redo Search Here';
      controlUI.appendChild(controlText);

      // Setup the click event listeners: simply set the map to Chicago.
      // Setup the click event listeners: simply set the map to Chicago.
      controlUI.addEventListener('click', function() {
        displayRestaurantsInBounds(map)
      });
    }

function placesIveNeverBeenFilter(controlDiv, map) {

      // Set CSS for the control border.
      var controlUI = document.createElement('div');
      //checkbox.type = "checkbox";
      controlUI.style.backgroundColor = '#fff';
      controlUI.style.border = '2px solid #fff';
      controlUI.style.borderRadius = '3px';
      controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
      controlUI.style.cursor = 'pointer';
      controlUI.style.marginBottom = '22px';
      controlUI.style.textAlign = 'center';
      controlUI.title = "Filter results to restaurants I've never visited";
      controlUI.innerHTML = "Places I've never visited";
      controlDiv.appendChild(controlUI);

      // Set CSS for the control interior.
      var controlText = document.createElement('input');
      controlText.type = "checkbox";
      controlText.style.color = 'rgb(25,25,25)';
      controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
      controlText.style.fontSize = '16px';
      controlText.style.lineHeight = '38px';
      controlText.style.paddingLeft = '5px';
      controlText.style.paddingRight = '5px';
      controlUI.appendChild(controlText);

      // Setup the click event listeners: simply set the map to Chicago.
      // Setup the click event listeners: simply set the map to Chicago.
      controlUI.addEventListener('click', function() {
        console.log("Im going to limit results to new spots!")
      });
    }

    function criticRecommendedFilter(controlDiv, map) {

          // Set CSS for the control border.
          var controlUI = document.createElement('div');
          //checkbox.type = "checkbox";
          controlUI.style.backgroundColor = '#fff';
          controlUI.style.border = '2px solid #fff';
          controlUI.style.borderRadius = '3px';
          controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
          controlUI.style.cursor = 'pointer';
          controlUI.style.marginBottom = '22px';
          controlUI.style.textAlign = 'center';
          controlUI.title = "Filter results to restaurants I've never been to";
          controlUI.innerHTML = "Critic Recommended";
          controlDiv.appendChild(controlUI);

          // Set CSS for the control interior.
          var controlText = document.createElement('input');
          controlText.type = "checkbox";
          controlText.style.color = 'rgb(25,25,25)';
          controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
          controlText.style.fontSize = '16px';
          controlText.style.lineHeight = '38px';
          controlText.style.paddingLeft = '5px';
          controlText.style.paddingRight = '5px';
          controlUI.appendChild(controlText);

          // Setup the click event listeners: simply set the map to Chicago.
          // Setup the click event listeners: simply set the map to Chicago.
          controlUI.addEventListener('click', function() {
            console.log("Im going to limit results to critic recommendations")
          });
        }

function highYelpRatingFilter(controlDiv, map) {

      // Set CSS for the control border.
      var controlUI = document.createElement('div');
      //checkbox.type = "checkbox";
      controlUI.style.backgroundColor = '#fff';
      controlUI.style.border = '2px solid #fff';
      controlUI.style.borderRadius = '3px';
      controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
      controlUI.style.cursor = 'pointer';
      controlUI.style.marginBottom = '22px';
      controlUI.style.textAlign = 'center';
      controlUI.title = "Filter results to restaurants I've never been to";
      controlUI.innerHTML = "Highly Rated on Yelp";
      controlDiv.appendChild(controlUI);

      // Set CSS for the control interior.
      var controlText = document.createElement('input');
      controlText.type = "checkbox";
      controlText.style.color = 'rgb(25,25,25)';
      controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
      controlText.style.fontSize = '16px';
      controlText.style.lineHeight = '38px';
      controlText.style.paddingLeft = '5px';
      controlText.style.paddingRight = '5px';
      controlUI.appendChild(controlText);

      // Setup the click event listeners: simply set the map to Chicago.
      // Setup the click event listeners: simply set the map to Chicago.
      controlUI.addEventListener('click', function() {
        console.log("Im going to limit results to yelp recommendations")
      });
    }


function displayRestaurantsInBounds(map, max_results=20){
    //console.log("I should be displaying restaurants")
    var bounds = map.getBounds()
    clearMarkers()
    lats = bounds['f']
    lons = bounds['b']
    west = lats['b']
    east = lats['f']
    north = lons['f']
    south = lons['b']

    var data = {'west': west, 'east': east, 'south': south, 'north': north, 'max_results': max_results}
    //console.log("BOUNDS: ", bounds)
    $.post(
        '/restaurants/filter',
        data,
        function(results){
          if (results){
            var restaurants = JSON.parse(results)
            restaurants.map((restaurant) => displayRestaurant(map, restaurant))
          }

        }
     )
  }



function make_button(restaurant){
  safe_name = encodeURIComponent(restaurant['_id'])
  html = "<div><button id='been-to-"+safe_name+"'>I've been here!</button></div>"

  return html
}

function getWindowContent(restaurant){
  var been_here = make_button(restaurant)
  var title = "<div>" + restaurant['name'] + "</div>"+ "<br>"

  var rating = "<tr><th>Yelp Rating: </th> <td>" + restaurant['yelp']['rating'] + "</td></tr>"
  var rating_count = "<tr><th>Yelp Review Count: </th> <td>" + restaurant['yelp']['review_count'] + "</td></tr>"
  var price = "<tr><th>Yelp Price: </th> <td>" +  +restaurant['yelp']['price'] + "</td></tr>"
  var datatable = '<table class="w3-table-all"><tbody>'+rating+rating_count+price+"</tbody></table>"

  var img = "<img class='r-thumb' src='"+restaurant['image_url']+"'>"
  return title  + datatable+ img + been_here
}

function displayRestaurant(map, restaurant){
      console.log(restaurant)
      var lat = restaurant['coords']['lat']
      var lon = restaurant['coords']['lon']
      var name = restaurant['name']
      var id = restaurant['_id']
      var LatLng = {lat: lat, lng: lon};

      var marker = new google.maps.Marker({
        position: LatLng,
        map: map,
        title: name,
        id:id,
        content: content,
      });
      markers.push(marker)

      var content = getWindowContent(restaurant)

      var infowindow = new google.maps.InfoWindow({
        content: content,
      });
      marker.addListener('click', function() {
        infowindow.open(map, marker);
        var safe_name = encodeURIComponent(id)
        var button_id = "been-to-"+safe_name
        var button = document.getElementById(button_id)
        button.onclick = () => {console.log("You clicked ", button_id)}
      });

}

function geolocate(lat, lon){
    var url = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${lat},${lon}&key=AIzaSyA5_dtT8LKpUQH0drnSukH5TYQncEiezRg`
    $.get(
        url,
        function(response){console.log(response)}
    )
}

function handleLocationError(browserHasGeolocation) {
  console.log("Could not get location")
}

function setMapOnAll(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
  setMapOnAll(null);
  markers = [];
}
