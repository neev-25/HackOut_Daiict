import React, { useEffect, useState } from 'react'
import { getSeries } from '../services/api'

export default function SeriesPanel() {
  const [rows, setRows] = useState([])

  useEffect(() => {
    getSeries()
      .then(res => setRows(res.data))
      .catch(() => {})
  }, [])

  return (
    <pre
      style={{
        maxHeight: 200,
        overflow: 'auto',
        background: '#fafafa',
        padding: 12
      }}
    >
      {JSON.stringify(rows.slice(-10), null, 2)}
    </pre>
  )
}
