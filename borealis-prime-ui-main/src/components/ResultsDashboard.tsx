import LoadingDots from "./LoadingDots";

interface ResultsDashboardProps {
  isCalculating: boolean;
  results: {
    worstCaseKp: string;
    incidentProbability: string;
    expectedLoss: string;
    recommendedPremium: string;
  } | null;
}

const ResultsDashboard = ({ isCalculating, results }: ResultsDashboardProps) => {
  const resultFields = [
    { label: "Worst-Case Kp (24h)", value: results?.worstCaseKp },
    { label: "Incident Probability", value: results?.incidentProbability },
    { label: "Expected Loss (24h)", value: results?.expectedLoss },
    { label: "Recommended 24h Premium", value: results?.recommendedPremium },
  ];

  return (
    <div className="dashboard-card p-8 animate-fade-in">
      {!results && !isCalculating ? (
        <div className="text-center py-12">
          <p className="text-muted-foreground text-lg">
            Awaiting calculation... Please configure the asset in the sidebar and run the workflow.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {resultFields.map((field, index) => (
            <div key={index} className="space-y-2">
              <p className="text-sm font-medium text-muted-foreground uppercase tracking-wide">
                {field.label}
              </p>
              <div className="min-h-[2rem] flex items-center">
                {isCalculating ? (
                  <LoadingDots />
                ) : field.value ? (
                  <p className="text-xl font-semibold text-foreground">{field.value}</p>
                ) : (
                  <div className="w-16 h-6 bg-muted animate-pulse rounded"></div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ResultsDashboard;