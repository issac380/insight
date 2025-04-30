import React, { useEffect, useState } from 'https://esm.sh/react@18.2.0'
import ReactDOM from 'https://esm.sh/react-dom@18.2.0/client'

function App() {
  const [reports, setReports] = useState([])

  useEffect(() => {
    console.log("🚀 React app mounted")
    const eventSource = new EventSource("http://localhost:8000/api/stream")

    eventSource.onmessage = (event) => {
      console.log("📦 Received from stream:", event.data)
      const report = JSON.parse(event.data)
      setReports((prev) => [...prev, report])
    }

    return () => eventSource.close()
  }, [])

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>🚨 Theft Incident Monitor</h1>
      {reports.map((r, i) => (
        <div key={i} style={{
          border: '1px solid #ddd',
          borderRadius: '8px',
          padding: '12px',
          marginTop: '10px',
          background: '#f9f9f9'
        }}>
          <p><strong>Tag:</strong> {r.tag}</p>
          <p><strong>Product:</strong> {r.product}</p>
          <p><strong>Price:</strong> ${r.price.toFixed(2)}</p>
          <p style={{ fontStyle: 'italic', color: '#c00' }}>{r.message}</p>
        </div>
      ))}
    </div>
  )
}

const root = ReactDOM.createRoot(document.getElementById('root'))
root.render(<App />)