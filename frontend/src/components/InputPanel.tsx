import React from 'react';
import { Send, Globe, Code2 } from 'lucide-react';
import CodeEditor from './CodeEditor';

interface InputPanelProps {
  url: string;
  setUrl: (url: string) => void;
  language: string;
  setLanguage: (lang: string) => void;
  code: string;
  setCode: (code: string) => void;
  onAnalyze: () => void;
  isAnalyzing: boolean;
}

const InputPanel: React.FC<InputPanelProps> = ({
  url, setUrl, language, setLanguage, code, setCode, onAnalyze, isAnalyzing
}) => {
  return (
    <div className="card space-y-6">
      <div className="flex items-center gap-2 mb-2">
        <Code2 className="text-blue-500" />
        <h3 className="text-xl font-bold text-white">Problem Input</h3>
      </div>

      <div className="space-y-4">
        {/* URL Input */}
        <div className="space-y-1.5">
          <label className="text-xs text-slate-500 uppercase tracking-widest flex items-center gap-2">
            <Globe size={12} /> LeetCode Problem URL
          </label>
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://leetcode.com/problems/..."
            className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2.5 text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Language Selection */}
          <div className="space-y-1.5 md:col-span-1">
            <label className="text-xs text-slate-500 uppercase tracking-widest block">Language</label>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="w-full bg-white/5 border border-white/10 rounded-lg px-3 py-2.5 text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/50 appearance-none"
            >
              <option value="java" className="bg-slate-900">Java</option>
              <option value="python" className="bg-slate-900">Python</option>
            </select>
          </div>

          {/* Spacer/Editor Header */}
          <div className="md:col-span-3 flex items-end">
            <span className="text-xs text-slate-500 uppercase tracking-widest mb-1">Implementation</span>
          </div>
        </div>

        {/* Code Editor */}
        <CodeEditor 
          value={code} 
          onChange={(val) => setCode(val || '')} 
          language={language} 
        />

        {/* Action Button */}
        <button
          onClick={onAnalyze}
          disabled={isAnalyzing || !url || !code}
          className="btn-primary w-full py-4 flex items-center justify-center gap-2 text-lg"
        >
          {isAnalyzing ? (
            <>
              <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin" />
              Analyzing Algorithm...
            </>
          ) : (
            <>
              <Send size={20} />
              Start Mentorship Session
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default InputPanel;
