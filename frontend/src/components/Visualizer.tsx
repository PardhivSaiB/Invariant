import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeft, ChevronRight, Play, Pause, RotateCcw } from 'lucide-react';

interface VisualStep {
  step_number: number;
  left_pointer?: number;
  right_pointer?: number;
  window_state: any;
  action: string;
  explanation: string;
  invariant_status: string;
}

interface VisualizerProps {
  steps: VisualStep[];
  pattern: string;
  invariant: string;
}

const Visualizer: React.FC<VisualizerProps> = ({ steps, pattern, invariant }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    let interval: any;
    if (isPlaying && currentStep < steps.length - 1) {
      interval = setInterval(() => {
        setCurrentStep((prev) => prev + 1);
      }, 1500);
    } else {
      setIsPlaying(false);
    }
    return () => clearInterval(interval);
  }, [isPlaying, currentStep, steps.length]);

  const nextStep = () => {
    if (currentStep < steps.length - 1) setCurrentStep(currentStep + 1);
  };

  const prevStep = () => {
    if (currentStep > 0) setCurrentStep(currentStep - 1);
  };

  const reset = () => {
    setCurrentStep(0);
    setIsPlaying(false);
  };

  const step = steps[currentStep];
  if (!step) return null;

  // Attempt to extract array from window_state if it's a string or list
  const getArrayState = () => {
    if (Array.isArray(step.window_state)) return step.window_state;
    if (typeof step.window_state === 'string') return step.window_state.split('');
    return [];
  };

  const data = getArrayState();

  return (
    <div className="card space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-xl font-bold text-white">{pattern} Visualization</h3>
          <p className="text-sm text-slate-400">Invariant: <span className="text-blue-400 font-mono italic">{invariant}</span></p>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={reset} className="p-2 hover:bg-white/5 rounded-lg text-slate-400"><RotateCcw size={20} /></button>
          <button onClick={prevStep} disabled={currentStep === 0} className="p-2 hover:bg-white/5 disabled:opacity-30 rounded-lg text-slate-400"><ChevronLeft size={24} /></button>
          <button onClick={() => setIsPlaying(!isPlaying)} className="p-3 bg-blue-600/20 text-blue-400 rounded-full hover:bg-blue-600/30 transition-colors">
            {isPlaying ? <Pause size={24} /> : <Play size={24} />}
          </button>
          <button onClick={nextStep} disabled={currentStep === steps.length - 1} className="p-2 hover:bg-white/5 disabled:opacity-30 rounded-lg text-slate-400"><ChevronRight size={24} /></button>
        </div>
      </div>

      <div className="relative py-12 px-4 bg-slate-900/50 rounded-xl border border-white/5 overflow-hidden">
        <div className="flex justify-center items-end gap-3 min-h-[100px]">
          {data.map((item, idx) => {
            const isLeft = idx === step.left_pointer;
            const isRight = idx === step.right_pointer;
            const inWindow = (step.left_pointer !== undefined && step.right_pointer !== undefined) && 
                            (idx >= step.left_pointer && idx <= step.right_pointer);

            return (
              <div key={idx} className="relative flex flex-col items-center">
                <AnimatePresence mode="popLayout">
                  {isLeft && (
                    <motion.div
                      initial={{ opacity: 0, y: -20 }}
                      animate={{ opacity: 1, y: -4 }}
                      exit={{ opacity: 0, y: -20 }}
                      className="absolute -top-10 text-xs font-bold text-blue-400 bg-blue-400/10 px-2 py-1 rounded"
                    >
                      L
                    </motion.div>
                  )}
                  {isRight && (
                    <motion.div
                      initial={{ opacity: 0, y: -20 }}
                      animate={{ opacity: 1, y: -4 }}
                      exit={{ opacity: 0, y: -20 }}
                      className="absolute -top-10 text-xs font-bold text-indigo-400 bg-indigo-400/10 px-2 py-1 rounded"
                    >
                      R
                    </motion.div>
                  )}
                </AnimatePresence>
                
                <motion.div
                  layout
                  className={`w-12 h-12 flex items-center justify-center rounded-lg border-2 text-lg font-bold transition-colors
                    ${inWindow ? 'bg-blue-600/20 border-blue-500/50 text-white' : 'bg-white/5 border-white/10 text-slate-500'}
                    ${(isLeft || isRight) ? 'ring-2 ring-white/20' : ''}
                  `}
                >
                  {item}
                </motion.div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="md:col-span-2 space-y-2">
          <div className="flex items-center gap-2">
             <span className="px-2 py-1 rounded bg-blue-500/10 text-blue-400 text-[10px] font-bold uppercase tracking-wider">
               Action: {step.action}
             </span>
             <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wider ${
               step.invariant_status.toLowerCase().includes('valid') || step.invariant_status.toLowerCase().includes('maintained') 
               ? 'bg-green-500/10 text-green-400' 
               : 'bg-red-500/10 text-red-400'
             }`}>
               {step.invariant_status}
             </span>
          </div>
          <p className="text-slate-200 leading-relaxed">{step.explanation}</p>
        </div>
        <div className="bg-white/5 rounded-xl p-4 flex flex-col justify-center items-center">
           <span className="text-xs text-slate-400 uppercase tracking-widest mb-1">Step</span>
           <span className="text-3xl font-bold text-white font-mono">{step.step_number} / {steps.length}</span>
        </div>
      </div>

      {/* Progress bar */}
      <div className="h-1 bg-white/5 rounded-full overflow-hidden">
        <motion.div 
          initial={{ width: 0 }}
          animate={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
          className="h-full bg-blue-600"
        />
      </div>
    </div>
  );
};

export default Visualizer;
