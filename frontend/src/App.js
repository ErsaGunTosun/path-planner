import React, { useState, useEffect } from 'react';

import Map from './components/Map/Map';
import TopMenu from './components/TopMenu/TopMenu';
import ControlPanel from './components/ControlPanel/ControlPanel';
import StatusBar from './components/StatusBar/StatusBar';

function App() {
  const [menuBtn, setMenuBtn] = useState("");
  const [isMarkeMode, setIsMarkeMode] = useState(true);
  const [isObstacleMode, setIsObstacleMode] = useState(false);

  const handleMenuBtnClick = (value) => {
    if (value === menuBtn) {
      value = "";
    }

    setMenuBtn(value)
  };


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
      <StatusBar isMarkeMode={isMarkeMode} isObstacleMode={isObstacleMode} />
      <TopMenu handleMenuBtnClick={handleMenuBtnClick} />
      <Map />
      <ControlPanel menuBtn={menuBtn} handleMenuBtnClick={handleMenuBtnClick} isMarkeMode={isMarkeMode}
        isObstacleMode={isObstacleMode} setIsMarkeMode={setIsMarkeMode} setIsObstacleMode={setIsObstacleMode} />
    </div>
  );
}

export default App;
