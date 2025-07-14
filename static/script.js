console.log("script.js loaded");

let activePanel = null;

function togglePanel(panelId) {
    const panel = document.getElementById(panelId);
    const button = event.target.closest('.menu-button');

    if (activePanel && activePanel !== panelId) {
        closePanel(activePanel);
    }

    if (panel.classList.contains('active')) {
        closePanel(panelId);
    } else {
        showPanel(panelId);
        button.classList.add('active');
        activePanel = panelId;
    }
}

function showPanel(panelId) {
    const panel = document.getElementById(panelId);
    panel.classList.add('active');
}

function closePanel(panelId) {
    const panel = document.getElementById(panelId);
    const buttons = document.querySelectorAll('.menu-button');

    panel.classList.remove('active');
    buttons.forEach(btn => btn.classList.remove('active'));
    activePanel = null;
}