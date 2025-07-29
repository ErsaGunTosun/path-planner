function updateRobotPosition() {
    fetch(API_BASE_URL + "/robot/status")
        .then(response => response.json())
        .then(data => {
            if (data.status === "success" && robotMarker) {
                const robotData = data.robot_status;
                robotMarker.setLatLng([robotData.lat, robotData.lon]);
                
                if (robotData.status === 'completed') {
                    updateRobotStatus('stopped');
                    stopRobotTracking();
                    
                    if (robotMarker) {
                        map_10d8ba379c84a8a32988e7436c041a4b.removeLayer(robotMarker);
                        robotMarker = null;
                    }
                    
                    showModal('Success', 'Robot completed the path!', 'success');
                    return;
                }
                
                if (robotStatus === 'moving' && robotData.status === 'moving') {
                    fetch(API_BASE_URL + "/robot/update", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/x-www-form-urlencoded",
                        }
                    });
                }
            }
        })
        .catch(error => console.error('Robot position update error:', error));
}

function startRobotTracking() {
    if (robotUpdateInterval) {
        clearInterval(robotUpdateInterval);
    }
    robotUpdateInterval = setInterval(updateRobotPosition, ROBOT_UPDATE_INTERVAL);
}

function stopRobotTracking() {
    if (robotUpdateInterval) {
        clearInterval(robotUpdateInterval);
        robotUpdateInterval = null;
    }
}

function updateRobotStatus(status) {
    robotStatus = status;
    const statusElement = document.getElementById('robot-status');
    const startBtn = document.getElementById('robot-start');
    const pauseBtn = document.getElementById('robot-pause');
    const stopBtn = document.getElementById('robot-stop');
    
    statusElement.textContent = status;
    
    if (status === 'moving') {
        statusElement.style.color = '#059669';
    } else if (status === 'paused') {
        statusElement.style.color = '#d97706';
    } else {
        statusElement.style.color = '#dc2626';
    }
    
    startBtn.disabled = (status === 'moving');
    pauseBtn.disabled = (status === 'stopped');
    stopBtn.disabled = (status === 'stopped');
}

function robotStart() { 
    if (!pathData || !pathData.edges || pathData.edges.length === 0) {
        showModal('Error', 'No path available. Create a path first!', 'error');
        return;
    }
    
    fetch(API_BASE_URL + "/robot/start", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            if (data.message.includes("resumed") && robotMarker) {
                updateRobotStatus('moving');
                startRobotTracking();
                showModal('Success', data.message, 'success');
            } else {
                const firstEdge = pathData.edges[0];
                const firstWaypoint = firstEdge[0];
                
                if (robotMarker) {
                    map_10d8ba379c84a8a32988e7436c041a4b.removeLayer(robotMarker);
                }
                
                createRobotMarker(firstWaypoint[0], firstWaypoint[1]);
                
                updateRobotStatus('moving');
                startRobotTracking();
                showModal('Success', data.message, 'success');
            }
        } else {
            showModal('Error', data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showModal('Error', 'Network error occurred', 'error');
    });
}

function robotStop() {
    fetch(API_BASE_URL + "/robot/stop", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            updateRobotStatus('stopped');
            stopRobotTracking();
            
            if (robotMarker) {
                map_10d8ba379c84a8a32988e7436c041a4b.removeLayer(robotMarker);
                robotMarker = null;
            }
        }
    })
    .catch(error => console.error('Error:', error));
}

function robotPause() {
    fetch(API_BASE_URL + "/robot/pause", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            updateRobotStatus('paused');
            stopRobotTracking();
        }
    })
    .catch(error => console.error('Error:', error));
}

function toggleRobotPanel() {
    const content = document.getElementById('robot-content');
    const arrow = document.getElementById('robot-arrow');
    
    if (isRobotPanelOpen) {
        content.style.maxHeight = '0px';
        content.style.opacity = '0';
        arrow.style.transform = 'rotate(180deg)';
        arrow.innerHTML = '▼';
        isRobotPanelOpen = false;
    } else {    
        content.style.maxHeight = '200px';
        content.style.opacity = '1';
        arrow.style.transform = 'rotate(0deg)';
        arrow.innerHTML = '▲';
        isRobotPanelOpen = true;
    }
} 