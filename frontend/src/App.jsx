import React, { useState, useRef } from 'react';
import FirewallPanel from './components/FirewallPanel';
import VerdictBadge from './components/VerdictBadge';
import RiskMeter from './components/RiskMeter';
import LogStream from './components/LogStream';
import { checkFirewall } from './api';

function App() {
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const logStreamRef = useRef(null);

  const handleIntercept = async (request) => {
    setIsLoading(true);
    setError(null);
    setResponse(null);

    // Add log entry when interception starts
    if (logStreamRef.current?.addLog) {
      logStreamRef.current.addLog('OUTPUT INTERCEPTED');
    }

    try {
      const result = await checkFirewall(request);
      setResponse(result);
      
      // Add log entries after response
      if (logStreamRef.current?.addLog) {
        setTimeout(() => {
          logStreamRef.current.addLog('RISK SCORE COMPUTED');
          logStreamRef.current.addLog(`VERDICT: ${result.verdict}`);
        }, 100);
      }
    } catch (err) {
      setError(err.message || 'Failed to check firewall');
      if (logStreamRef.current?.addLog) {
        logStreamRef.current.addLog(`ERROR: ${err.message}`);
      }
      console.error('Firewall check error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-bg-darker text-neon-cyan p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <header className="text-center py-8 border-b border-panel-border">
          <h1 className="text-5xl font-bold uppercase tracking-wider mb-2">
            <span className="text-neon-cyan">AI DECISION</span>{' '}
            <span className="text-neon-magenta">FIREWALL</span>
          </h1>
          <p className="text-lg text-gray-400 mt-2">
            Runtime Governance for Artificial Intelligence
          </p>
          <div className="mt-4 flex items-center justify-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-success rounded-full animate-pulse"></div>
              <span className="text-sm uppercase tracking-wider">System Active</span>
            </div>
            <span className="text-gray-600">|</span>
            <span className="text-sm text-gray-400 animate-flicker">
              Monitoring AI Systems...
            </span>
          </div>
        </header>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Input Panel */}
          <div className="lg:col-span-2">
            <FirewallPanel onSubmit={handleIntercept} isLoading={isLoading} />
          </div>

          {/* Right Column - Log Stream */}
          <div>
            <LogStream ref={logStreamRef} isActive={true} />
          </div>
        </div>

        {/* Verdict Display */}
        {response && (
          <div className="glass-panel p-6 space-y-6 animate-fadeIn">
            <div className="flex items-center justify-between border-b border-panel-border pb-4">
              <h2 className="text-2xl font-bold uppercase tracking-wider text-neon-cyan">
                VERDICT
              </h2>
              <VerdictBadge verdict={response.verdict} size="lg" />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Risk Score */}
              <div>
                <RiskMeter riskScore={response.risk_score} />
              </div>

              {/* Details */}
              <div className="space-y-4">
                <div>
                  <h3 className="text-sm uppercase tracking-wider text-gray-400 mb-2">
                    Reason
                  </h3>
                  <p className="text-neon-cyan">{response.reason}</p>
                </div>

                <div>
                  <h3 className="text-sm uppercase tracking-wider text-gray-400 mb-2">
                    Explanation
                  </h3>
                  <p className="text-gray-300 leading-relaxed">{response.explanation}</p>
                </div>

                {response.confidence_alignment !== null && (
                  <div>
                    <h3 className="text-sm uppercase tracking-wider text-gray-400 mb-2">
                      Confidence Alignment
                    </h3>
                    <div className="flex items-center space-x-2">
                      {response.confidence_alignment ? (
                        <>
                          <div className="w-3 h-3 bg-success rounded-full"></div>
                          <span className="text-success">Aligned</span>
                        </>
                      ) : (
                        <>
                          <div className="w-3 h-3 bg-warning rounded-full"></div>
                          <span className="text-warning">Misaligned</span>
                        </>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Failed Checks */}
            {response.failed_checks && response.failed_checks.length > 0 && (
              <div className="border-t border-panel-border pt-4">
                <h3 className="text-sm uppercase tracking-wider text-gray-400 mb-3">
                  Failed Checks
                </h3>
                <div className="flex flex-wrap gap-2">
                  {response.failed_checks.map((check, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-danger/20 border border-danger text-danger text-xs uppercase tracking-wider"
                    >
                      {check}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Details Object (Collapsible) */}
            {response.details && Object.keys(response.details).length > 0 && (
              <div className="border-t border-panel-border pt-4">
                <details className="cursor-pointer">
                  <summary className="text-sm uppercase tracking-wider text-gray-400 mb-2 hover:text-neon-cyan transition-colors">
                    Technical Details
                  </summary>
                  <pre className="mt-2 p-4 bg-bg-dark border border-panel-border text-xs text-gray-300 overflow-x-auto">
                    {JSON.stringify(response.details, null, 2)}
                  </pre>
                </details>
              </div>
            )}
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="glass-panel p-6 border-danger border-2 shadow-glow-red">
            <div className="flex items-center space-x-3">
              <div className="w-3 h-3 bg-danger rounded-full animate-pulse"></div>
              <h3 className="text-lg font-bold uppercase tracking-wider text-danger">
                Error
              </h3>
            </div>
            <p className="mt-2 text-gray-300">{error}</p>
          </div>
        )}

        {/* Footer */}
        <footer className="text-center py-4 border-t border-panel-border text-xs text-gray-500">
          <p>AI Decision Firewall v1.0.0 | Runtime Governance System</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
