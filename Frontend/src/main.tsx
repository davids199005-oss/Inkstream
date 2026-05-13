import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import 'highlight.js/styles/github.css'
import Navigation from './routes/routes'
import './index.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Navigation />
  </StrictMode>,
)
