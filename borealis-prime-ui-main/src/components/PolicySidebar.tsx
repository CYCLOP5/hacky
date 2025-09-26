import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";
import { Minus, Plus } from "lucide-react";

interface PolicySidebarProps {
  onRunWorkflow: (data: any) => void;
}

const PolicySidebar = ({ onRunWorkflow }: PolicySidebarProps) => {
  const [assetValue, setAssetValue] = useState(250);
  const [shieldingLevel, setShieldingLevel] = useState("Standard");
  const [yearsInOrbit, setYearsInOrbit] = useState([5]);
  const [riskAdjustment, setRiskAdjustment] = useState([1.0]);

  const handleRunWorkflow = () => {
    onRunWorkflow({
      assetValue,
      shieldingLevel,
      yearsInOrbit: yearsInOrbit[0],
      riskAdjustment: riskAdjustment[0],
    });
  };

  const adjustAssetValue = (increment: number) => {
    setAssetValue(Math.max(1, assetValue + increment));
  };

  return (
    <div className="w-80 h-screen bg-sidebar border-r border-sidebar-border flex flex-col">
      <div className="p-6 border-b border-sidebar-border">
        <h2 className="text-lg font-semibold text-sidebar-foreground">Policy Configuration</h2>
      </div>
      
      <div className="flex-1 p-6 space-y-8">
        {/* Asset Details Section */}
        <div className="space-y-6">
          <h3 className="text-sm font-medium text-sidebar-foreground/70 uppercase tracking-wide">Asset Details</h3>
          
          {/* Asset Value */}
          <div className="space-y-3">
            <Label htmlFor="asset-value" className="text-sm font-medium text-sidebar-foreground">
              Asset Value ($ Millions)
            </Label>
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => adjustAssetValue(-10)}
                className="h-9 w-9 p-0 border-sidebar-border bg-sidebar-accent hover:bg-sidebar-accent/80"
              >
                <Minus className="h-4 w-4" />
              </Button>
              <Input
                id="asset-value"
                type="number"
                value={assetValue}
                onChange={(e) => setAssetValue(Number(e.target.value))}
                className="flex-1 text-center bg-sidebar-accent border-sidebar-border text-sidebar-foreground"
              />
              <Button
                variant="outline"
                size="sm"
                onClick={() => adjustAssetValue(10)}
                className="h-9 w-9 p-0 border-sidebar-border bg-sidebar-accent hover:bg-sidebar-accent/80"
              >
                <Plus className="h-4 w-4" />
              </Button>
            </div>
          </div>

          {/* Shielding Level */}
          <div className="space-y-3">
            <Label className="text-sm font-medium text-sidebar-foreground">Asset Shielding Level</Label>
            <Select value={shieldingLevel} onValueChange={setShieldingLevel}>
              <SelectTrigger className="bg-sidebar-accent border-sidebar-border text-sidebar-foreground">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-sidebar border-sidebar-border">
                <SelectItem value="Low">Low</SelectItem>
                <SelectItem value="Standard">Standard</SelectItem>
                <SelectItem value="High">High</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Years in Orbit */}
          <div className="space-y-3">
            <Label className="text-sm font-medium text-sidebar-foreground">
              Years in Orbit: {yearsInOrbit[0]}
            </Label>
            <Slider
              value={yearsInOrbit}
              onValueChange={setYearsInOrbit}
              max={20}
              min={1}
              step={1}
              className="w-full"
            />
          </div>
        </div>

        {/* Underwriter Adjustment Section */}
        <div className="space-y-6">
          <h3 className="text-sm font-medium text-sidebar-foreground/70 uppercase tracking-wide">Underwriter Adjustment</h3>
          
          <div className="space-y-3">
            <Label className="text-sm font-medium text-sidebar-foreground">
              Risk Adjustment Factor: {riskAdjustment[0].toFixed(1)}
            </Label>
            <Slider
              value={riskAdjustment}
              onValueChange={setRiskAdjustment}
              max={2.0}
              min={0.5}
              step={0.1}
              className="w-full"
            />
          </div>
        </div>
      </div>

      {/* Run Workflow Button */}
      <div className="p-6 border-t border-sidebar-border">
        <Button 
          onClick={handleRunWorkflow}
          className="w-full bg-alert-red hover:bg-alert-red/90 text-white font-semibold py-3 text-base"
        >
          Run Agentic Workflow
        </Button>
      </div>
    </div>
  );
};

export default PolicySidebar;