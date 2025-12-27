import React from 'react';

const VerdictBadge = ({ verdict, size = 'lg' }) => {
  const verdictStyles = {
    ALLOW: {
      bg: 'bg-success/20',
      border: 'border-success',
      text: 'text-success',
      glow: 'shadow-glow-green',
      label: 'ALLOW',
    },
    BLOCK: {
      bg: 'bg-danger/20',
      border: 'border-danger',
      text: 'text-danger',
      glow: 'shadow-glow-red',
      label: 'BLOCK',
    },
    REQUIRE_EVIDENCE: {
      bg: 'bg-warning/20',
      border: 'border-warning',
      text: 'text-warning',
      glow: 'shadow-glow-yellow',
      label: 'REQUIRE_EVIDENCE',
    },
    REQUIRE_HUMAN_REVIEW: {
      bg: 'bg-danger/20',
      border: 'border-danger',
      text: 'text-danger',
      glow: 'shadow-glow-red',
      label: 'REQUIRE_HUMAN_REVIEW',
    },
  };

  const style = verdictStyles[verdict] || verdictStyles.ALLOW;
  const sizeClasses = {
    sm: 'text-xs px-3 py-1',
    md: 'text-sm px-4 py-2',
    lg: 'text-lg px-6 py-3',
  };

  return (
    <div
      className={`
        inline-flex items-center justify-center
        ${style.bg} ${style.border} ${style.text}
        border-2 ${style.glow}
        ${sizeClasses[size]}
        font-bold uppercase tracking-wider
        animate-pulse-slow
      `}
    >
      <span className="relative">
        {style.label}
        <span className="absolute inset-0 animate-flicker opacity-50">
          {style.label}
        </span>
      </span>
    </div>
  );
};

export default VerdictBadge;




