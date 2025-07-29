function renderPaths() {
    if (pathData && pathData.edges) {
        pathData.edges.forEach(edge => {
            L.polyline(edge, {
                color: 'red',
                weight: 4,
                opacity: 0.8
            }).addTo(map_10d8ba379c84a8a32988e7436c041a4b);
        });
        
        if (pathData.alternatives && pathData.alternatives.length > 0) {
            pathData.alternatives.forEach((altPath, index) => {
                if (altPath && altPath.length > 0) {
                    altPath.forEach(edge => {
                        L.polyline(edge, {
                            color: 'green',
                            weight: 3,
                            opacity: 1,
                            dashArray: '5, 10'
                        }).addTo(map_10d8ba379c84a8a32988e7436c041a4b);
                    });
                }
            });
        }
    }
} 