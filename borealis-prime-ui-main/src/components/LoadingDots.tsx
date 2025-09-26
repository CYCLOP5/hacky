const LoadingDots = () => {
  return (
    <div className="flex space-x-1">
      <div className="w-2 h-2 bg-primary rounded-full animate-bounce-dots"></div>
      <div className="w-2 h-2 bg-primary rounded-full animate-bounce-dots"></div>
      <div className="w-2 h-2 bg-primary rounded-full animate-bounce-dots"></div>
    </div>
  );
};

export default LoadingDots;