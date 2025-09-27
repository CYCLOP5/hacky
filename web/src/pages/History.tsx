import React from 'react'
import { DailyKpBars } from '../components/DailyKpBars'
import { getDailyGeomag } from '../services/api'

// Risk level assessment for historical data
const getRiskPeriodAssessment = (maxKp: number, stormDays: number, totalDays: number) => {
  const stormPercentage = totalDays > 0 ? (stormDays / totalDays) * 100 : 0
  
  if (maxKp >= 8) return { 
    level: 'CRITICAL', 
    color: '#dc2626', 
    description: 'Severe geomagnetic storms recorded - high impact on satellite operations' 
  }
  if (maxKp >= 7) return { 
    level: 'HIGH', 
    color: '#f97316', 
    description: 'Strong geomagnetic activity - increased operational risks observed' 
  }
  if (maxKp >= 6 || stormPercentage > 15) return { 
    level: 'MODERATE', 
    color: '#fbbf24', 
    description: 'Moderate geomagnetic activity - some operational impacts possible' 
  }
  if (maxKp >= 5 || stormPercentage > 5) return { 
    level: 'LOW', 
    color: '#10b981', 
    description: 'Minor geomagnetic activity - minimal operational impacts' 
  }
  return { 
    level: 'MINIMAL', 
    color: '#22c55e', 
    description: 'Quiet geomagnetic conditions - optimal for satellite operations' 
  }
}

// Calculate trend direction
const getTrend = (days: any[]) => {
  if (days.length < 14) return { direction: 'stable', change: 0 }
  
  const recent = days.slice(-7).filter(d => d.kp_avg !== null)
  const previous = days.slice(-14, -7).filter(d => d.kp_avg !== null)
  
  if (recent.length === 0 || previous.length === 0) return { direction: 'stable', change: 0 }
  
  const recentAvg = recent.reduce((sum, d) => sum + d.kp_avg, 0) / recent.length
  const previousAvg = previous.reduce((sum, d) => sum + d.kp_avg, 0) / previous.length
  
  const change = ((recentAvg - previousAvg) / previousAvg) * 100
  
  if (Math.abs(change) < 5) return { direction: 'stable', change }
  return { direction: change > 0 ? 'increasing' : 'decreasing', change }
}

