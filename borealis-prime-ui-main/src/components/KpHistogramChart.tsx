import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip, Cell } from 'recharts';

const KpHistogramChart = () => {
  // Mock Kp index forecast data for next 72 hours
  const kpData = [
    { hour: '0h', kp: 2.1, level: 'low' },
    { hour: '3h', kp: 3.2, level: 'low' },
    { hour: '6h', kp: 4.5, level: 'medium' },
    { hour: '9h', kp: 5.8, level: 'medium' },
    { hour: '12h', kp: 7.2, level: 'high' },
    { hour: '15h', kp: 6.9, level: 'high' },
    { hour: '18h', kp: 5.1, level: 'medium' },
    { hour: '21h', kp: 3.8, level: 'medium' },
    { hour: '24h', kp: 2.9, level: 'low' },
    { hour: '27h', kp: 3.1, level: 'low' },
    { hour: '30h', kp: 4.2, level: 'medium' },
    { hour: '33h', kp: 5.5, level: 'medium' },
    { hour: '36h', kp: 6.8, level: 'high' },
    { hour: '39h', kp: 7.5, level: 'high' },
    { hour: '42h', kp: 6.2, level: 'high' },
    { hour: '45h', kp: 4.9, level: 'medium' },
    { hour: '48h', kp: 3.6, level: 'medium' },
    { hour: '51h', kp: 2.8, level: 'low' },
    { hour: '54h', kp: 3.4, level: 'low' },
    { hour: '57h', kp: 4.1, level: 'medium' },
    { hour: '60h', kp: 5.3, level: 'medium' },
    { hour: '63h', kp: 6.1, level: 'high' },
    { hour: '66h', kp: 4.7, level: 'medium' },
    { hour: '69h', kp: 3.2, level: 'low' },
    { hour: '72h', kp: 2.5, level: 'low' },
  ];

  const getBarColor = (level: string) => {
    switch (level) {
      case 'low': return 'hsl(var(--chart-low))';
      case 'medium': return 'hsl(var(--chart-medium))';
      case 'high': return 'hsl(var(--chart-high))';
      default: return 'hsl(var(--primary))';
    }
  };

  const CustomBar = (props: any) => {
    const { payload, ...rest } = props;
    return <Bar {...rest} fill={getBarColor(payload?.level)} />;
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="dashboard-card p-3">
          <p className="text-sm font-medium">{`Time: ${label}`}</p>
          <p className="text-sm text-primary">{`Kp Index: ${data.kp}`}</p>
          <p className="text-xs text-muted-foreground capitalize">{`Activity: ${data.level}`}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="dashboard-card p-6">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-foreground mb-2">
          Kp Index Forecast (Next 72 Hours)
        </h3>
        <div className="flex items-center space-x-4 text-sm">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: 'hsl(var(--chart-low))' }}></div>
            <span className="text-muted-foreground">Low (0-4)</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: 'hsl(var(--chart-medium))' }}></div>
            <span className="text-muted-foreground">Medium (4-6)</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: 'hsl(var(--chart-high))' }}></div>
            <span className="text-muted-foreground">High (6+)</span>
          </div>
        </div>
      </div>
      
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={kpData} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
            <XAxis 
              dataKey="hour" 
              tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }}
              axisLine={{ stroke: 'hsl(var(--border))' }}
              interval={2}
            />
            <YAxis 
              tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }}
              axisLine={{ stroke: 'hsl(var(--border))' }}
              domain={[0, 9]}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar 
              dataKey="kp" 
              radius={[2, 2, 0, 0]}
            >
              {kpData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={getBarColor(entry.level)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default KpHistogramChart;