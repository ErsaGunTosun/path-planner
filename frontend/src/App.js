import React, {useState,useEffect} from 'react';
import axios from 'axios';

import Map from './components/Map/Map';
import TopMenu from './components/TopMenu/TopMenu';
import ControlPanel from './components/ControlPanel/ControlPanel';
function App() {
  const [menuBtn, setMenuBtn] = useState("");

  const handleMenuBtnClick = (value) => {
    if (value === menuBtn) {
      value = "";
    }

    setMenuBtn(value)
  };

  return (
    <div className="App">
      <TopMenu handleMenuBtnClick={handleMenuBtnClick} />
      <Map />
      <ControlPanel menuBtn={menuBtn} handleMenuBtnClick={handleMenuBtnClick} />
    </div>
  );
}

export default App;