export default function HistoryPage(){
  const [days, setDays] = React.useState<any[]>([])
  const [loading, setLoading] = React.useState(true)
  
  React.useEffect(()=>{
    getDailyGeomag(30).then(d=> {
      setDays(d.days)
      setLoading(false)
    }).catch(()=>{
      setLoading(false)
    })
  },[])

  // Enhanced statistics with business intelligence
  const analytics = React.useMemo(() => {
    if (!days.length) return { 
      maxKp: 0, avgKp: 0, stormDays: 0, totalDays: 0, 
      validDays: [], riskAssessment: null, trend: null,
      operationalImpact: 0, highRiskDays: 0, volatility: 0
    }
    
    // Filter and validate Kp values
    const validDays = days.filter(d => d.kp_max !== null && d.kp_avg !== null)
      .map(d => ({
        ...d,
        kp_max: Math.min(d.kp_max, 9),
        kp_avg: Math.min(d.kp_avg, 9)
      }))
    
    if (validDays.length === 0) return { 
      maxKp: 0, avgKp: 0, stormDays: 0, totalDays: 0,
      validDays: [], riskAssessment: null, trend: null,
      operationalImpact: 0, highRiskDays: 0, volatility: 0
    }
    
    const maxKp = Math.max(...validDays.map(d => d.kp_max))
    const avgKp = validDays.reduce((sum, d) => sum + d.kp_avg, 0) / validDays.length
    const stormDays = validDays.filter(d => d.kp_max >= 5).length
    const highRiskDays = validDays.filter(d => d.kp_max >= 6).length
    
    // Calculate operational impact score (0-100)
    const operationalImpact = Math.min(100, (stormDays / validDays.length) * 100 + (maxKp - 3) * 10)
    
    // Calculate volatility (standard deviation)
    const variance = validDays.reduce((sum, d) => sum + Math.pow(d.kp_max - avgKp, 2), 0) / validDays.length
    const volatility = Math.sqrt(variance)
    
    const riskAssessment = getRiskPeriodAssessment(maxKp, stormDays, validDays.length)
    const trend = getTrend(validDays)
    
    return {
      maxKp, avgKp, stormDays, totalDays: validDays.length, validDays,
      riskAssessment, trend, operationalImpact, highRiskDays, volatility
    }
  }, [days])

  return (
    <div className="container">
      {/* Header with Risk Assessment */}
      <div className="card" style={{ marginBottom: 32 }}>
        <h2 style={{ 
          marginTop: 0, 
          background: 'linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%)', 
          WebkitBackgroundClip: 'text', 
          WebkitTextFillColor: 'transparent', 
          backgroundClip: 'text' 
        }}>
          30-Day Geomagnetic Activity Analysis
        </h2>
        <p style={{ color: '#94a3b8', marginBottom: 24 }}>
          Historical space weather patterns and operational risk assessment for satellite insurance
        </p>
        
        {/* Primary Risk Assessment */}
        {!loading && analytics.riskAssessment && (
          <div style={{
            background: `linear-gradient(135deg, ${analytics.riskAssessment.color}20, ${analytics.riskAssessment.color}10)`,
            border: `1px solid ${analytics.riskAssessment.color}40`,
            borderRadius: 12,
            padding: 20,
            marginBottom: 24
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 12 }}>
              <div style={{
                background: analytics.riskAssessment.color,
                color: 'white',
                padding: '6px 16px',
                borderRadius: 8,
                fontSize: '0.875rem',
                fontWeight: 700
              }}>
                {analytics.riskAssessment.level} RISK PERIOD
              </div>
              <span style={{ fontSize: '1.25rem', fontWeight: 600, color: analytics.riskAssessment.color }}>
                Peak Kp {analytics.maxKp.toFixed(1)}
              </span>
            </div>
            <p style={{ margin: 0, color: '#cbd5e1', lineHeight: 1.6 }}>
              {analytics.riskAssessment.description}
            </p>
          </div>
        )}

        {/* Key Metrics Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16 }}>
          <div style={{ background: '#1e293b', padding: 16, borderRadius: 8, border: '1px solid #334155' }}>
            <h4 style={{ margin: '0 0 8px 0', color: '#94a3b8' }}>Activity Trend</h4>
            <div style={{ 
              fontSize: '1.25rem', 
              fontWeight: 600, 
              color: analytics.trend?.direction === 'increasing' ? '#f97316' : 
                     analytics.trend?.direction === 'decreasing' ? '#22c55e' : '#0ea5e9'
            }}>
              {loading ? '...' : 
               analytics.trend?.direction === 'increasing' ? 'Increasing' :
               analytics.trend?.direction === 'decreasing' ? 'Decreasing' : 'Stable'}
            </div>
            <div style={{ color: '#64748b', fontSize: '0.875rem' }}>
              {!loading && analytics.trend?.change !== undefined && 
                `${Math.abs(analytics.trend.change).toFixed(1)}% vs previous week`}
            </div>
          </div>

          <div style={{ background: '#1e293b', padding: 16, borderRadius: 8, border: '1px solid #334155' }}>
            <h4 style={{ margin: '0 0 8px 0', color: '#94a3b8' }}>Storm Days</h4>
            <div style={{ fontSize: '1.25rem', fontWeight: 600, color: '#cbd5e1' }}>
              {loading ? '...' : `${analytics.stormDays} of ${analytics.totalDays}`}
            </div>
            <div style={{ color: '#64748b', fontSize: '0.875rem' }}>
              {!loading && `${((analytics.stormDays / analytics.totalDays) * 100).toFixed(1)}% storm activity`}
            </div>
          </div>

          <div style={{ background: '#1e293b', padding: 16, borderRadius: 8, border: '1px solid #334155' }}>
            <h4 style={{ margin: '0 0 8px 0', color: '#94a3b8' }}>Operational Impact</h4>
            <div style={{ fontSize: '1.25rem', fontWeight: 600, color: '#cbd5e1' }}>
              {loading ? '...' : `${Math.round(analytics.operationalImpact)}/100`}
            </div>
            <div style={{ color: '#64748b', fontSize: '0.875rem' }}>Risk score based on activity</div>
          </div>

          <div style={{ background: '#1e293b', padding: 16, borderRadius: 8, border: '1px solid #334155' }}>
            <h4 style={{ margin: '0 0 8px 0', color: '#94a3b8' }}>Peak Activity</h4>
            <div style={{ fontSize: '1.25rem', fontWeight: 600, color: '#cbd5e1' }}>
              {loading ? '...' : `Kp ${analytics.maxKp.toFixed(1)}`}
            </div>
            <div style={{ color: '#64748b', fontSize: '0.875rem' }}>Maximum observed index</div>
          </div>
        </div>
      </div>

      {/* Main Chart - Full Width */}
      <div className="card" style={{ marginBottom: 24 }}>
        <DailyKpBars days={days} />
      </div>

      {/* Business Intelligence - Separate Section */}
      <div className="card" style={{ marginBottom: 24 }}>
        <h3 style={{ marginTop: 0 }}>Business Intelligence Summary</h3>
          
          {/* Insurance Risk Factors */}
          <div style={{ marginBottom: 24 }}>
            <h4 style={{ color: '#0ea5e9', marginBottom: 12 }}>Insurance Risk Factors</h4>
            <div style={{ display: 'grid', gap: 12 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 0' }}>
                <span style={{ color: '#cbd5e1' }}>High Risk Days (Kp ≥ 6)</span>
                <span style={{ 
                  color: analytics.highRiskDays > 3 ? '#dc2626' : analytics.highRiskDays > 1 ? '#f59e0b' : '#10b981',
                  fontWeight: 600 
                }}>
                  {loading ? '...' : analytics.highRiskDays}
                </span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 0' }}>
                <span style={{ color: '#cbd5e1' }}>Activity Volatility</span>
                <span style={{ 
                  color: analytics.volatility > 1.5 ? '#dc2626' : analytics.volatility > 1.0 ? '#f59e0b' : '#10b981',
                  fontWeight: 600 
                }}>
                  {loading ? '...' : analytics.volatility.toFixed(2)}
                </span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 0' }}>
                <span style={{ color: '#cbd5e1' }}>Average Daily Kp</span>
                <span style={{ color: '#cbd5e1', fontWeight: 600 }}>
                  {loading ? '...' : analytics.avgKp.toFixed(2)}
                </span>
              </div>
            </div>
          </div>

          {/* Storm Classification Guide */}
          <div style={{ marginBottom: 20 }}>
            <h4 style={{ color: '#0ea5e9', marginBottom: 12 }}>Storm Impact Classifications</h4>
            <div style={{ display: 'grid', gap: 8 }}>
              {[
                { range: 'Kp 8-9', level: 'G4-G5 Severe/Extreme', color: '#dc2626', impact: 'Critical satellite disruptions, widespread outages' },
                { range: 'Kp 7', level: 'G3 Strong', color: '#f97316', impact: 'Significant operational impacts, increased failure rates' },
                { range: 'Kp 6', level: 'G2 Moderate', color: '#fbbf24', impact: 'Moderate disruptions, degraded performance' },
                { range: 'Kp 5', level: 'G1 Minor', color: '#10b981', impact: 'Minor impacts, isolated issues possible' },
                { range: 'Kp 0-4', level: 'G0 Quiet', color: '#22c55e', impact: 'Normal operations, minimal risk' }
              ].map((item, index) => (
                <div key={index} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '6px 0' }}>
                  <div style={{
                    width: 12,
                    height: 12,
                    borderRadius: '50%',
                    background: item.color
                  }} />
                  <div style={{ display: 'flex', flex: 1, justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ color: item.color, fontWeight: 500, minWidth: 60 }}>{item.range}</span>
                    <span style={{ color: '#cbd5e1', fontWeight: 500, minWidth: 120 }}>{item.level}</span>
                    <span style={{ color: '#94a3b8', fontSize: '0.875rem', textAlign: 'right', flex: 1 }}>
                      {item.impact}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Data Source Info */}
        {/* Data Source Info */}
        <div style={{ 
          background: '#0f172a', 
          padding: 16, 
          borderRadius: 8, 
          border: '1px solid #334155',
          marginTop: 20 
        }}>
          <h4 style={{ margin: '0 0 8px 0', color: '#94a3b8' }}>Data Source</h4>
          <p style={{ margin: 0, color: '#64748b', fontSize: '0.875rem' }}>
            NOAA Space Weather Prediction Center • Updated daily • Historical geomagnetic indices
          </p>
        </div>
      </div>
    </div>
  )
}
