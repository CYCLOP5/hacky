import { Zap } from "lucide-react";

const CosmicIcon = () => {
  return (
    <div className="relative">
      <Zap className="h-5 w-5 text-primary" />
      <div className="absolute inset-0 h-5 w-5 animate-pulse-glow">
        <Zap className="h-5 w-5 text-primary-glow" />
      </div>
    </div>
  );
};

export default CosmicIcon;