import { useState } from "react";
import PolicySidebar from "@/components/PolicySidebar";
import ResultsDashboard from "@/components/ResultsDashboard";
import AgenticProcessLog from "@/components/AgenticProcessLog";
import KpHistogramChart from "@/components/KpHistogramChart";
import AlarmsWidget from "@/components/AlarmsWidget";
import CosmicIcon from "@/components/CosmicIcon";

const ProfessionalDashboard = () => {
  const [isCalculating, setIsCalculating] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const [showResults, setShowResults] = useState(false);

  const handleRunWorkflow = async (configData: any) => {
    setIsCalculating(true);
    setLogs([]);
    setResults(null);
    setShowResults(true); // Switch to results view

    // Simulate AI workflow process
    const processSteps = [
      "Initializing space weather data collection...",
      "Analyzing current solar activity levels...",
      `Processing asset configuration: $${configData.assetValue}M value, ${configData.shieldingLevel} shielding`,
      "Calculating geomagnetic storm probabilities...",
      `Applying ${configData.yearsInOrbit}-year orbital degradation factors...`,
      `Adjusting risk parameters by factor ${configData.riskAdjustment}...`,
      "Running Monte Carlo simulations...",
      "Generating insurance premium recommendations...",
      "Finalizing risk assessment report...",
    ];

    for (let i = 0; i < processSteps.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 800));
      setLogs(prev => [...prev, processSteps[i]]);
    }

    // Simulate results calculation
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const mockResults = {
      worstCaseKp: "7.2",
      incidentProbability: "12.3%",
      expectedLoss: `$${(configData.assetValue * 0.023).toFixed(1)}M`,
      recommendedPremium: `$${(configData.assetValue * 0.0045).toFixed(2)}M`,
    };

    setResults(mockResults);
    setIsCalculating(false);
    setLogs(prev => [...prev, "Workflow completed successfully."]);
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="flex">
        {/* Sidebar */}
        <PolicySidebar onRunWorkflow={handleRunWorkflow} />
        
        {/* Main Content Area */}
        <div className="flex-1 min-h-screen">
          {/* Header */}
          <header className="border-b border-border bg-card/50 backdrop-blur-sm">
            <div className="px-8 py-6">
              <div className="flex items-center space-x-3 mb-2">
                <CosmicIcon />
                <h1 className="text-2xl font-bold text-foreground">
                  Project Borealis: Cosmic Weather Insurance
                </h1>
              </div>
              <p className="text-muted-foreground">
                User interface for pricing a 24-hour insurance policy for a Geostationary (GEO) Satellite.
              </p>
            </div>
          </header>

          {/* Main Dashboard */}
          <main className="p-8">
            {!showResults ? (
              /* Default State - Histogram and Alarms */
              <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
                <div className="xl:col-span-2">
                  <KpHistogramChart />
                </div>
                <div className="xl:col-span-1">
                  <AlarmsWidget />
                </div>
              </div>
            ) : (
              /* Results State - Dashboard and Process Log */
              <div className="space-y-8">
                {/* Results Dashboard */}
                <div>
                  <h2 className="text-xl font-semibold text-foreground mb-4">Results Dashboard</h2>
                  <ResultsDashboard isCalculating={isCalculating} results={results} />
                </div>

                {/* Agentic Process Log */}
                <div>
                  <AgenticProcessLog isRunning={isCalculating} logs={logs} />
                </div>
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
};

export default ProfessionalDashboard;