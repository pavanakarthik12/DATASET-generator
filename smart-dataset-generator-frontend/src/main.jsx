import React, { useEffect, useState } from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import Landing from './pages/Landing.jsx'
import './index.css'

const Root = () => {
  const getRoute = () => (window.location.hash.startsWith('#/app') ? 'app' : 'home')
  const [route, setRoute] = useState(getRoute())

  useEffect(() => {
    const onHashChange = () => setRoute(getRoute())
    window.addEventListener('hashchange', onHashChange)
    return () => window.removeEventListener('hashchange', onHashChange)
  }, [])

  // When route switches to app, ensure we scroll to the forms section
  useEffect(() => {
    if (route !== 'app') return
    const scrollToData = () => {
      const el = document.getElementById('data')
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
    // Try immediately and on next frame to handle mount timing
    scrollToData()
    const id = requestAnimationFrame(scrollToData)
    return () => cancelAnimationFrame(id)
  }, [route])

  return route === 'app' ? <App /> : <Landing />
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Root />
  </React.StrictMode>,
)
