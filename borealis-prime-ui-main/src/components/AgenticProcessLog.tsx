import { ScrollArea } from "@/components/ui/scroll-area";
import LoadingDots from "./LoadingDots";

interface AgenticProcessLogProps {
  isRunning: boolean;
  logs: string[];
}

const AgenticProcessLog = ({ isRunning, logs }: AgenticProcessLogProps) => {
  return (
    <div className="dashboard-card animate-fade-in">
      <div className="p-6 border-b border-border">
        <h3 className="text-lg font-semibold text-foreground">Agentic Process Log</h3>
      </div>
      
      <div className="p-6">
        {logs.length === 0 && !isRunning ? (
          <p className="text-muted-foreground">
            The thought process and tool execution of the AI agents will appear here once the workflow is run.
          </p>
        ) : (
          <ScrollArea className="h-64">
            <div className="space-y-3">
              {logs.map((log, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                  <p className="text-sm text-foreground">{log}</p>
                </div>
              ))}
              {isRunning && (
                <div className="flex items-center space-x-3">
                  <LoadingDots />
                  <p className="text-sm text-muted-foreground">Processing...</p>
                </div>
              )}
            </div>
          </ScrollArea>
        )}
      </div>
    </div>
  );
};

export default AgenticProcessLog;