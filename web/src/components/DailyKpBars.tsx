import React from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import type { DailyGeomagDay } from '../services/api'

// Function to get storm classification color based on Kp value
const getStormColor = (kp: number) => {
  if (kp >= 8) return '#ef4444' // G4-G5: Severe to Extreme (red)
  if (kp >= 7) return '#f97316' // G3: Strong Storm (orange)
  if (kp >= 6) return '#f59e0b' // G2: Moderate Storm (yellow)
  return '#10b981'              // G0-G1: Quiet to Minor (green)
}

export function DailyKpBars({ days }: { days: DailyGeomagDay[] }) {
  const data = days.map(d => {
    const maxKp = Math.min(d.kp_max ?? 0, 9)
    const avgKp = Math.min(d.kp_avg ?? 0, 9)
    return {
      date: d.date.slice(5),
      max: maxKp,
      avg: avgKp,
      maxColor: getStormColor(maxKp),
      avgColor: getStormColor(avgKp)
    }
  })
  return (
    <div className="card">
      <h3 style={{marginTop:0, background: 'linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text'}}>Daily Kp Indices (Last {days.length} days)</h3>
      <div style={{width:'100%', height:320, padding: '10px 0'}}>
        <ResponsiveContainer>
          <BarChart data={data} margin={{ top: 20, right: 30, left: 10, bottom: 20 }}>

            <CartesianGrid strokeDasharray="1 1" stroke="#334155" strokeWidth={0.5} />
            <XAxis 
              dataKey="date" 
              stroke="#94a3b8" 
              interval={Math.ceil(data.length/8)}
              fontSize={11}
              tickLine={false}
              axisLine={false}
            />
            <YAxis 
              domain={[0,9]} 
              stroke="#94a3b8"
              fontSize={11}
              tickLine={false}
              axisLine={false}
            />
            <Tooltip 
              formatter={(v: any, name: any) => {
                const kp = Number(v)
                const roundedKp = Math.round(kp * 10) / 10
                let classification = ''
                let color = '#10b981'
                if (kp >= 8) { classification = 'G4-G5 Severe'; color = '#ef4444' }
                else if (kp >= 7) { classification = 'G3 Strong'; color = '#f97316' }
                else if (kp >= 6) { classification = 'G2 Moderate'; color = '#f59e0b' }
                else if (kp >= 5) { classification = 'G1 Minor'; color = '#10b981' }
                else { classification = 'G0 Quiet'; color = '#10b981' }
                
                return [
                  <span style={{ color }}>
                    {roundedKp} ({classification})
                  </span>, 
                  name === 'max' ? 'Maximum Kp' : 'Average Kp'
                ]
              }}
              contentStyle={{
                background: 'rgba(26, 35, 50, 0.95)',
                border: '1px solid #475569',
                borderRadius: '12px',
                boxShadow: '0 10px 25px rgba(0, 0, 0, 0.5)',
                backdropFilter: 'blur(10px)',
                color: '#f8fafc'
              }}
              labelStyle={{ color: '#cbd5e1' }}
            />
            <Bar 
              dataKey="avg" 
              radius={[4,4,0,0]}
              strokeWidth={1}
            >
              {data.map((entry, index) => (
                <Cell key={`avg-${index}`} fill={entry.avgColor} stroke={entry.avgColor} />
              ))}
            </Bar>
            <Bar 
              dataKey="max" 
              radius={[4,4,0,0]}
              strokeWidth={1}
            >
              {data.map((entry, index) => (
                <Cell key={`max-${index}`} fill={entry.maxColor} stroke={entry.maxColor} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
