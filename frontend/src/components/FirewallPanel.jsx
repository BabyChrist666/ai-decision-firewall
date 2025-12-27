import React, { useState } from 'react';

const FirewallPanel = ({ onSubmit, isLoading }) => {
  const [aiOutput, setAiOutput] = useState('');
  const [confidence, setConfidence] = useState(0.5);
  const [intendedAction, setIntendedAction] = useState('answer');
  const [sources, setSources] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const sourcesArray = sources
      .split(',')
      .map((s) => s.trim())
      .filter((s) => s.length > 0);

    onSubmit({
      ai_output: aiOutput,
      confidence: parseFloat(confidence),
      intended_action: intendedAction,
      sources: sourcesArray,
    });
  };

  return (
    <div className="glass-panel p-6 space-y-6 scanline">
      <div className="border-b border-panel-border pb-4">
        <h2 className="text-2xl font-bold uppercase tracking-wider text-neon-cyan">
          INTERCEPT OUTPUT
        </h2>
        <p className="text-sm text-gray-400 mt-1">
          Submit AI-generated content for firewall evaluation
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label className="block text-sm uppercase tracking-wider text-gray-400 mb-2">
            AI Output
          </label>
          <textarea
            className="input-field w-full h-32 resize-none"
            value={aiOutput}
            onChange={(e) => setAiOutput(e.target.value)}
            placeholder="Enter AI-generated output..."
            required
          />
        </div>

        <div>
          <label className="block text-sm uppercase tracking-wider text-gray-400 mb-2">
            Confidence: {Math.round(confidence * 100)}%
          </label>
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={confidence}
            onChange={(e) => setConfidence(e.target.value)}
            className="w-full h-2 bg-bg-dark rounded-lg appearance-none cursor-pointer accent-neon-cyan"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>0%</span>
            <span>50%</span>
            <span>100%</span>
          </div>
        </div>

        <div>
          <label className="block text-sm uppercase tracking-wider text-gray-400 mb-2">
            Intended Action
          </label>
          <select
            className="input-field w-full"
            value={intendedAction}
            onChange={(e) => setIntendedAction(e.target.value)}
            required
          >
            <option value="answer">Answer</option>
            <option value="email">Email</option>
            <option value="trade">Trade</option>
            <option value="execute_code">Execute Code</option>
          </select>
        </div>

        <div>
          <label className="block text-sm uppercase tracking-wider text-gray-400 mb-2">
            Sources (comma-separated URLs)
          </label>
          <input
            type="text"
            className="input-field w-full"
            value={sources}
            onChange={(e) => setSources(e.target.value)}
            placeholder="https://example.com/source1, https://example.com/source2"
          />
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className={`
            cyber-button-primary w-full
            ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}
          `}
        >
          {isLoading ? 'PROCESSING...' : 'INTERCEPT OUTPUT'}
        </button>
      </form>
    </div>
  );
};

export default FirewallPanel;




