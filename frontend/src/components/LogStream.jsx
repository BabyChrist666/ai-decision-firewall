import React, { useState, useEffect, useRef, useImperativeHandle, forwardRef } from 'react';

function getTimestamp() {
  const now = new Date();
  return now.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
}

const LogStream = forwardRef(({ isActive = true }, ref) => {
  const [logs, setLogs] = useState([]);
  const logEndRef = useRef(null);

  const addLog = (message) => {
    const newLog = {
      id: Date.now(),
      message,
      timestamp: getTimestamp(),
    };
    setLogs((prev) => {
      const updated = [...prev, newLog];
      return updated.slice(-20);
    });
  };

  useImperativeHandle(ref, () => ({
    addLog,
  }));

  useEffect(() => {
    if (!isActive) return;

    const initialLogs = [
      { id: 1, message: 'SYSTEM INITIALIZED', timestamp: getTimestamp() },
      { id: 2, message: 'FIREWALL ACTIVE', timestamp: getTimestamp() },
      { id: 3, message: 'MONITORING AI SYSTEMS...', timestamp: getTimestamp() },
    ];
    setLogs(initialLogs);

    const interval = setInterval(() => {
      const logMessages = [
        'MONITORING AI SYSTEMS...',
        'SCANNING OUTPUTS...',
        'POLICY ENFORCEMENT READY',
        'AWAITING INTERCEPTION...',
        'SYSTEM OPTIMAL',
        'NO ANOMALIES DETECTED',
      ];

      const randomMessage = logMessages[Math.floor(Math.random() * logMessages.length)];
      const newLog = {
        id: Date.now(),
        message: randomMessage,
        timestamp: getTimestamp(),
      };

      setLogs((prev) => {
        const updated = [...prev, newLog];
        return updated.slice(-20);
      });
    }, 4000);

    return () => clearInterval(interval);
  }, [isActive]);

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  return (
    <div className="glass-panel p-4 h-64 overflow-y-auto">
      <div className="mb-2 pb-2 border-b border-panel-border">
        <span className="text-sm uppercase tracking-wider text-neon-cyan font-bold">
          SYSTEM LOG
        </span>
      </div>
      <div className="space-y-1 font-mono text-xs">
        {logs.map((log) => (
          <div key={log.id} className="terminal-line">
            <span className="text-gray-500">[{log.timestamp}]</span>{' '}
            <span className="text-green-400">{log.message}</span>
          </div>
        ))}
        <div ref={logEndRef} />
      </div>
    </div>
  );
});

LogStream.displayName = 'LogStream';

export default LogStream;
