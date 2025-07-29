function map_click_event(e) {
    let latitude = e.latlng.lat.toFixed(4);
    let longitude = e.latlng.lng.toFixed(4);

    fetch(API_BASE_URL + "/add_marker", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({ lat: latitude, lon: longitude }),
    })
    .then(res => {
        return res.json();
    })
    .then(data => {
        addNewMarker(latitude, longitude, data.marker);
    })
    .catch(error => {
        console.error('Error adding marker:', error);
        showModal('Error', 'Error adding marker!', 'error');
    });
}

function map_move_event() {
    let new_center = map_10d8ba379c84a8a32988e7436c041a4b.getCenter();
    let changed_value = Math.abs(new_center.lat - old_center.lat) + Math.abs(new_center.lng - old_center.lng);
    
    if (changed_value >= 0.0001) {
        fetch(API_BASE_URL + "/change_center", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({ lat: new_center.lat, lon: new_center.lng }),
        })
        .catch(error => {
            console.error('Error updating center:', error);
        });
    }
    
    old_center = new_center;
}

function initializeMapEvents() {
    map_10d8ba379c84a8a32988e7436c041a4b.on('click', map_click_event);
    map_10d8ba379c84a8a32988e7436c041a4b.on('moveend', map_move_event);
} 