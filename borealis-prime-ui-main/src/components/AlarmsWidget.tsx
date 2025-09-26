import { useState } from "react";
import { AlertTriangle, Clock, ChevronDown, ChevronUp } from "lucide-react";

interface Alarm {
  id: string;
  date: string;
  time: string;
  severity: 'low' | 'medium' | 'high';
  description: string;
  details: string;
}

const AlarmsWidget = () => {
  const [expandedAlarm, setExpandedAlarm] = useState<string | null>(null);

  const alarms: Alarm[] = [
    {
      id: '1',
      date: '2024-01-15',
      time: '14:23 UTC',
      severity: 'high',
      description: 'G3 Geomagnetic Storm',
      details: 'Strong geomagnetic storm conditions observed. Kp index reached 7.2. Satellite operations may be affected.'
    },
    {
      id: '2',
      date: '2024-01-14',
      time: '09:15 UTC',
      severity: 'medium',
      description: 'Solar Flare M-Class',
      details: 'M2.1 solar flare detected from region AR3529. Increased particle radiation expected.'
    },
    {
      id: '3',
      date: '2024-01-13',
      time: '22:47 UTC',
      severity: 'medium',
      description: 'CME Impact Expected',
      details: 'Coronal mass ejection impact forecast for next 24-48 hours. Monitor for geomagnetic activity.'
    },
    {
      id: '4',
      date: '2024-01-13',
      time: '16:32 UTC',
      severity: 'low',
      description: 'Radio Blackout R1',
      details: 'Minor radio blackout on sunlit side of Earth. HF radio communications briefly affected.'
    },
    {
      id: '5',
      date: '2024-01-12',
      time: '11:58 UTC',
      severity: 'low',
      description: 'Electron Flux Increase',
      details: 'Moderate increase in >2MeV electron flux at geosynchronous orbit. Normal operational impact.'
    }
  ];

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'low': return 'text-chart-low border-chart-low';
      case 'medium': return 'text-chart-medium border-chart-medium';
      case 'high': return 'text-chart-high border-chart-high';
      default: return 'text-muted-foreground border-border';
    }
  };

  const getSeverityBg = (severity: string) => {
    switch (severity) {
      case 'low': return 'bg-chart-low/10';
      case 'medium': return 'bg-chart-medium/10';
      case 'high': return 'bg-chart-high/10';
      default: return 'bg-muted/10';
    }
  };

  const toggleExpanded = (alarmId: string) => {
    setExpandedAlarm(expandedAlarm === alarmId ? null : alarmId);
  };

  return (
    <div className="dashboard-card p-4">
      <div className="flex items-center space-x-2 mb-4">
        <AlertTriangle className="h-5 w-5 text-warning" />
        <h3 className="text-lg font-semibold text-foreground">Space Weather Alarms</h3>
        <span className="text-xs text-muted-foreground">(Last 3 Days)</span>
      </div>
      
      <div className="space-y-3 max-h-80 overflow-y-auto">
        {alarms.map((alarm) => (
          <div
            key={alarm.id}
            className={`border-l-4 ${getSeverityColor(alarm.severity)} ${getSeverityBg(alarm.severity)} 
                       p-3 rounded-r-md cursor-pointer transition-all duration-200 hover:bg-opacity-20`}
            onClick={() => toggleExpanded(alarm.id)}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2 mb-1">
                  <Clock className="h-3 w-3 text-muted-foreground flex-shrink-0" />
                  <span className="text-xs text-muted-foreground">
                    {alarm.date} • {alarm.time}
                  </span>
                </div>
                <p className="text-sm font-medium text-foreground truncate">
                  {alarm.description}
                </p>
                {expandedAlarm === alarm.id && (
                  <div className="mt-2 pt-2 border-t border-border/50">
                    <p className="text-xs text-muted-foreground leading-relaxed">
                      {alarm.details}
                    </p>
                  </div>
                )}
              </div>
              <div className="ml-2 flex-shrink-0">
                {expandedAlarm === alarm.id ? (
                  <ChevronUp className="h-4 w-4 text-muted-foreground" />
                ) : (
                  <ChevronDown className="h-4 w-4 text-muted-foreground" />
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-4 pt-3 border-t border-border">
        <p className="text-xs text-muted-foreground text-center">
          Showing recent space weather events that may affect satellite operations
        </p>
      </div>
    </div>
  );
};

export default AlarmsWidget;