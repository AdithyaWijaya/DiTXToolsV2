import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Halo, Selamat Datang di Vite + React!</h1>
      <p>Contoh project sederhana dengan counter.</p>
      
      <button 
        onClick={() => setCount(count + 1)}
        style={{ padding: '10px 20px', fontSize: '16px', cursor: 'pointer' }}
      >
        Jumlah klik: {count}
      </button>
    </div>
  )
}

export default App