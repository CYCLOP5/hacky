import React from 'react'

export function MetricCard({ title, value, subtitle }: { title: string; value: React.ReactNode; subtitle?: string }){
  return (
    <div className="metric">
      <h4>{title}</h4>
      <div className="metric-value">{value}</div>
      {subtitle && <div className="metric-sub">{subtitle}</div>}
    </div>
  )
}