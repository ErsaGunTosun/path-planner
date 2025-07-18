import React, { useState, useEffect } from 'react'

import { IoCloseSharp } from "react-icons/io5";

import Bookmarks from '../Bookmarks/Bookmarks';

function BookmarksPanel({ menuBtn, handleMenuBtnClick }) {
    const [showPanel, setShowPanel] = useState(false);

    const handleClosePanel = () => {
        setShowPanel(false);
        handleMenuBtnClick("");
    };

    useEffect(() => {
        if (menuBtn === "bookmarks") {
            setShowPanel(true);
        } else {
            setShowPanel(false);
        }
    }, [menuBtn]);

    return (
        <div id="bookmarks" className={`overlay-panel bg-white fixed bottom-5 left-5 w-80 max-h-96 rounded-lg z-50 pb-5 ${showPanel ? 'translate-y-0 opacity-100' : 'translate-y-full opacity-0'} transition-all duration-300 ease-in-out`}>
            <div className="panel-header px-4 py-2 flex items-center justify-between bg-gray shadow-sm rounded-t-lg">
                <span>Bookmarks</span>
                <button className="close-btn" onClick={() => handleClosePanel()}>
                    <IoCloseSharp />
                </button>
            </div>
            <div className="panel-content flex flex-col gap-y-3 p-3 overflow-y-auto">
                <Bookmarks />
                <Bookmarks />
                <Bookmarks />
            </div>
        </div>
    )
}

export default BookmarksPanel