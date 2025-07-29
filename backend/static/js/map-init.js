// Map initialization
function initializeMap() {
    map_10d8ba379c84a8a32988e7436c041a4b = L.map(
        "map_10d8ba379c84a8a32988e7436c041a4b",
        {
            center: [center.lat, center.lon],
            crs: L.CRS.EPSG3857,
            zoom: 15,
            zoomControl: true,
            preferCanvas: false,
        }
    );
      
    old_center = {
        lat: map_10d8ba379c84a8a32988e7436c041a4b.options.center[0],
        lng: map_10d8ba379c84a8a32988e7436c041a4b.options.center[1]
    };

    // Add tile layer
    const tile_layer = L.tileLayer(
        "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            minZoom: 0,
            maxZoom: 19,
            maxNativeZoom: 19,
            noWrap: false,
            attribution: "&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors",
            subdomains: "abc",
            detectRetina: false,
            tms: false,
            opacity: 1,
        }
    );
    
    tile_layer.addTo(map_10d8ba379c84a8a32988e7436c041a4b);
} 