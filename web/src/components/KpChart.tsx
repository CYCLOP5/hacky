import React from 'react'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  AreaChart, Area, ReferenceLine
} from 'recharts'

export type KpPoint = { t: string; kp: number }

export function KpChart({ data }: { data: KpPoint[] }) {
  // Format x labels to show day/hour
  const formatX = (iso: string) => {
    const d = new Date(iso)
    return `${d.getUTCMonth()+1}/${d.getUTCDate()} ${d.getUTCHours()}h`
  }

  return (
    <div className="card">
      <h3 style={{marginTop:0, background: 'linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text'}}>Kp Forecast (Next Few Days)</h3>
      <div style={{width:'100%', height:350, padding: '10px 0'}}>
        <ResponsiveContainer>
          <AreaChart data={data} margin={{ top: 20, right: 30, left: 10, bottom: 20 }}>
            <defs>
              <linearGradient id="kpFillModern" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#0ea5e9" stopOpacity={0.8}/>
                <stop offset="50%" stopColor="#3b82f6" stopOpacity={0.4}/>
                <stop offset="100%" stopColor="#06b6d4" stopOpacity={0.1}/>
              </linearGradient>
              <filter id="glow">
                <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                <feMerge> 
                  <feMergeNode in="coloredBlur"/>
                  <feMergeNode in="SourceGraphic"/> 
                </feMerge>
              </filter>
            </defs>
            <CartesianGrid strokeDasharray="1 1" stroke="#334155" strokeWidth={0.5} />
            <XAxis 
              dataKey="t" 
              tickFormatter={formatX} 
              stroke="#94a3b8" 
              interval={Math.ceil(data.length/8)}
              fontSize={11}
              tickLine={false}
              axisLine={false}
            />
            <YAxis 
              domain={[0, 9]} 
              stroke="#94a3b8" 
              allowDecimals={false}
              fontSize={11}
              tickLine={false}
              axisLine={false}
            />
            <Tooltip 
              labelFormatter={(v: any)=>`UTC ${formatX(String(v))}`} 
              formatter={(v: any)=>[String(v), 'Kp Index']}
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
            <ReferenceLine 
              y={5} 
              stroke="#fbbf24" 
              strokeDasharray="2 4" 
              strokeWidth={2}
              label={{ value: 'G1 Storm', position: 'insideTopRight', fill: '#fbbf24', fontSize: 11, fontWeight: 600 }} 
            />
            <ReferenceLine 
              y={7} 
              stroke="#f97316" 
              strokeDasharray="2 4" 
              strokeWidth={2}
              label={{ value: 'G3 Strong', position: 'insideTopRight', fill: '#f97316', fontSize: 11, fontWeight: 600 }} 
            />
            <ReferenceLine 
              y={8} 
              stroke="#dc2626" 
              strokeDasharray="2 4" 
              strokeWidth={2}
              label={{ value: 'G4 Severe', position: 'insideTopRight', fill: '#dc2626', fontSize: 11, fontWeight: 600 }} 
            />
            <Area 
              type="monotone" 
              dataKey="kp" 
              stroke="#0ea5e9" 
              strokeWidth={3}
              fillOpacity={1} 
              fill="url(#kpFillModern)"
              filter="url(#glow)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
