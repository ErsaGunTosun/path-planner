import React from 'react'
import { FaGear,FaChartSimple,FaSliders } from "react-icons/fa6";

function TopMenu() {
  return (
    <div className="top-menu fixed top-5 right-5 z-50 flex flex-col gap-2">

    <button className="menu-button w-12 h-12 bg-white cursor-pointer flex justify-center items-center rounded-full"  title="İstatistikler">
      <FaChartSimple className="text-xl" />
    </button>

    <button className="menu-button w-12 h-12 bg-white cursor-pointer flex justify-center items-center rounded-full" title="Kontroller">
      <FaGear className="text-xl" />
      </button>
    <button className="menu-button w-12 h-12 bg-white cursor-pointer flex justify-center items-center rounded-full" title="Ayarlar">
      <FaSliders className="text-xl" />
      </button>

  </div>
  )
}

export default TopMenu