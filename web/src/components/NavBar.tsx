import React from 'react'
import { NavLink } from 'react-router-dom'

export function NavBar(){
  return (
    <nav className="nav">
      <NavLink to="/" className={({isActive})=> isActive? 'nav-link active' : 'nav-link'}>Home</NavLink>
      <NavLink to="/forecast" className={({isActive})=> isActive? 'nav-link active' : 'nav-link'}>3‑Day Forecast</NavLink>
      <NavLink to="/history" className={({isActive})=> isActive? 'nav-link active' : 'nav-link'}>Past 30 Days</NavLink>
      <NavLink to="/events" className={({isActive})=> isActive? 'nav-link active' : 'nav-link'}>Historical Events</NavLink>
      <NavLink to="/business-logic" className={({isActive})=> isActive? 'nav-link active' : 'nav-link'}>Business Logic</NavLink>
      <NavLink to="/workflow" className={({isActive})=> isActive? 'nav-link active' : 'nav-link'}>Agentic Workflow</NavLink>
    </nav>
  )
}
