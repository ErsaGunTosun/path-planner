function createWaypointIcon() {
    return L.AwesomeMarkers.icon({
        markerColor: "blue",
        iconColor: "white",
        prefix: "glyphicon",
        extraClasses: "fa-rotate-0",
        icon: "map-marker"
    });
}

function createObstacleIcon() {
    return L.AwesomeMarkers.icon({
        markerColor: "red",
        iconColor: "white",
        prefix: "fa",
        extraClasses: "fa-rotate-0",
        icon: "lock"
    });
}

function createRobotIcon() {
    return L.AwesomeMarkers.icon({
        markerColor: 'orange',
        iconColor: 'white',
        prefix: 'fa',
        icon: 'robot',
        extraClasses: 'fa-rotate-0'
    });
}

function createPopupContent(type, lat, lon, markerId) {
    const title = type === 'marker' ? 'Waypoint' : 'Obstacle';
    return '<div>' +
        '<strong>' + title + '</strong><br>' +
        'Lat: ' + parseFloat(lat).toFixed(4) + '<br>' +
        'Lon: ' + parseFloat(lon).toFixed(4) + '<br>' +
        '<button onclick="removeMarker(' + lat + ', ' + lon + ', \'' + markerId + '\')" ' +
                'style="background-color: #dc3545; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer; margin-top: 5px;">' +
            'Delete' +
        '</button>' +
    '</div>';
}

function loadExistingMarkers() {
    if (markers.length > 0) {
        markers.forEach((marker, index) => {
            const markerId = `marker_${index}_${marker.lat}_${marker.lon}`;
            let markerObj;
            let icon;
            
            if (marker.status === 'marker') {
                icon = createWaypointIcon();
            } else {
                icon = createObstacleIcon();
            }
            
            const popupContent = createPopupContent(marker.status, marker.lat, marker.lon, markerId);
            
            markerObj = L.marker([marker.lat, marker.lon], {icon: icon})
                .addTo(map_10d8ba379c84a8a32988e7436c041a4b)
                .bindPopup(popupContent);
            
            markerObjects[markerId] = markerObj;
        });
    }
}

function addNewMarker(latitude, longitude, markerData) {
    const newMarkerId = 'marker_new_' + latitude + '_' + longitude;
    let markerObj;
    let icon;
    
    if (markerData.status === 'marker') {
        icon = createWaypointIcon();
    } else if (markerData.status === 'obstacle') {
        icon = createObstacleIcon();
    }
    
    const popupContent = createPopupContent(markerData.status, latitude, longitude, newMarkerId);
    
    markerObj = L.marker([latitude, longitude], {icon: icon})
        .addTo(map_10d8ba379c84a8a32988e7436c041a4b)
        .bindPopup(popupContent);
    
    if (markerObj) {
        markerObjects[newMarkerId] = markerObj;
    }
}

function createRobotMarker(lat, lon) {
    const robotIcon = createRobotIcon();
    
    robotMarker = L.marker([lat, lon], {icon: robotIcon})
        .addTo(map_10d8ba379c84a8a32988e7436c041a4b)
        .bindPopup('<div><strong>🤖 Robot</strong><br>Status: ' + robotStatus + '</div>');
}

function removeMarker(lat, lon, markerId) {
    showModal(
        'Delete Marker',
        'Are you sure you want to delete this marker?',
        'warning',
        true
    ).then(confirmed => {
        if (confirmed) {
            fetch(API_BASE_URL + "/remove_marker", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({ lat: lat, lon: lon }),
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    if (markerObjects[markerId]) {
                        map_10d8ba379c84a8a32988e7436c041a4b.removeLayer(markerObjects[markerId]);
                        delete markerObjects[markerId];
                    }
                    showModal('Success', 'Marker deleted successfully!', 'success');
                } else {
                    showModal('Error', 'Error deleting marker: ' + data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showModal('Error', 'Error deleting marker!', 'error');
            });
        }
    });
} 