import React from 'react';

const RiskMeter = ({ riskScore }) => {
  const percentage = Math.round(riskScore * 100);
  
  const getRiskLevel = (score) => {
    if (score < 0.3) return { level: 'LOW', color: 'bg-success', text: 'text-success' };
    if (score < 0.6) return { level: 'MEDIUM', color: 'bg-warning', text: 'text-warning' };
    return { level: 'HIGH', color: 'bg-danger', text: 'text-danger' };
  };

  const risk = getRiskLevel(riskScore);

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-sm uppercase tracking-wider text-gray-400">Risk Score</span>
        <span className={`text-2xl font-bold ${risk.text}`}>
          {percentage}%
        </span>
      </div>
      
      <div className="relative h-4 bg-bg-dark border border-panel-border overflow-hidden">
        <div
          className={`h-full ${risk.color} transition-all duration-500 relative`}
          style={{ width: `${percentage}%` }}
        >
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-pulse"></div>
        </div>
      </div>
      
      <div className="flex justify-between text-xs text-gray-500">
        <span>LOW</span>
        <span>MEDIUM</span>
        <span className="text-danger">HIGH</span>
      </div>
      
      <div className="text-right">
        <span className={`text-xs uppercase ${risk.text} font-bold`}>
          {risk.level} RISK
        </span>
      </div>
    </div>
  );
};

export default RiskMeter;




