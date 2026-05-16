import React, { useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertCircle, Brain, Layout, Sparkles } from 'lucide-react';

import InputPanel from './components/InputPanel';
import AnalysisDashboard from './components/AnalysisDashboard';
import HintPanel from './components/HintPanel';
import Visualizer from './components/Visualizer';

const API_BASE_URL = 'http://localhost:8000/api';

function App() {
  // Input State
  const [url, setUrl] = useState('');
  const [language, setLanguage] = useState('java');
  const [code, setCode] = useState('');
  
  // App State
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    setIsAnalyzing(true);
    setError(null);
    try {
      const response = await axios.post(`${API_BASE_URL}/analyze/`, {
        leetcode_url: url,
        language,
        code,
      });
      setResult(response.data);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to analyze the code. Please ensure the backend is running.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen pb-20 relative overflow-hidden">
      {/* Background Orbs */}
      <div className="glow top-[-100px] left-[-100px] opacity-20" />
      <div className="glow bottom-[-100px] right-[-100px] opacity-20" style={{ background: 'radial-gradient(circle, rgba(139, 92, 246, 0.15) 0%, transparent 70%)' }} />

      {/* Navbar */}
      <nav className="border-b border-white/5 bg-black/20 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center shadow-lg shadow-blue-600/40">
              <Sparkles size={18} className="text-white" />
            </div>
            <span className="text-2xl font-black tracking-tighter text-white">INVARIANT</span>
          </div>
          <div className="hidden md:flex items-center gap-6 text-sm font-medium text-slate-400">
            <span className="text-blue-400">Mentor</span>
            <span className="hover:text-white cursor-pointer transition-colors">Curriculum</span>
            <span className="hover:text-white cursor-pointer transition-colors">Docs</span>
            <div className="h-4 w-px bg-white/10 mx-2" />
            <button className="px-4 py-1.5 rounded-full border border-white/10 hover:bg-white/5 transition-all">
              Sign In
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 pt-12 space-y-12">
        {/* Header Section */}
        <header className="text-center space-y-4 max-w-2xl mx-auto mb-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-bold uppercase tracking-widest"
          >
            <Brain size={14} /> AI DSA Mentorship
          </motion.div>
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-5xl md:text-6xl font-black tracking-tight text-white"
          >
            Learn the <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400">Reasoning</span> behind algorithms.
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-lg text-slate-400"
          >
            Paste your solution and let Invariant guide you through patterns, complexity, and visual execution steps.
          </motion.p>
        </header>

        {/* Input and Error Handling */}
        <section className="grid grid-cols-1 gap-8">
          <InputPanel
            url={url} setUrl={setUrl}
            language={language} setLanguage={setLanguage}
            code={code} setCode={setCode}
            onAnalyze={handleAnalyze}
            isAnalyzing={isAnalyzing}
          />

          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 flex items-center gap-3"
              >
                <AlertCircle size={20} />
                <p className="font-medium">{error}</p>
              </motion.div>
            )}
          </AnimatePresence>
        </section>

        {/* Results Sections */}
        <AnimatePresence>
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-12"
            >
              <div className="flex items-center gap-4">
                <div className="h-px bg-white/10 flex-grow" />
                <h2 className="text-xs font-bold text-slate-500 uppercase tracking-[0.3em] whitespace-nowrap">Analysis Results</h2>
                <div className="h-px bg-white/10 flex-grow" />
              </div>

              {/* Analysis and Hints Grid */}
              <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
                <div className="xl:col-span-2">
                  <AnalysisDashboard 
                    pattern={result.pattern_analysis} 
                    complexity={result.complexity_analysis} 
                  />
                </div>
                <div className="xl:col-span-1">
                  <HintPanel hints={result.hints} />
                </div>
              </div>

              {/* Visualization Section */}
              <section className="space-y-6">
                <div className="flex items-center gap-2 text-indigo-400 mb-2">
                  <Layout size={20} />
                  <h3 className="text-xl font-bold text-white uppercase tracking-wider">Whiteboard Replay</h3>
                </div>
                <Visualizer 
                  steps={result.visualization.steps}
                  pattern={result.visualization.pattern}
                  invariant={result.visualization.invariant}
                />
              </section>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Footer */}
      <footer className="mt-20 py-12 border-t border-white/5 text-center space-y-4">
        <p className="text-slate-500 text-sm italic font-mono">
          "The best way to understand an algorithm is to see it fail and then see it fixed."
        </p>
        <div className="flex justify-center gap-4 text-xs font-bold text-slate-600 uppercase tracking-widest">
           <span>© 2026 Invariant AI</span>
           <span>•</span>
           <span className="hover:text-white cursor-pointer transition-colors">Privacy</span>
           <span>•</span>
           <span className="hover:text-white cursor-pointer transition-colors">Terms</span>
        </div>
      </footer>
    </div>
  );
}

export default App;
