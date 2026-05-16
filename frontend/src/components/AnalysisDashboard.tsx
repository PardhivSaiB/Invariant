import React from 'react';
import { Activity, Clock, Database, Search, Zap } from 'lucide-react';

interface AnalysisDashboardProps {
  pattern: {
    detected_pattern: string;
    confidence: number;
    reasoning: string;
    signals: string[];
    optimization_possible: boolean;
    recommended_pattern: string;
  };
  complexity: {
    time_complexity: string;
    space_complexity: string;
    reasoning: string;
    performance_bottlenecks: string[];
    optimization_opportunities: string[];
  };
}

const AnalysisDashboard: React.FC<AnalysisDashboardProps> = ({ pattern, complexity }) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Pattern Analysis */}
      <div className="card space-y-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-blue-500">
            <Search size={20} />
            <h3 className="text-xl font-bold text-white">Pattern Recognition</h3>
          </div>
          <div className="px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 text-xs font-bold border border-blue-500/20">
            {(pattern.confidence * 100).toFixed(0)}% Confidence
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <span className="text-xs text-slate-500 uppercase tracking-widest block mb-1">Detected Approach</span>
            <div className={`text-2xl font-bold ${pattern.optimization_possible ? 'text-orange-400' : 'text-green-400'}`}>
              {pattern.detected_pattern}
            </div>
          </div>

          <p className="text-slate-400 text-sm leading-relaxed">{pattern.reasoning}</p>

          <div className="space-y-2">
            <span className="text-xs text-slate-500 uppercase tracking-widest block">Signals Observed</span>
            <div className="flex flex-wrap gap-2">
              {pattern.signals.map((signal, idx) => (
                <span key={idx} className="px-2 py-1 rounded-md bg-white/5 border border-white/10 text-slate-300 text-xs">
                  {signal}
                </span>
              ))}
            </div>
          </div>

          {pattern.optimization_possible && (
            <div className="p-4 rounded-xl bg-orange-500/10 border border-orange-500/20 space-y-2">
              <div className="flex items-center gap-2 text-orange-400">
                <Zap size={16} />
                <span className="text-xs font-bold uppercase tracking-wider">Optimization Recommended</span>
              </div>
              <p className="text-sm text-slate-300">
                Consider using <span className="text-orange-300 font-bold">{pattern.recommended_pattern}</span> to improve performance.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Complexity Analysis */}
      <div className="card space-y-6">
        <div className="flex items-center gap-2 text-indigo-500">
          <Activity size={20} />
          <h3 className="text-xl font-bold text-white">Performance Metrics</h3>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="p-4 rounded-xl bg-white/5 border border-white/10">
            <div className="flex items-center gap-2 text-slate-500 mb-1">
              <Clock size={14} />
              <span className="text-[10px] uppercase tracking-widest">Time</span>
            </div>
            <div className="text-2xl font-mono font-bold text-indigo-400">{complexity.time_complexity}</div>
          </div>
          <div className="p-4 rounded-xl bg-white/5 border border-white/10">
            <div className="flex items-center gap-2 text-slate-500 mb-1">
              <Database size={14} />
              <span className="text-[10px] uppercase tracking-widest">Space</span>
            </div>
            <div className="text-2xl font-mono font-bold text-purple-400">{complexity.space_complexity}</div>
          </div>
        </div>

        <div className="space-y-4">
          <p className="text-slate-400 text-sm leading-relaxed">{complexity.reasoning}</p>

          <div className="space-y-2">
            <span className="text-xs text-slate-500 uppercase tracking-widest block">Bottlenecks</span>
            <div className="space-y-1">
              {complexity.performance_bottlenecks.map((b, idx) => (
                <div key={idx} className="flex items-start gap-2 text-sm text-slate-300">
                  <div className="mt-1.5 w-1.5 h-1.5 rounded-full bg-red-500/50 shrink-0" />
                  <span>{b}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <span className="text-xs text-slate-500 uppercase tracking-widest block">Optimization Path</span>
            <div className="space-y-1">
              {complexity.optimization_opportunities.map((o, idx) => (
                <div key={idx} className="flex items-start gap-2 text-sm text-slate-300">
                  <div className="mt-1.5 w-1.5 h-1.5 rounded-full bg-green-500/50 shrink-0" />
                  <span>{o}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisDashboard;
