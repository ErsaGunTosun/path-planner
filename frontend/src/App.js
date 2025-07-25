import React, { useState, useEffect } from 'react';

import Map from './components/Map/Map';
import TopMenu from './components/TopMenu/TopMenu';
import ControlPanel from './components/ControlPanel/ControlPanel';
import BookmarksPanel from './components/BookmarksPanel/BookmarksPanel';
import StatusBar from './components/StatusBar/StatusBar';

function App() {
  const [menuBtn, setMenuBtn] = useState("");
  const [mapSrc, setMapSrc] = useState("http://127.0.0.1:5000/map");
  const [isMarkeMode, setIsMarkeMode] = useState(true);
  const [isObstacleMode, setIsObstacleMode] = useState(false);
  const [isMapLoading, setIsMapLoading] = useState(false);

  const handleMenuBtnClick = (value) => {
    if (value === menuBtn) {
      value = "";
    }
    setMenuBtn(value)
  };

  const handleCreatePath = () => {
    setIsMapLoading(true);
    fetch("http://127.0.0.1:5000/path/create", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    })
      .then(response => {
        if (response.ok) {
          const timestamp = new Date().getTime();
          setMapSrc(`http://127.0.0.1:5000/map?t=${timestamp}`);
        } else {
          setIsMapLoading(false);
          throw new Error('Network response was not ok');
        }
      })
      .catch(error => {
        setIsMapLoading(false);
        console.error('Error creating path:', error);
      });
  };

  const handleCreateAStarPath = () => {
    setIsMapLoading(true);
    fetch("http://127.0.0.1:5000/path/create_astar", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          const timestamp = new Date().getTime();
          setMapSrc(`http://127.0.0.1:5000/map?t=${timestamp}`);
        } else {
          setIsMapLoading(false);
          throw new Error('Network response was not ok');
        }
      })
      .catch(error => {
        setIsMapLoading(false);
      });
  };

  const handleClearMap = () => {
    setIsMapLoading(true);
    fetch("http://127.0.0.1:5000/path/clear", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    })
      .then(response => {
        if (response.ok) {
          const timestamp = new Date().getTime();
          setMapSrc(`http://127.0.0.1:5000/map?t=${timestamp}`);
        } else {
          setIsMapLoading(false);
          throw new Error('Network response was not ok');
        }
      })
      .catch(error => {
        setIsMapLoading(false);
        console.error('Error clearing map:', error);
      });
  };

  const handleBookmarkLoad = () => {
    const timestamp = new Date().getTime();
    setMapSrc(`http://127.0.0.1:5000/map?t=${timestamp}`);
  };

  useEffect(() => {
    if (mapSrc.includes('?t=')) {
      setIsMapLoading(true);
    }
  }, [mapSrc]);

  useEffect(() => {
    if (sessionStorage.getItem("isMarkeMode")) {
      setIsMarkeMode(sessionStorage.getItem("isMarkeMode") === "true");
      fetch("http://127.0.0.1:5000/options/marker", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({ isMarkeMode: sessionStorage.getItem("isMarkeMode") === "true" }),

      })
    }
    else {
      sessionStorage.setItem("isMarkeMode", "true");
    }

    if (sessionStorage.getItem("isObstacleMode")) {
      setIsObstacleMode(sessionStorage.getItem("isObstacleMode") === "true");
      fetch("http://127.0.0.1:5000/options/obstacle", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({ isObstacleMode: sessionStorage.getItem("isObstacleMode") === "true" }),

      })
    }
    else {
      sessionStorage.setItem("isObstacleMode", "false");
      setIsObstacleMode(false);
    }

  }, []);

  return (
    <div className="App">
      
      <StatusBar
        isMarkeMode={isMarkeMode}
        isObstacleMode={isObstacleMode}
        pathCreateFunction={handleCreatePath}
        astarPathCreateFunction={handleCreateAStarPath}
        clearMapFunction={handleClearMap}
      />

      <TopMenu handleMenuBtnClick={handleMenuBtnClick} />
      <Map mapSrc={mapSrc} isMapLoading={isMapLoading} setIsMapLoading={setIsMapLoading} />
      <ControlPanel menuBtn={menuBtn} handleMenuBtnClick={handleMenuBtnClick} isMarkeMode={isMarkeMode}
        isObstacleMode={isObstacleMode} setIsMarkeMode={setIsMarkeMode} setIsObstacleMode={setIsObstacleMode} />
      <BookmarksPanel menuBtn={menuBtn} handleMenuBtnClick={handleMenuBtnClick} onBookmarkLoad={handleBookmarkLoad} />
    </div>
  );
}

export default App;
