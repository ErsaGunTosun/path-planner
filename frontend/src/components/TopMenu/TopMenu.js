import React from 'react'
import { FaGear,FaChartSimple,FaBookmark } from "react-icons/fa6";

function TopMenu({handleMenuBtnClick}) {
  return (
    <div className="top-menu fixed top-5 right-5 z-50 flex flex-col gap-2">

    <button onClick={() => handleMenuBtnClick("controls")}
    className="menu-button w-12 h-12 bg-white cursor-pointer flex justify-center items-center rounded-full">
      <FaGear className="text-xl" />
      </button>
    <button onClick={() => handleMenuBtnClick("bookmarks")}
     className="menu-button w-12 h-12 bg-white cursor-pointer flex justify-center items-center rounded-full">
      <FaBookmark className="text-xl" />
      </button>

  </div>
  )
}

export default TopMenu