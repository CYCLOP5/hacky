import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider, Link, Outlet } from 'react-router-dom'
import './styles.css'
import HomePage from './pages/Home'
import WorkflowPage from './pages/Workflow'
import ForecastPage from './pages/Forecast'
import HistoryPage from './pages/History'
import HistoricalEventsPage from './pages/HistoricalEvents'
import BusinessLogicPage from './pages/BusinessLogic'
import { HeroScene } from './components/HeroScene'
import { NavBar } from './components/NavBar'

function Shell(){
  return (
    <div>
      <HeroScene />
      <header>
        <div className="brand">
          <div className="brand-icon">BOREALIS</div>
          <h1>Project Borealis</h1>
        </div>
        <NavBar />
      </header>
      <div style={{position:'relative', zIndex:1}}>
        <Outlet />
      </div>
    </div>
  )
}

const router = createBrowserRouter([
  {
    path: '/',
    element: <Shell />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'forecast', element: <ForecastPage /> },
      { path: 'history', element: <HistoryPage /> },
      { path: 'events', element: <HistoricalEventsPage /> },
      { path: 'business-logic', element: <BusinessLogicPage /> },
      { path: 'workflow', element: <WorkflowPage /> },
    ]
  }
])

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
