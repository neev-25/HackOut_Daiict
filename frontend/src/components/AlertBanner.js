import React from 'react'
const COLORS = ['#2e7d32', '#f9a825', '#fb8c00', '#c62828']
const LABELS = ['SAFE','MINOR','MODERATE','SEVERE']


export default function AlertBanner({ severity, effects }){
const sev = Number(severity ?? 0)
return (
<div style={{ margin:'12px 0', padding:12, borderRadius:8, background:COLORS[sev] || COLORS[0], color:'white' }}>
<b>Status: {LABELS[sev] || LABELS[0]}</b>
<ul>
{(effects||[]).map((e,i)=>(<li key={i}>{e}</li>))}
</ul>
</div>
)
}