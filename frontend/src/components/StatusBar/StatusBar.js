import React from 'react'

function StatusBar({ isMarkeMode, isObstacleMode }) {
    return (
        <div className="status-bar fixed z-50 left-12 top-5">
            <button
            className="flex items-center space-x-2 px-4 py-2 rounded-full bg-white transition-colors duration-200">
            <span className="text-gray-800 text-sm font-medium whitespace-nowrap">Status
                <span className={`ml-2 text-xs font-semibold ${isMarkeMode ? 'text-green-500' : isObstacleMode ? 'text-red-500' : 'text-gray-500'}`}>
                {
                    isMarkeMode ? "Marker Mode" : isObstacleMode ? "Obstacle Mode" : "Move Mode"
                }
                </span>
            </span>
          </button>
        </div>
    )
}

export default StatusBar