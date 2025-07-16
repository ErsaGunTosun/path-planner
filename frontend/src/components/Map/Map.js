import React from 'react'

export default function Map() {
  return (
    <div class="map-container fixed top-0 left-0 w-full h-full z-1" >
      <iframe id="mapFrame" class="map-frame w-full h-full border-none" src="http://127.0.0.1:5000/map" title="Folium Map">
      </iframe>
    </div>
  )
}
