function initMap() {
var myLatLng = {lat: 38.028273, lng: -118.401568};

var map = new google.maps.Map(document.getElementById('map'), {
  zoom: 4,
  center: myLatLng
});

var marker = new google.maps.Marker({
  position: myLatLng,
  map: map,
  title: 'My Home'
});

var infowindow = new google.maps.InfoWindow({
  content: "This is a place."
});

marker.addListener('click', function() {
  infowindow.open(map, marker);
});

}

var url = "https://maps.googleapis.com/maps/api/js?key="+api_key+"&callback=initMap"
$.getScript(url, function() {
alert('Load was performed.');
<!--async defer-->
});