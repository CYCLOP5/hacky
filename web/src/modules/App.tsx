import React, { useMemo, useState } from 'react'
import { runWorkflow, getPortfolio, getThreeDayForecast, type RunInputs } from '../services/api'

// Step indicator component
const StepIndicator = ({ currentStep, steps }: { currentStep: number; steps: string[] }) => (
  <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 32 }}>
    {steps.map((step, index) => (
      <React.Fragment key={index}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <div style={{
            width: 32,
            height: 32,
            borderRadius: '50%',
            background: index <= currentStep ? '#0ea5e9' : '#334155',
            color: 'white',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: 600,
            transition: 'all 0.3s ease'
          }}>
            {index + 1}
          </div>
          <span style={{ 
            color: index <= currentStep ? '#0ea5e9' : '#64748b',
            fontWeight: index === currentStep ? 600 : 400,
            transition: 'all 0.3s ease'
          }}>
            {step}
          </span>
        </div>
        {index < steps.length - 1 && (
          <div style={{
            width: 40,
            height: 2,
            background: index < currentStep ? '#0ea5e9' : '#334155',
            transition: 'all 0.3s ease'
          }} />
        )}
      </React.Fragment>
    ))}
  </div>
)

// Shielding info component
const ShieldingInfo = ({ level }: { level: string }) => {
  const info = {
    'Standard': { icon: '', desc: 'Basic radiation hardening suitable for most missions', risk: 'Medium' },
    'Hardened': { icon: '', desc: 'Advanced protection for critical operations', risk: 'Low' },
    'Light/Legacy': { icon: '', desc: 'Minimal shielding, higher vulnerability', risk: 'High' }
  }[level]
  
  return info ? (
    <div style={{ 
      background: '#1e293b', 
      padding: 12, 
      borderRadius: 8, 
      marginTop: 8,
      border: '1px solid #334155'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
        <span style={{ fontWeight: 600, color: '#cbd5e1' }}>{level}</span>
        <span style={{ 
          background: info.risk === 'Low' ? '#10b98120' : info.risk === 'High' ? '#dc262620' : '#f59e0b20',
          color: info.risk === 'Low' ? '#10b981' : info.risk === 'High' ? '#dc2626' : '#f59e0b',
          padding: '2px 8px',
          borderRadius: 4,
          fontSize: '0.75rem',
          fontWeight: 600
        }}>
          {info.risk} Risk
        </span>
      </div>
      <p style={{ margin: 0, color: '#94a3b8', fontSize: '0.875rem' }}>{info.desc}</p>
    </div>
  ) : null
}

export function App({ embedded = false }: { embedded?: boolean }) {
  const [currentStep, setCurrentStep] = useState(0)
  const [assetValue, setAssetValue] = useState(300)
  const [shielding, setShielding] = useState<'Standard'|'Hardened'|'Light/Legacy'>('Standard')
  const [years, setYears] = useState(5)
  const [adj, setAdj] = useState(1.0)
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<any | null>(null)
  const [showTechnicalDetails, setShowTechnicalDetails] = useState(false)
  const [currentForecast, setCurrentForecast] = useState<any>(null)

  const steps = ['Configure Policy', 'Run Analysis', 'Review Results']

  React.useEffect(() => {
    getThreeDayForecast().then(setCurrentForecast).catch(()=>{})
  }, [])

  const inputs: RunInputs = useMemo(() => ({
    asset_value_millions: assetValue,
    shielding_level: shielding,
    years_in_orbit: years,
    adjustment_factor: adj
  }), [assetValue, shielding, years, adj])

  async function onRun() {
    setError(null)
    setLoading(true)
    setCurrentStep(1)
    
    try {
      const r = await runWorkflow(inputs)
      setResult(r)
      setCurrentStep(2)
    } catch (e: any) {
      setError(e?.message ?? 'Failed to run workflow')
      setCurrentStep(0)
    } finally {
      setLoading(false)
    }
  }

  const getPremiumStatus = () => {
    if (!result?.pricing_result?.final_premium_usd) return null
    const premium = result.pricing_result.final_premium_usd
    const assetValueUSD = assetValue * 1000000
    const percentage = (premium / assetValueUSD) * 100
    
    if (percentage > 5) return { status: 'High', color: '#dc2626', icon: '' }
    if (percentage > 2) return { status: 'Moderate', color: '#f59e0b', icon: '' }
    return { status: 'Competitive', color: '#10b981', icon: '' }
  }

  const getRiskLevel = () => {
    if (!result?.individual_risk?.incident_probability) return null
    const prob = result.individual_risk.incident_probability * 100
    
    if (prob > 1) return { level: 'High Risk', color: '#dc2626', icon: '' }
    if (prob > 0.5) return { level: 'Moderate Risk', color: '#f59e0b', icon: '' }
    return { level: 'Low Risk', color: '#10b981', icon: '' }
  }

  return (
    <>
      {!embedded && (
        <header>
          <div className="brand">
            <h1>Project Borealis: Cosmic Weather Insurance</h1>
          </div>
          <div>AI-Powered Risk Assessment</div>
        </header>
      )}

      <div className="container">
        <div className="card" style={{ marginBottom: 32 }}>
          <h2 style={{ 
            marginTop: 0, 
            background: 'linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%)', 
            WebkitBackgroundClip: 'text', 
            WebkitTextFillColor: 'transparent', 
            backgroundClip: 'text' 
          }}>
            Satellite Insurance Workflow
          </h2>
          <p style={{ color: '#94a3b8', marginBottom: 24 }}>
            Our AI agents analyze space weather data, assess satellite risks, and calculate precise insurance premiums.
          </p>
          
          <StepIndicator currentStep={currentStep} steps={steps} />
        </div>

        {/* Step 1: Policy Configuration */}
        <div className="card" style={{ marginBottom: 24 }}>
          <h3 style={{ display: 'flex', alignItems: 'center', gap: 12, marginTop: 0 }}>
            <span style={{ 
              background: currentStep >= 0 ? '#0ea5e9' : '#334155', 
              color: 'white', 
              width: 24, 
              height: 24, 
              borderRadius: '50%', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center', 
              fontSize: '0.875rem', 
              fontWeight: 600 
            }}>1</span>
            Policy Configuration
          </h3>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 24 }}>
            <div>
              <div className="input">
                <label>Satellite Value</label>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span style={{ color: '#94a3b8', fontSize: '1.25rem', fontWeight: 600 }}>$</span>
                  <input 
                    type="number" 
                    value={assetValue} 
                    min={1} 
                    step={1}
                    style={{ fontSize: '1.125rem', fontWeight: 600 }}
                    onChange={e=>setAssetValue(Number(e.target.value))} 
                  />
                  <span style={{ color: '#94a3b8', fontWeight: 500 }}>Million USD</span>
                </div>
                <small style={{ color: '#64748b' }}>Total replacement cost of the satellite</small>
              </div>

              <div className="input">
                <label>Radiation Shielding Level</label>
                <select value={shielding} onChange={e=>setShielding(e.target.value as any)} style={{ fontSize: '1rem' }}>
                  <option value="Standard">Standard Protection</option>
                  <option value="Hardened">Hardened Systems</option>
                  <option value="Light/Legacy">Light/Legacy</option>
                </select>
                <ShieldingInfo level={shielding} />
              </div>
            </div>

            <div>
              <div className="input">
                <label>Mission Duration</label>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <input 
                    type="number" 
                    value={years} 
                    min={0} 
                    max={20} 
                    step={1}
                    style={{ fontSize: '1.125rem', fontWeight: 600 }}
                    onChange={e=>setYears(Number(e.target.value))} 
                  />
                  <span style={{ color: '#94a3b8', fontWeight: 500 }}>Years in orbit</span>
                </div>
                <small style={{ color: '#64748b' }}>Longer missions face increased degradation risk</small>
              </div>

              <div className="input">
                <label style={{display:'flex', alignItems:'center', gap:8}}>
                  <input 
                    type="checkbox" 
                    checked={showAdvanced} 
                    onChange={e=>setShowAdvanced(e.target.checked)} 
                  />
                  Advanced Underwriting Controls
                </label>
                {showAdvanced && (
                  <div style={{ marginTop: 12, padding: 16, background: '#1e293b', borderRadius: 8, border: '1px solid #334155' }}>
                    <label>Risk Adjustment Factor</label>
                    <input 
                      type="range" 
                      value={adj} 
                      min={0.5} 
                      max={2} 
                      step={0.05}
                      onChange={e=>setAdj(Number(e.target.value))} 
                      style={{ width: '100%', marginBottom: 8 }}
                    />
                    <div style={{ display: 'flex', justifyContent: 'space-between', color: '#94a3b8', fontSize: '0.875rem' }}>
                      <span>Conservative (0.5x)</span>
                      <span style={{ fontWeight: 600, color: '#0ea5e9' }}>{adj}x</span>
                      <span>Aggressive (2.0x)</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          <div style={{ marginTop: 24, padding: 20, background: '#0f172a', borderRadius: 12, border: '1px solid #1e293b' }}>
            <h4 style={{ margin: '0 0 12px 0', color: '#0ea5e9' }}>Policy Summary</h4>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16 }}>
              <div>
                <span style={{ color: '#64748b', fontSize: '0.875rem' }}>Coverage Amount</span>
                <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#22c55e' }}>
                  ${assetValue.toLocaleString()}M
                </div>
              </div>
              <div>
                <span style={{ color: '#64748b', fontSize: '0.875rem' }}>Protection Level</span>
                <div style={{ fontSize: '1.125rem', fontWeight: 600, color: '#cbd5e1' }}>
                  {shielding}
                </div>
              </div>
              <div>
                <span style={{ color: '#64748b', fontSize: '0.875rem' }}>Mission Duration</span>
                <div style={{ fontSize: '1.125rem', fontWeight: 600, color: '#cbd5e1' }}>
                  {years} {years === 1 ? 'Year' : 'Years'}
                </div>
              </div>
            </div>
            
            <button 
              onClick={onRun} 
              disabled={loading} 
              style={{
                marginTop: 20,
                width: '100%',
                background: loading ? '#334155' : 'linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%)',
                color: 'white',
                border: 'none',
                padding: '16px 24px',
                borderRadius: 8,
                fontSize: '1.125rem',
                fontWeight: 600,
                cursor: loading ? 'not-allowed' : 'pointer',
                transition: 'all 0.3s ease',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 12
              }}
            >
              {loading ? (
                <>
                  <div style={{ 
                    width: 20, 
                    height: 20, 
                    border: '2px solid #64748b', 
                    borderTop: '2px solid white', 
                    borderRadius: '50%', 
                    animation: 'spin 1s linear infinite' 
                  }} />
                  AI Agents Working...
                </>
              ) : (
                <>
                  Run AI Analysis
                </>
              )}
            </button>
            
            {error && (
              <div style={{ 
                marginTop: 16, 
                padding: 12, 
                background: '#dc262620', 
                border: '1px solid #dc2626', 
                borderRadius: 8, 
                color: '#fca5a5' 
              }}>
                <strong>Error:</strong> {error}
              </div>
            )}
          </div>
        </div>

        {/* Step 3: Results */}
        {(loading || result) && (
          <div className="card">
            <h3 style={{ display: 'flex', alignItems: 'center', gap: 12, marginTop: 0 }}>
              <span style={{ 
                background: '#0ea5e9', 
                color: 'white', 
                width: 24, 
                height: 24, 
                borderRadius: '50%', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center', 
                fontSize: '0.875rem', 
                fontWeight: 600 
              }}>3</span>
              Insurance Quote Results
            </h3>

            {/* Premium Display */}
            <div style={{ 
              background: 'linear-gradient(135deg, #0ea5e920 0%, #3b82f620 100%)', 
              border: '1px solid #0ea5e940', 
              borderRadius: 16, 
              padding: 24, 
              marginBottom: 24, 
              textAlign: 'center' 
            }}>
              <div style={{ color: '#94a3b8', fontSize: '0.875rem', marginBottom: 8 }}>
                24-Hour Premium Quote
              </div>
              {/* Policy Status Indicator */}
              {result?.pricing_result?.policy_status && (
                <div style={{ 
                  marginBottom: 12,
                  padding: '8px 16px',
                  borderRadius: 8,
                  fontSize: '0.875rem',
                  fontWeight: 600,
                  display: 'inline-block',
                  background: result.pricing_result.policy_status === 'APPROVED' 
                    ? '#22c55e20' 
                    : result.pricing_result.policy_status === 'MODIFIED'
                    ? '#f59e0b20'
                    : '#dc262620',
                  color: result.pricing_result.policy_status === 'APPROVED'
                    ? '#22c55e'
                    : result.pricing_result.policy_status === 'MODIFIED' 
                    ? '#f59e0b'
                    : '#dc2626',
                  border: `1px solid ${result.pricing_result.policy_status === 'APPROVED'
                    ? '#22c55e40'
                    : result.pricing_result.policy_status === 'MODIFIED'
                    ? '#f59e0b40' 
                    : '#dc262640'}`
                }}>
                  {result.pricing_result.policy_status === 'APPROVED' && 'Policy Approved'}
                  {result.pricing_result.policy_status === 'MODIFIED' && 'Modified Coverage'}
                  {result.pricing_result.policy_status === 'REJECTED' && 'Policy Rejected'}
                </div>
              )}

              <div style={{ 
                fontSize: '2.5rem', 
                fontWeight: 800, 
                background: result?.pricing_result?.policy_status === 'REJECTED' 
                  ? 'linear-gradient(135deg, #dc2626 0%, #f59e0b 100%)'
                  : 'linear-gradient(135deg, #0ea5e9 0%, #22c55e 100%)', 
                WebkitBackgroundClip: 'text', 
                WebkitTextFillColor: 'transparent', 
                backgroundClip: 'text',
                marginBottom: 8
              }}>
                {loading && !result ? 'Processing...' :
                  result?.pricing_result?.policy_status === 'REJECTED'
                  ? 'N/A'
                  : result?.pricing_result?.final_premium_usd 
                  ? `$${result.pricing_result.final_premium_usd.toLocaleString()}`
                  : 'Processing...'}
              </div>

              <div style={{ color: '#64748b', fontSize: '0.875rem', display: 'grid', gap: 4 }}>
                {result?.pricing_result?.final_premium_usd && result?.pricing_result?.policy_status !== 'REJECTED' && (
                  <div>
                    {((result.pricing_result.final_premium_usd / (assetValue * 1000000)) * 100).toFixed(3)}% of asset value
                  </div>
                )}
                {result?.pricing_result?.coverage_percentage && result.pricing_result.coverage_percentage < 100 && (
                  <div style={{ color: '#f59e0b', fontWeight: 600 }}>
                    {result.pricing_result.coverage_percentage}% coverage
                  </div>
                )}
                 {result?.pricing_result?.rejection_reason && (
                  <div style={{ color: '#dc2626', fontWeight: 600 }}>
                    {result.pricing_result.rejection_reason}
                  </div>
                )}
              </div>
            </div>

            {/* Key Metrics */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 16, marginBottom: 24 }}>
              <div style={{ background: '#1e293b', padding: 20, borderRadius: 12, border: '1px solid #334155' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                  <span style={{ fontWeight: 600, color: getRiskLevel()?.color }}>
                    {getRiskLevel()?.level}
                  </span>
                </div>
                <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#cbd5e1' }}>
                  {result?.individual_risk?.incident_probability 
                    ? `${(result.individual_risk.incident_probability * 100).toFixed(3)}%`
                    : '...'
                  }
                </div>
                <div style={{ color: '#64748b', fontSize: '0.875rem' }}>24-hour incident probability</div>
              </div>

              <div style={{ background: '#1e293b', padding: 20, borderRadius: 12, border: '1px solid #334155' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                  <span style={{ fontWeight: 600, color: '#0ea5e9' }}>Space Weather</span>
                </div>
                <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#cbd5e1' }}>
                  Kp {currentForecast?.expected_max_kp ? currentForecast.expected_max_kp.toFixed(1) : (result?.worst_case_kp ? result.worst_case_kp.toFixed(1) : '...')}
                </div>
                <div style={{ color: '#64748b', fontSize: '0.875rem' }}>Expected maximum (3-day forecast)</div>
              </div>

              <div style={{ background: '#1e293b', padding: 20, borderRadius: 12, border: '1px solid #334155' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                  <span style={{ fontWeight: 600, color: '#22c55e' }}>Portfolio Status</span>
                </div>
                <div style={{ fontSize: '1.125rem', fontWeight: 600, color: '#cbd5e1', wordBreak: 'break-word' }}>
                  {loading && !result ? 'Analyzing...' : result?.portfolio_assessment?.strategic_recommendation || 'Analyzing...'}
                </div>
                <div style={{ color: '#64748b', fontSize: '0.875rem' }}>Risk officer recommendation</div>
              </div>
            </div>

            {/* Premium Breakdown */}
            {result?.pricing_result?.base_premium_usd && result?.pricing_result?.policy_status !== 'REJECTED' && (
              <div style={{ 
                marginBottom: 24,
                padding: 20, 
                background: '#0f172a', 
                borderRadius: 12, 
                border: '1px solid #1e293b' 
              }}>
                <h4 style={{ marginTop: 0, color: '#94a3b8' }}>Premium Breakdown</h4>
                <div style={{ display: 'grid', gap: 8, fontSize: '0.875rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: '#cbd5e1' }}>Base Premium:</span>
                    <span style={{ fontWeight: 600, color: '#cbd5e1' }}>
                      ${result.pricing_result.base_premium_usd.toLocaleString()}
                    </span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: '#cbd5e1' }}>Surcharge Applied:</span>
                    <span style={{ fontWeight: 600, color: result.pricing_result.surcharge_applied > 0 ? '#f59e0b' : '#22c55e' }}>
                      {result.pricing_result.surcharge_applied > 0 
                        ? `+$${result.pricing_result.surcharge_applied.toLocaleString()}`
                        : '$0'}
                    </span>
                  </div>
                  <div style={{ borderTop: '1px solid #334155', margin: '8px 0' }} />
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '1rem' }}>
                    <span style={{ color: '#0ea5e9' }}>Final Premium:</span>
                    <span style={{ fontWeight: 700, color: '#0ea5e9' }}>
                      ${result.pricing_result.final_premium_usd.toLocaleString()}
                    </span>
                  </div>
                </div>
              </div>
            )}

            {/* Alternative Options for Modified/Rejected Policies */}
            {result?.pricing_result?.alternative_options && (
              <div style={{ 
                marginBottom: 24,
                padding: 16, 
                background: '#1e293b', 
                borderRadius: 8, 
                border: '1px solid #334155' 
              }}>
                <h4 style={{ marginTop: 0, color: '#f59e0b' }}>Alternative Coverage Options</h4>
                {result.pricing_result.alternative_options.partial_coverage && (
                  <div style={{ 
                    background: '#1e293b', 
                    padding: 16, 
                    borderRadius: 8, 
                    border: '1px solid #334155',
                    marginBottom: 12
                  }}>
                    <h5 style={{ marginTop: 0, color: '#22c55e' }}>Partial Coverage Option</h5>
                    <div style={{ display: 'grid', gap: 8, fontSize: '0.875rem' }}>
                      <div style={{ color: '#cbd5e1' }}>
                        <strong>Coverage Amount:</strong> ${(result.pricing_result.alternative_options.partial_coverage.coverage_amount / 1000000).toFixed(1)}M
                      </div>
                      <div style={{ color: '#cbd5e1' }}>
                        <strong>Premium:</strong> ${result.pricing_result.alternative_options.partial_coverage.premium_usd.toLocaleString()}
                      </div>
                      <div style={{ color: '#cbd5e1' }}>
                        <strong>Deductible:</strong> ${(result.pricing_result.alternative_options.partial_coverage.deductible / 1000000).toFixed(1)}M
                      </div>
                    </div>
                  </div>
                )}
                {result.pricing_result.alternative_options.recommendation && (
                  <div style={{ 
                    padding: 12, 
                    background: '#dc262620', 
                    border: '1px solid #dc2626', 
                    borderRadius: 8, 
                    color: '#fca5a5',
                    fontSize: '0.875rem'
                  }}>
                    <strong>Recommendation:</strong> {result.pricing_result.alternative_options.recommendation}
                  </div>
                )}
              </div>
            )}

            {/* Deductible Information */}
            {result?.pricing_result?.deductible_usd && (
              <div style={{ 
                marginBottom: 24,
                padding: 16, 
                background: '#1e293b', 
                borderRadius: 8, 
                border: '1px solid #334155' 
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ color: '#94a3b8' }}>Policy Deductible:</span>
                  <span style={{ fontWeight: 600, color: '#cbd5e1' }}>
                    ${result.pricing_result.deductible_usd.toLocaleString()}
                  </span>
                </div>
              </div>
            )}

            {/* Risk Mitigation Advice */}
            {result?.pricing_result?.risk_mitigation && (
              <div style={{ 
                marginBottom: 24,
                padding: 20, 
                background: '#0f172a', 
                borderRadius: 12, 
                border: '1px solid #1e293b' 
              }}>
                <h4 style={{ marginTop: 0, color: '#0ea5e9' }}>Risk Mitigation Advice</h4>
                <p style={{ margin: 0, color: '#cbd5e1', lineHeight: 1.6 }}>
                  {result.pricing_result.risk_mitigation}
                </p>
              </div>
            )}

            {/* Technical Details Toggle */}
            <div style={{ marginTop: 24 }}>
              <button 
                onClick={() => setShowTechnicalDetails(!showTechnicalDetails)}
                style={{
                  background: 'none',
                  border: '1px solid #334155',
                  color: '#94a3b8',
                  padding: '8px 16px',
                  borderRadius: 6,
                  cursor: 'pointer',
                  fontSize: '0.875rem'
                }}
              >
                {showTechnicalDetails ? 'Hide' : 'Show'} Technical Analysis
              </button>
              
              {showTechnicalDetails && (
                <div style={{ 
                  marginTop: 16, 
                  padding: 20, 
                  background: '#0f172a', 
                  borderRadius: 12, 
                  border: '1px solid #1e293b',
                  maxHeight: 400,
                  overflow: 'auto'
                }}>
                  <h4 style={{ margin: '0 0 12px 0', color: '#94a3b8' }}>Detailed AI Analysis</h4>
                  <div style={{ color: '#64748b', fontSize: '0.875rem', marginBottom: 12 }}>
                    This is the raw JSON output from the AI workflow, providing a complete picture of the data used in the analysis.
                  </div>
                  <pre style={{ 
                    color: '#cbd5e1', 
                    fontSize: '0.75rem', 
                    lineHeight: 1.4,
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word'
                  }}>
                    {JSON.stringify(result, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </>
  )
}
