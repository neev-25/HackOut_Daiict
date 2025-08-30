import React from 'react'
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet'


export default function MapView({ affected }) {
const style = (feature) => ({
weight: 1,
color: '#333',
fillOpacity: 0.6,
fillColor: '#d9534f'
})
return (
<div style={{ height: 420 }}>
<MapContainer center={[21.6, 72.1]} zoom={10} style={{ height: '100%' }}>
<TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
{affected?.features && <GeoJSON data={affected} style={style} />}
</MapContainer>
</div>
)
}