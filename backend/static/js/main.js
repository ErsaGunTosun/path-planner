function initializeApplication(centerData, markersData, pathDataParam) {
    initializeTemplateData(centerData, markersData, pathDataParam);
    
    initializeMap();
    
    loadExistingMarkers();
    
    renderPaths();
    
    initializeMapEvents();
    
    initializeRobotEventListeners();
}

function initializeRobotEventListeners() {
    document.getElementById('robot-start').addEventListener('click', robotStart);
    document.getElementById('robot-stop').addEventListener('click', robotStop);
    document.getElementById('robot-pause').addEventListener('click', robotPause);
    
    document.getElementById('robot-header').addEventListener('click', toggleRobotPanel);
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('Application ready for initialization');
}); 