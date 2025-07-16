import React, { useEffect, useState } from 'react'

import { IoCloseSharp } from "react-icons/io5";


function ControlPanel({ menuBtn, handleMenuBtnClick }) {
  const [showPanel, setShowPanel] = useState(false);
  const [isMarkeMode, setIsMarkeMode] = useState(true);
  const [isObstacleMode, setIsObstacleMode] = useState(false);

  useEffect(() => {
    if (menuBtn === "controls") {
      setShowPanel(true);
    } else {
      setShowPanel(false);
    }
  }, [menuBtn]);

  const handleClosePanel = () => {
    setShowPanel(false);
    handleMenuBtnClick("");
  };

  const handleToggleMarkerMode = () => {
    setIsMarkeMode(!isMarkeMode);
    if (!isMarkeMode) {
      setIsObstacleMode(false);
    }
  };

  const handleToggleObstacleMode = () => {
    setIsObstacleMode(!isObstacleMode);
    if (!isObstacleMode) {
      setIsMarkeMode(false);
    }
  };

  return (
    <div id="controls" className={`overlay-panel bg-white fixed bottom-5 left-5 w-80 max-h-96 rounded-lg z-50 pb-10 ${showPanel ? 'translate-y-0 opacity-100' : 'translate-y-full opacity-0'} transition-all duration-300 ease-in-out`}>
      <div className="panel-header px-4 py-2 flex items-center justify-between bg-gray-200 rounded-t-lg">
        <span>Control Panel</span>
        <button className="close-btn" onClick={() => handleClosePanel()}>
          <IoCloseSharp />
        </button>
      </div>
      <div className="panel-content flex flex-col gap-y-2 p-5">

        <label className="inline-flex items-center justify-between cursor-pointer">
          <span className="ms-3 text-sm font-medium text-gray-900 dark:text-gray-300">Checked toggle</span>
          <input type="checkbox" value="" className="sr-only peer" checked={isMarkeMode} onClick={() => {
          handleToggleMarkerMode();}} />
          <div className="relative w-9 h-5 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600 dark:peer-checked:bg-blue-600"></div>
        </label>

        <label className="inline-flex items-center justify-between cursor-pointer">
          <span className="ms-3 text-sm font-medium text-gray-900 dark:text-gray-300">Checked toggle</span>
          <input type="checkbox" value="" className="sr-only2 peer2"  checked={isObstacleMode} onClick={() => {
          handleToggleObstacleMode();
        }}/>
          <div className="relative w-9 h-5 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600 dark:peer-checked:bg-blue-600"></div>
        </label>

      </div>
    </div>
  )
}

export default ControlPanel