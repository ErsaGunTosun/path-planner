import React from 'react'

function StatusBar({ isMarkeMode, isObstacleMode, pathCreateFunction, clearMapFunction }) {

  

    return (
        <div className="status-bar fixed z-50 left-12 top-5 flex gap-2">

            <button
                className="flex items-center space-x-2 px-3 py-2 rounded-full bg-white hover:bg-gray-100 "
                onClick={pathCreateFunction}>
                <span className="text-gray-800 text-sm font-medium whitespace-nowrap">Create Path
                </span>
            </button>

            <button
                className="flex items-center space-x-2 px-3 py-2 rounded-full bg-white hover:bg-gray-100 "
                onClick={clearMapFunction}>
                <span className="text-gray-800 text-sm font-medium whitespace-nowrap">Clear Map
                </span>
            </button>


            <p
                className="flex items-center space-x-2 px-3 py-2 rounded-full bg-white">
                <span className="text-gray-800 text-sm font-medium whitespace-nowrap">Status
                    <span className={`ml-2 text-xs font-semibold ${isMarkeMode ? 'text-green-500' : isObstacleMode ? 'text-red-500' : 'text-gray-500'}`}>
                        {   

                            isMarkeMode ? "Marker Mode" : isObstacleMode ? "Obstacle Mode" : "Move Mode"
                        }
                    </span>
                </span>
            </p>

        </div>
    )
}

export default StatusBar