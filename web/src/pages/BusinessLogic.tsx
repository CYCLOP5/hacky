import React, { useState } from 'react'

const BusinessLogic: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'pricing' | 'risk' | 'examples'>('overview')

  // Sample data for charts
  const riskLevels = [
    { kp: '0-3', risk: 'Low', color: '#22c55e', percentage: 85, surcharge: '0%' },
    { kp: '3-6', risk: 'Moderate', color: '#f59e0b', percentage: 10, surcharge: '0%' },
    { kp: '6-7', risk: 'Elevated', color: '#f97316', percentage: 4, surcharge: '75%' },
    { kp: '7-8', risk: 'High', color: '#dc2626', percentage: 0.8, surcharge: '150%' },
    { kp: '8-9', risk: 'Critical', color: '#7c2d12', percentage: 0.2, surcharge: '400%' }
  ]

  const policyExamples = [
    {
      scenario: 'Normal Conditions',
      kp: 4.2,
      satelliteValue: 10,
      premium: 0.05,
      status: 'APPROVED',
      coverage: 100,
      reasoning: 'Low risk conditions, standard premium applies'
    },
    {
      scenario: 'Moderate Storm',
      kp: 6.8,
      satelliteValue: 10,
      premium: 0.875,
      status: 'APPROVED',
      coverage: 100,
      reasoning: '75% surcharge applied due to elevated space weather risk'
    },
    {
      scenario: 'Major Storm',
      kp: 8.1,
      satelliteValue: 10,
      premium: 0.87,
      status: 'APPROVED',
      coverage: 100,
      reasoning: '150% surcharge applied due to high space weather risk. Premium is within economical limits.'
    },
    {
      scenario: 'Extreme Event',
      kp: 9.2,
      satelliteValue: 10,
      premium: 1.5,
      status: 'MODIFIED',
      coverage: 71,
      reasoning: 'Premium capped at 15% of asset value. Coverage reduced to 71%.'
    }
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'APPROVED': return '#22c55e'
      case 'MODIFIED': return '#f59e0b'
      case 'REJECTED': return '#dc2626'
      default: return '#64748b'
    }
  }

  const TabButton = ({ tab, label, isActive, onClick }: { 
    tab: string
    label: string
    isActive: boolean
    onClick: () => void 
  }) => (
    <button
      onClick={onClick}
      style={{
        padding: '12px 24px',
        borderRadius: 8,
        border: 'none',
        fontSize: '1rem',
        fontWeight: 600,
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        background: isActive ? 'linear-gradient(135deg, #0ea5e9 0%, #22c55e 100%)' : '#1e293b',
        color: isActive ? 'white' : '#94a3b8'
      }}
    >
      {label}
    </button>
  )

  return (
    <div className="container">
      {/* Header */}
      <div style={{ marginBottom: 32 }}>
        <h1 style={{ 
          fontSize: '3rem', 
          fontWeight: 800, 
          background: 'linear-gradient(135deg, #0ea5e9 0%, #22c55e 100%)', 
          WebkitBackgroundClip: 'text', 
          WebkitTextFillColor: 'transparent',
          marginBottom: 16
        }}>
          Business Logic Engine
        </h1>
        <p style={{ fontSize: '1.125rem', color: '#94a3b8', maxWidth: '800px' }}>
          Understand how Project Borealis uses sophisticated AI-driven business logic to balance risk management 
          with commercial viability in satellite insurance pricing.
        </p>
      </div>

      {/* Tab Navigation */}
      <div style={{ 
        display: 'flex', 
        gap: 16, 
        marginBottom: 32,
        padding: 16,
        background: '#0f172a',
        borderRadius: 12,
        border: '1px solid #1e293b'
      }}>
        <TabButton 
          tab="overview" 
          label="Overview" 
          isActive={activeTab === 'overview'} 
          onClick={() => setActiveTab('overview')} 
        />
        <TabButton 
          tab="pricing" 
          label="Pricing Model" 
          isActive={activeTab === 'pricing'} 
          onClick={() => setActiveTab('pricing')} 
        />
        <TabButton 
          tab="risk" 
          label="Risk Assessment" 
          isActive={activeTab === 'risk'} 
          onClick={() => setActiveTab('risk')} 
        />
        <TabButton 
          tab="examples" 
          label="Real Examples" 
          isActive={activeTab === 'examples'} 
          onClick={() => setActiveTab('examples')} 
        />
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div className="card">
          <h2 style={{ marginTop: 0 }}>Intelligent Business Decision Framework</h2>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 24, marginBottom: 32 }}>
            <div style={{ 
              padding: 24, 
              background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)', 
              borderRadius: 12, 
              border: '1px solid #334155' 
            }}>
              <h3 style={{ color: '#22c55e', marginTop: 0 }}>Smart Premium Capping</h3>
              <p style={{ color: '#cbd5e1', lineHeight: 1.6 }}>
                Automatically caps premiums at 15% of asset value to maintain economic viability. 
                Prevents customer loss from unaffordable pricing while protecting company margins.
              </p>
            </div>

            <div style={{ 
              padding: 24, 
              background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)', 
              borderRadius: 12, 
              border: '1px solid #334155' 
            }}>
              <h3 style={{ color: '#0ea5e9', marginTop: 0 }}>Graduated Risk Response</h3>
              <p style={{ color: '#cbd5e1', lineHeight: 1.6 }}>
                Uses tiered surcharge system instead of binary accept/reject decisions. 
                Continues writing policies during severe space weather with appropriate risk pricing.
              </p>
            </div>

            <div style={{ 
              padding: 24, 
              background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)', 
              borderRadius: 12, 
              border: '1px solid #334155' 
            }}>
              <h3 style={{ color: '#f59e0b', marginTop: 0 }}>Alternative Solutions</h3>
              <p style={{ color: '#cbd5e1', lineHeight: 1.6 }}>
                Offers partial coverage, deductibles, and risk mitigation advice when full coverage 
                becomes uneconomical, maintaining customer relationships.
              </p>
            </div>
          </div>

          {/* Decision Flow Diagram */}
          <div style={{ 
            padding: 32, 
            background: '#0f172a', 
            borderRadius: 12, 
            border: '1px solid #1e293b',
            marginBottom: 24 
          }}>
            <h3 style={{ color: '#cbd5e1', textAlign: 'center', marginBottom: 32 }}>
              Business Logic Decision Flow
            </h3>
            
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 24 }}>
              {/* Input */}
              <div style={{ 
                padding: '16px 32px', 
                background: '#1e293b', 
                borderRadius: 8, 
                border: '1px solid #334155',
                textAlign: 'center' 
              }}>
                <div style={{ color: '#0ea5e9', fontWeight: 600 }}>Space Weather Forecast</div>
                <div style={{ color: '#94a3b8', fontSize: '0.875rem' }}>Kp Index + Asset Details</div>
              </div>

              {/* Arrow */}
              <div style={{ color: '#64748b' }}>V</div>

              {/* Risk Assessment */}
              <div style={{ 
                padding: '16px 32px', 
                background: '#1e293b', 
                borderRadius: 8, 
                border: '1px solid #334155',
                textAlign: 'center' 
              }}>
                <div style={{ color: '#22c55e', fontWeight: 600 }}>AI Risk Assessment</div>
                <div style={{ color: '#94a3b8', fontSize: '0.875rem' }}>Incident Probability + Portfolio Analysis</div>
              </div>

              {/* Arrow */}
              <div style={{ color: '#64748b' }}>V</div>

              {/* Decision Logic */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16, width: '100%' }}>
                <div style={{ 
                  padding: 16, 
                  background: '#22c55e20', 
                  border: '1px solid #22c55e40', 
                  borderRadius: 8,
                  textAlign: 'center' 
                }}>
                  <div style={{ color: '#22c55e', fontWeight: 600 }}>Premium ≤ 15%</div>
                  <div style={{ color: '#94a3b8', fontSize: '0.875rem' }}>Approve Full Coverage</div>
                </div>

                <div style={{ 
                  padding: 16, 
                  background: '#f59e0b20', 
                  border: '1px solid #f59e0b40', 
                  borderRadius: 8,
                  textAlign: 'center' 
                }}>
                  <div style={{ color: '#f59e0b', fontWeight: 600 }}>Premium 15-50%</div>
                  <div style={{ color: '#94a3b8', fontSize: '0.875rem' }}>Modify Coverage</div>
                </div>

                <div style={{ 
                  padding: 16, 
                  background: '#dc262620', 
                  border: '1px solid #dc262640', 
                  borderRadius: 8,
                  textAlign: 'center' 
                }}>
                  <div style={{ color: '#dc2626', fontWeight: 600 }}>Premium {'>'}  50%</div>
                  <div style={{ color: '#94a3b8', fontSize: '0.875rem' }}>Reject + Alternatives</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'pricing' && (
        <div className="card">
          <h2 style={{ marginTop: 0 }}>Adaptive Pricing Model</h2>
          
          {/* Surcharge Chart */}
          <div style={{ 
            padding: 32, 
            background: '#0f172a', 
            borderRadius: 12, 
            border: '1px solid #1e293b',
            marginBottom: 24 
          }}>
            <h3 style={{ color: '#cbd5e1', textAlign: 'center', marginBottom: 24 }}>
              Risk-Based Surcharge Structure
            </h3>
            
            <div style={{ display: 'grid', gap: 16 }}>
              {riskLevels.map((level, index) => (
                <div key={index} style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                  <div style={{ 
                    width: 80, 
                    fontSize: '0.875rem', 
                    fontWeight: 600, 
                    color: level.color 
                  }}>
                    Kp {level.kp}
                  </div>
                  
                  <div style={{ 
                    flex: 1, 
                    height: 24, 
                    background: '#1e293b', 
                    borderRadius: 4, 
                    overflow: 'hidden',
                    position: 'relative'
                  }}>
                    <div style={{ 
                      width: `${Math.min(level.percentage * 10, 100)}%`, 
                      height: '100%', 
                      background: level.color,
                      transition: 'width 0.5s ease'
                    }} />
                    <div style={{ 
                      position: 'absolute', 
                      left: 8, 
                      top: '50%', 
                      transform: 'translateY(-50%)', 
                      fontSize: '0.75rem', 
                      fontWeight: 600, 
                      color: 'white'
                    }}>
                      {level.percentage}% Frequency
                    </div>
                  </div>
                  
                  <div style={{ 
                    width: 120, 
                    textAlign: 'right', 
                    fontSize: '0.875rem', 
                    fontWeight: 600, 
                    color: level.color 
                  }}>
                    {level.surcharge} Surcharge
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Pricing Formula */}
          <div style={{ 
            padding: 24, 
            background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)', 
            borderRadius: 12, 
            border: '1px solid #334155',
            marginBottom: 24 
          }}>
            <h3 style={{ color: '#22c55e', marginTop: 0 }}>Base Pricing Formula</h3>
            <div style={{ 
              fontFamily: 'monospace', 
              background: '#0f172a', 
              padding: 16, 
              borderRadius: 8, 
              border: '1px solid #1e293b',
              marginBottom: 16
            }}>
              <div style={{ color: '#cbd5e1' }}>Expected Loss = Incident Probability × Asset Value</div>
              <div style={{ color: '#cbd5e1' }}>Base Premium = (Expected Loss × 1.20) + $10,000</div>
              <div style={{ color: '#f59e0b' }}>Final Premium = Base Premium × Surcharge Multiplier</div>
            </div>
            <p style={{ color: '#94a3b8', fontSize: '0.875rem', margin: 0 }}>
              The 20% markup covers operational costs and profit margin. The $10,000 base covers administrative overhead.
            </p>
          </div>

          {/* Business Constraints */}
          <div style={{ 
            padding: 24, 
            background: 'linear-gradient(135deg, #dc262620 0%, #f9731610 100%)', 
            borderRadius: 12, 
            border: '1px solid #dc262640' 
          }}>
            <h3 style={{ color: '#dc2626', marginTop: 0 }}>Economic Viability Constraints</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 16 }}>
              <div>
                <div style={{ color: '#fca5a5', fontWeight: 600, marginBottom: 4 }}>15% Asset Value Cap</div>
                <div style={{ color: '#cbd5e1', fontSize: '0.875rem' }}>
                  Maximum economical premium - above this, offer modified coverage
                </div>
              </div>
              <div>
                <div style={{ color: '#fca5a5', fontWeight: 600, marginBottom: 4 }}>50% Asset Value Threshold</div>
                <div style={{ color: '#cbd5e1', fontSize: '0.875rem' }}>
                  Automatic rejection - recommend self-insurance or alternatives
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'risk' && (
        <div className="card">
          <h2 style={{ marginTop: 0 }}>Multi-Agent Risk Assessment</h2>
          
          {/* Agent Workflow */}
          <div style={{ 
            padding: 32, 
            background: '#0f172a', 
            borderRadius: 12, 
            border: '1px solid #1e293b',
            marginBottom: 24 
          }}>
            <h3 style={{ color: '#cbd5e1', textAlign: 'center', marginBottom: 32 }}>
              AI Agent Collaboration Pipeline
            </h3>
            
            <div style={{ display: 'grid', gap: 24 }}>
              {[
                {
                  step: 1,
                  agent: 'Data Analyst',
                  color: '#0ea5e9',
                  task: 'Fetches NOAA space weather data and real-time alerts',
                  output: 'Worst-case Kp forecast + contextual information'
                },
                {
                  step: 2,
                  agent: 'Risk Analyst', 
                  color: '#22c55e',
                  task: 'Calculates incident probability for specific satellite',
                  output: 'Risk category + probability assessment'
                },
                {
                  step: 3,
                  agent: 'Chief Risk Officer',
                  color: '#f59e0b',
                  task: 'Analyzes portfolio exposure and strategic implications',
                  output: 'Business recommendation + portfolio risk level'
                },
                {
                  step: 4,
                  agent: 'Pricing Specialist',
                  color: '#dc2626',
                  task: 'Synthesizes risk data into commercial premium',
                  output: 'Final premium + business viability assessment'
                }
              ].map((agent, index) => (
                <div key={index} style={{ display: 'flex', alignItems: 'center', gap: 24 }}>
                  <div style={{ 
                    width: 48, 
                    height: 48, 
                    borderRadius: '50%', 
                    background: agent.color,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '1.25rem',
                    fontWeight: 700,
                    color: 'white'
                  }}>
                    {agent.step}
                  </div>
                  
                  <div style={{ flex: 1 }}>
                    <div style={{ color: agent.color, fontWeight: 600, marginBottom: 4 }}>
                      {agent.agent}
                    </div>
                    <div style={{ color: '#cbd5e1', marginBottom: 4 }}>
                      {agent.task}
                    </div>
                    <div style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
                      Output: {agent.output}
                    </div>
                  </div>
                  
                  {index < 3 && (
                    <div style={{ color: '#64748b', fontSize: '1.5rem' }}>{'>'}</div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Risk Factors */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 24 }}>
            <div style={{ 
              padding: 24, 
              background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)', 
              borderRadius: 12, 
              border: '1px solid #334155' 
            }}>
              <h3 style={{ color: '#0ea5e9', marginTop: 0 }}>Space Weather Factors</h3>
              <ul style={{ color: '#cbd5e1', paddingLeft: 20 }}>
                <li>Kp index intensity and duration</li>
                <li>Solar wind velocity and density</li>
                <li>Interplanetary magnetic field orientation</li>
                <li>Historical event correlation patterns</li>
              </ul>
            </div>

            <div style={{ 
              padding: 24, 
              background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)', 
              borderRadius: 12, 
              border: '1px solid #334155' 
            }}>
              <h3 style={{ color: '#22c55e', marginTop: 0 }}>Satellite Characteristics</h3>
              <ul style={{ color: '#cbd5e1', paddingLeft: 20 }}>
                <li>Radiation shielding level</li>
                <li>Mission duration and degradation</li>
                <li>Orbital position and exposure</li>
                <li>Component vulnerability assessment</li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'examples' && (
        <div className="card">
          <h2 style={{ marginTop: 0 }}>Real-World Scenario Examples</h2>
          
          <div style={{ display: 'grid', gap: 24 }}>
            {policyExamples.map((example, index) => (
              <div key={index} style={{ 
                padding: 24, 
                background: '#0f172a', 
                borderRadius: 12, 
                border: '1px solid #1e293b' 
              }}>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 20, alignItems: 'center' }}>
                  <div>
                    <h4 style={{ margin: '0 0 8px 0', color: '#cbd5e1' }}>{example.scenario}</h4>
                    <div style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
                      Kp {example.kp} • ${example.satelliteValue}M Satellite
                    </div>
                  </div>
                  
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ 
                      color: getStatusColor(example.status), 
                      fontWeight: 600,
                      marginBottom: 4 
                    }}>
                      {example.status}
                    </div>
                    <div style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
                      {example.coverage}% Coverage
                    </div>
                  </div>
                  
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ 
                      fontSize: '1.5rem', 
                      fontWeight: 700, 
                      color: example.status === 'REJECTED' ? '#dc2626' : '#22c55e',
                      marginBottom: 4 
                    }}>
                      {example.status === 'REJECTED' ? 'N/A' : `$${example.premium}M`}
                    </div>
                    <div style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
                      {example.status !== 'REJECTED' && `${(example.premium / example.satelliteValue * 100).toFixed(1)}% of value`}
                    </div>
                  </div>
                </div>
                
                <div style={{ 
                  marginTop: 16, 
                  padding: 16, 
                  background: '#1e293b', 
                  borderRadius: 8,
                  border: '1px solid #334155' 
                }}>
                  <div style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
                    <strong>Business Logic:</strong> {example.reasoning}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Comparison Chart */}
          <div style={{ 
            marginTop: 32,
            padding: 32, 
            background: '#0f172a', 
            borderRadius: 12, 
            border: '1px solid #1e293b' 
          }}>
            <h3 style={{ color: '#cbd5e1', textAlign: 'center', marginBottom: 24 }}>
              Premium vs Risk Level Comparison
            </h3>
            
            <div style={{ display: 'grid', gap: 16 }}>
              {policyExamples.filter(ex => ex.status !== 'REJECTED').map((example, index) => (
                <div key={index} style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                  <div style={{ 
                    width: 120, 
                    fontSize: '0.875rem', 
                    fontWeight: 600, 
                    color: getStatusColor(example.status) 
                  }}>
                    {example.scenario}
                  </div>
                  
                  <div style={{ 
                    flex: 1, 
                    height: 32, 
                    background: '#1e293b', 
                    borderRadius: 8, 
                    overflow: 'hidden',
                    position: 'relative'
                  }}>
                    <div style={{ 
                      width: `${(example.premium / example.satelliteValue) * 100 * 6.67}%`, 
                      height: '100%', 
                      background: getStatusColor(example.status),
                      transition: 'width 0.5s ease'
                    }} />
                    <div style={{ 
                      position: 'absolute', 
                      left: 12, 
                      top: '50%', 
                      transform: 'translateY(-50%)', 
                      fontSize: '0.875rem', 
                      fontWeight: 600, 
                      color: 'white'
                    }}>
                      ${example.premium}M ({(example.premium / example.satelliteValue * 100).toFixed(1)}%)
                    </div>
                  </div>
                  
                  <div style={{ 
                    width: 80, 
                    textAlign: 'right', 
                    fontSize: '0.875rem', 
                    color: '#94a3b8' 
                  }}>
                    Kp {example.kp}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default BusinessLogic