let map_10d8ba379c84a8a32988e7436c041a4b;
let old_center;
let markers;
let pathData;
let markerObjects = {};
let robotMarker = null;
let robotUpdateInterval = null;
let robotStatus = 'stopped';
let isRobotPanelOpen = false;

const API_BASE_URL = "http://127.0.0.1:5000";
const ROBOT_UPDATE_INTERVAL = 500;

let center;

function initializeTemplateData(centerData, markersData, pathDataParam) {
    center = centerData;
    markers = markersData;
    pathData = pathDataParam;
} 