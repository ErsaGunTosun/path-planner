import React from 'react'
import { IoTrashSharp } from "react-icons/io5";
function Bookmarks() {
  return (
    <>
      <div className="bookmark-item flex  justify-between p-2 bg-gray-100 rounded-lg shadow-sm">
        <div className='flex flex-col items-start'>
          <span className="bookmark-title">Bookmark Title</span>
          <span className="bookmark-description text-xs text-gray-600">This is a description of the bookmark.</span>
          <button className="bookmark-edit-btn text-sm bg-green-500 text-white px-2 py-1 rounded hover:bg-green-600 transition-colors duration-200 mt-1">
            Apply to Map
          </button>
        </div>
        <div className="bookmark-actions flex justify-between items-center gap-x-2 pt-2">
          <button className="bookmark-delete-btn text-red-500 hover:text-red-700">
            <IoTrashSharp />
          </button>
        </div>
      </div>
    </>
  )
}

export default Bookmarks