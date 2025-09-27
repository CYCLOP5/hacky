import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function HomePage() {
  const navigate = useNavigate()
  const [scrollY, setScrollY] = useState(0)

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY)
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content" style={{ transform: `translateY(${scrollY * 0.3}px)` }}>
          <div className="hero-text">
            <h1 className="hero-title">
              Project <span className="gradient-text">Borealis</span>
            </h1>
            <p className="hero-subtitle">
              Next-Generation Space Weather Insurance Platform
            </p>
            <p className="hero-description">
              Revolutionizing space asset protection through advanced geomagnetic forecasting, 
              AI-powered risk assessment, and real-time orbital monitoring systems.
            </p>
            <div className="hero-buttons">
              <button className="primary-button" onClick={() => navigate('/workflow')}>
                Explore Dashboard
              </button>
              <button className="secondary-button" onClick={() => navigate('/forecast')}>
                View Forecasts
              </button>
            </div>
          </div>
        </div>
        
        {/* Scroll Indicator */}
        <div className="scroll-indicator">
          <div className="scroll-arrow"></div>
          <span>Scroll to discover</span>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="container">
          <h2 className="section-title">Advanced Space Weather Intelligence</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">MONITOR</div>
              <h3>Real-Time Monitoring</h3>
              <p>Continuous tracking of geomagnetic conditions with 3-day forecasting accuracy</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">SATELLITE</div>
              <h3>Satellite Tracking</h3>
              <p>Advanced orbital mechanics simulation for precise asset positioning</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">AI</div>
              <h3>AI Risk Assessment</h3>
              <p>Machine learning algorithms for predictive insurance modeling</p>
            </div>
          </div>
        </div>
      </section>

      {/* Technology Section */}
      <section className="tech-section">
        <div className="container">
          <div className="tech-content">
            <div className="tech-text">
              <h2>Cutting-Edge Technology Stack</h2>
              <p>
                Built with modern web technologies and powered by advanced space weather data sources, 
                Project Borealis delivers unprecedented accuracy in space weather forecasting.
              </p>
              <ul className="tech-list">
                <li>NOAA Space Weather Prediction Center Integration</li>
                <li>Real-time Kp Index Monitoring (0-9 Scale)</li>
                <li>G-Scale Geomagnetic Storm Classification</li>
                <li>Portfolio Risk Analysis & Premium Calculation</li>
              </ul>
            </div>
            <div className="tech-visual">
              <div className="data-visualization">
                <div className="data-point active">
                  <span className="label">Kp Index</span>
                  <span className="value">3.67</span>
                </div>
                <div className="data-point">
                  <span className="label">Storm Level</span>
                  <span className="value">G1</span>
                </div>
                <div className="data-point">
                  <span className="label">Risk Factor</span>
                  <span className="value">Low</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <div className="cta-content">
            <h2>Ready to Protect Your Space Assets?</h2>
            <p>Join the future of space weather insurance with Project Borealis</p>
            <button className="cta-button" onClick={() => navigate('/workflow')}>Get Started Today</button>
          </div>
        </div>
      </section>
    </div>
  )
}