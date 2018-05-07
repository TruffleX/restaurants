//window.appConfig = {
//    debug: {% if env == 'development' %}true{% else %}false{% endif %},
//  }


//List of map events:
//bounds_changed
//center_changed
//click
//dblclick
//drag
//dragend
//dragstart
//heading_changed
//idle
//maptypeid_changed
//mousemove
//mouseout
//mouseover
//projection_changed
//resize
//rightclick
//tilesloaded
//zoom_changed
//tilt_changed

// globals
var markers = []

function markerFactory(map, lat, lng, id, title, content){
    var ids = markers.map(marker => marker.id)
    if (ids.includes(id) == false){
        var LatLng = {lat: lat, lng: lng};
        var marker = new google.maps.Marker({
          position: LatLng,
          map: map,
          title: title,
          id:id,
        });
        var infowindow = new google.maps.InfoWindow({
          content: title + "\n" + content
        });
        marker.addListener('click', function() {
          infowindow.open(map, marker);
        });
        markers.push(marker)
    }
}

function initMap() {

    var myLatLng = {lat: 38.028273, lng: -118.401568};

    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 4,
      center: myLatLng
    });

    google.maps.event.addListener(map, 'tilesloaded', function() {
        var bounds = map.getBounds()
        lats = bounds['f']
        lons = bounds['b']
        west = lats['b']
        east = lats['f']
        north = lons['f']
        south = lons['b']

        data = {'west': west, 'east': east, 'south': south, 'north': north}
        console.log(data)
        $.post(
            '/api/entries',
            data,
            function(results){
                var restaurants = JSON.parse(results)
                restaurants.map(restaurant => {
                    var lat = restaurant['coords']['lat']
                    var lon = restaurant['coords']['lon']
                    var name = restaurant['name']
                    var content = ""
                    var id = restaurant['_id']
                    markerFactory(map, lat, lon, id, name, content)
                })
            }
         )
    });
}