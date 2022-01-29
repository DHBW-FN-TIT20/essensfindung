function get_location() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(show_position);
    } else { 
      alert("Geolocation is not supported by this browser.");
    }
}

function show_position(position){
    console.log("Ausgabe Latitude:");
    console.log(position.coords.latitude);
    console.log("Ausgabe Longitude:")
    console.log(position.coords.longitude);
    document.getElementById("restaurant_filter_latitude").innerHTML = position.coords.latitude;
    document.getElementById("restaurant_filter_longitude").innerHTML = position.coords.longitude;
}