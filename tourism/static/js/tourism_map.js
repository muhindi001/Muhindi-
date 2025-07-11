function getQueryParams() {
    const params = new URLSearchParams(window.location.search);
    return {
        lat: parseFloat(params.get("lat")),
        lng: parseFloat(params.get("lng")),
        name: params.get("name"),
    };
}

function initMap() {
    const queryParams = getQueryParams();

    // Default center (Tanzania) if no query parameters are provided
    const center = queryParams.lat && queryParams.lng
        ? { lat: queryParams.lat, lng: queryParams.lng }
        : { lat: -6.369028, lng: 34.888822 };

    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: queryParams.lat && queryParams.lng ? 10 : 6,
        center: center,
    });

    // Add a marker for the queried location
    if (queryParams.lat && queryParams.lng) {
        const marker = new google.maps.Marker({
            position: center,
            map: map,
            title: queryParams.name || "Selected Location",
        });

        const infoWindow = new google.maps.InfoWindow({
            content: `<h3>${queryParams.name || "Selected Location"}</h3>`,
        });

        marker.addListener("click", function () {
            infoWindow.open(map, marker);
        });
    }

    // Dynamic locations array
    var locations = JSON.parse(document.getElementById("map").dataset.locations);

    // Check if locations array is empty
    if (locations.length === 0) {
        console.error("No locations available to display on the map.");
        return;
    }

    // Add markers with info windows
    locations.forEach(function (location) {
        var marker = new google.maps.Marker({
            position: { lat: location.lat, lng: location.lng },
            map: map,
            title: location.name,
        });

        // Add an info window for each marker
        var infoWindow = new google.maps.InfoWindow({
            content: `<h3>${location.name}</h3><p>${location.description}</p>`,
        });

        marker.addListener("click", function () {
            infoWindow.open(map, marker);
        });
    });
}

// Handle Google Maps API loading errors
window.gm_authFailure = function () {
    alert("Failed to load Google Maps. Please check your API key.");
};