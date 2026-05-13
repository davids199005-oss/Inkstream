import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import Navigation from './routes/routes'
import './index.css'


createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Navigation />
  </StrictMode>,
)
