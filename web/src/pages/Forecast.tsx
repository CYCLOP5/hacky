import React from 'react'
import { KpChart, type KpPoint } from '../components/KpChart'
import { getThreeDayForecast, getDailyGeomag, type DailyGeomagDay } from '../services/api'

// Kp Level interpretations for satellite operations
const getKpRiskLevel = (kp: number) => {
  if (kp >= 8) return { level: 'SEVERE', color: '#dc2626', description: 'Critical risk to satellite operations, widespread disruptions likely' }
  if (kp >= 7) return { level: 'STRONG', color: '#f97316', description: 'High risk to satellites, especially those in vulnerable orbits' }
  if (kp >= 5) return { level: 'MODERATE', color: '#fbbf24', description: 'Increased risk to satellite operations, minor disruptions possible' }
  if (kp >= 4) return { level: 'MINOR', color: '#10b981', description: 'Low risk to satellite operations, minimal impact expected' }
  return { level: 'QUIET', color: '#22c55e', description: 'Favorable conditions for satellite operations' }
}

export default function ForecastPage() {
  const [forecast, setForecast] = React.useState<any>(null)
  const [recentActivity, setRecentActivity] = React.useState<DailyGeomagDay[]>([])

  React.useEffect(() => {
    Promise.all([
      getThreeDayForecast().then(setForecast).catch(()=>{}),
      getDailyGeomag(14).then(data => setRecentActivity(data.days || [])).catch(()=>{})
    ])
  }, [])

  const flattened: KpPoint[] = React.useMemo(() => {
    if (!forecast?.breakdown || !forecast?.days) return []
    // Convert all 3 days of breakdown data
    const allPoints: KpPoint[] = []
    forecast.breakdown.forEach((period: any) => {
      period.values.forEach((kp: number, dayIndex: number) => {
        const day = forecast.days[dayIndex]
        const hour = period.period.slice(0, 2)
        allPoints.push({ t: `${day}T${hour}:00:00Z`, kp })
      })
    })
    return allPoints.sort((a, b) => new Date(a.t).getTime() - new Date(b.t).getTime())
  }, [forecast])

  // Recent activity summary
  const recentMax = React.useMemo(() => {
    if (!recentActivity.length) return null
    return Math.max(...recentActivity.map(d => d.kp_max || 0))
  }, [recentActivity])

  const recentAvg = React.useMemo(() => {
    if (!recentActivity.length) return null
    const validMaxes = recentActivity.map(d => d.kp_max).filter(k => k !== null) as number[]
    return validMaxes.length > 0 ? validMaxes.reduce((a, b) => a + b, 0) / validMaxes.length : null
  }, [recentActivity])

  const expectedMaxRisk = forecast?.expected_max_kp ? getKpRiskLevel(forecast.expected_max_kp) : null

  return (
    <div className="container">
      {/* Header with key insights */}
      <div className="card">
        <h2 style={{marginTop:0, background: 'linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text'}}>
          NOAA 3-Day Space Weather Forecast
        </h2>
        <p style={{color:'#aab0c6', marginBottom: 16}}>
          Issued: {forecast?.issued ? new Date(forecast.issued).toLocaleString() : '…'}
        </p>
        
        {/* Risk Summary */}
        {expectedMaxRisk && (
          <div style={{
            background: `linear-gradient(135deg, ${expectedMaxRisk.color}20, ${expectedMaxRisk.color}10)`,
            border: `1px solid ${expectedMaxRisk.color}40`,
            borderRadius: 12,
            padding: 16,
            marginBottom: 16
          }}>
            <div style={{display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8}}>
              <div style={{
                background: expectedMaxRisk.color,
                color: 'white',
                padding: '4px 12px',
                borderRadius: 6,
                fontSize: '0.875rem',
                fontWeight: 600
              }}>
                {expectedMaxRisk.level} RISK
              </div>
              <span style={{fontSize: '1.25rem', fontWeight: 600, color: expectedMaxRisk.color}}>
                Kp {forecast.expected_max_kp}
              </span>
            </div>
            <p style={{margin: 0, color: '#cbd5e1'}}>{expectedMaxRisk.description}</p>
          </div>
        )}

        {/* Recent Activity Context */}
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16}}>
          <div style={{background: '#1e293b', padding: 16, borderRadius: 8, border: '1px solid #334155'}}>
            <h4 style={{margin: '0 0 8px 0', color: '#94a3b8'}}>Recent 14-Day Max</h4>
            <div style={{fontSize: '1.5rem', fontWeight: 600, color: recentMax && recentMax >= 5 ? '#f97316' : '#10b981'}}>
              {recentMax ? `Kp ${recentMax.toFixed(1)}` : '…'}
            </div>
          </div>
          <div style={{background: '#1e293b', padding: 16, borderRadius: 8, border: '1px solid #334155'}}>
            <h4 style={{margin: '0 0 8px 0', color: '#94a3b8'}}>Recent Average</h4>
            <div style={{fontSize: '1.5rem', fontWeight: 600, color: '#0ea5e9'}}>
              {recentAvg ? `Kp ${recentAvg.toFixed(1)}` : '…'}
            </div>
          </div>
          <div style={{background: '#1e293b', padding: 16, borderRadius: 8, border: '1px solid #334155'}}>
            <h4 style={{margin: '0 0 8px 0', color: '#94a3b8'}}>Forecast Peak</h4>
            <div style={{fontSize: '1.5rem', fontWeight: 600, color: expectedMaxRisk?.color || '#cbd5e1'}}>
              {forecast?.expected_max_kp ? `Kp ${forecast.expected_max_kp}` : '…'}
            </div>
          </div>
        </div>
      </div>

      {/* Chart and Detailed Table */}
      <div className="grid" style={{marginTop:24}}>
        <KpChart data={flattened} />
        
        <div className="card">
          <h3 style={{marginTop:0}}>Detailed Forecast Breakdown</h3>
          
          {/* Enhanced table with risk coloring */}
          <table style={{width:'100%', borderCollapse:'collapse'}}>
            <thead>
              <tr>
                <th style={{textAlign:'left', padding:'8px 6px', borderBottom:'1px solid #1d2442', color: '#94a3b8'}}>UTC Period</th>
                {forecast?.days?.map((d:string)=>(
                  <th key={d} style={{textAlign:'right', padding:'8px 6px', borderBottom:'1px solid #1d2442', color: '#94a3b8'}}>{d}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {(forecast?.breakdown||[]).map((row:any)=> (
                <tr key={row.period}>
                  <td style={{padding:'6px', fontWeight: 500, color: '#cbd5e1'}}>{row.period}</td>
                  {(row.values||[]).map((v:number, i:number)=>{
                    const riskLevel = getKpRiskLevel(v)
                    return (
                      <td key={i} style={{
                        padding:'6px', 
                        textAlign:'right', 
                        color: riskLevel.color,
                        fontWeight: v >= 5 ? 600 : 400,
                        background: v >= 7 ? `${riskLevel.color}15` : 'transparent'
                      }}>
                        {v.toFixed(2)}
                      </td>
                    )
                  })}
                </tr>
              ))}
            </tbody>
          </table>
          
          {/* Enhanced rationale */}
          {forecast?.rationale && (
            <div style={{marginTop: 16, padding: 16, background: '#1e293b', borderRadius: 8, border: '1px solid #334155'}}>
              <h4 style={{margin: '0 0 8px 0', color: '#94a3b8'}}>NOAA Analysis</h4>
              <p style={{margin: 0, color: '#cbd5e1', lineHeight: 1.6}}>{forecast.rationale}</p>
            </div>
          )}
          
          {/* Risk interpretation guide */}
          <div style={{marginTop: 16, padding: 16, background: '#0f172a', borderRadius: 8, border: '1px solid #334155'}}>
            <h4 style={{margin: '0 0 12px 0', color: '#94a3b8'}}>Kp Index Risk Levels</h4>
            <div style={{display: 'grid', gap: 8}}>
              {[
                { range: '8-9', ...getKpRiskLevel(8) },
                { range: '7', ...getKpRiskLevel(7) },
                { range: '5-6', ...getKpRiskLevel(5) },
                { range: '4', ...getKpRiskLevel(4) },
                { range: '0-3', ...getKpRiskLevel(2) }
              ].map(level => (
                <div key={level.range} style={{display: 'flex', alignItems: 'center', gap: 12}}>
                  <div style={{
                    width: 12,
                    height: 12,
                    borderRadius: '50%',
                    background: level.color
                  }} />
                  <span style={{color: level.color, fontWeight: 500, minWidth: 40}}>Kp {level.range}</span>
                  <span style={{color: '#94a3b8', fontSize: '0.875rem'}}>{level.description}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
