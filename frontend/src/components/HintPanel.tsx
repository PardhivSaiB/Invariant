import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Lightbulb, ChevronDown, ChevronUp, Lock } from 'lucide-react';

interface Hints {
  conceptual_hint: string;
  data_structure_hint: string;
  logic_hint: string;
  common_mistake_warning: string;
  invariant_hint: string;
}

interface HintPanelProps {
  hints: Hints;
}

const HintPanel: React.FC<HintPanelProps> = ({ hints }) => {
  const [unlockedLevel, setUnlockedLevel] = useState(0);

  const hintLevels = [
    { title: 'Conceptual Hint', content: hints.conceptual_hint, icon: <Lightbulb className="text-yellow-400" /> },
    { title: 'Data Structure Hint', content: hints.data_structure_hint, icon: <Lightbulb className="text-blue-400" /> },
    { title: 'Logic Hint', content: hints.logic_hint, icon: <Lightbulb className="text-green-400" /> },
    { title: 'Invariant Hint', content: hints.invariant_hint, icon: <Lightbulb className="text-purple-400" /> },
    { title: 'Common Mistake Warning', content: hints.common_mistake_warning, icon: <Lightbulb className="text-red-400" /> },
  ];

  return (
    <div className="card space-y-4">
      <div className="flex items-center gap-2 mb-4">
        <Lightbulb className="text-blue-500" />
        <h3 className="text-xl font-bold text-white">Mentor Hints</h3>
      </div>
      
      <div className="space-y-3">
        {hintLevels.map((hint, idx) => {
          const isUnlocked = idx <= unlockedLevel;
          
          return (
            <div key={idx} className={`rounded-xl border transition-all duration-300 ${
              isUnlocked ? 'border-white/10 bg-white/5' : 'border-white/5 bg-white/[0.02] opacity-60'
            }`}>
              <button 
                onClick={() => isUnlocked && setUnlockedLevel(idx)}
                className="w-full p-4 flex items-center justify-between text-left"
              >
                <div className="flex items-center gap-3">
                  {isUnlocked ? hint.icon : <Lock size={18} className="text-slate-600" />}
                  <span className={`font-medium ${isUnlocked ? 'text-slate-200' : 'text-slate-500'}`}>{hint.title}</span>
                </div>
                {!isUnlocked && idx === unlockedLevel + 1 && (
                  <button 
                    onClick={(e) => { e.stopPropagation(); setUnlockedLevel(idx); }}
                    className="text-xs font-bold text-blue-400 hover:text-blue-300 uppercase tracking-wider"
                  >
                    Unlock
                  </button>
                )}
              </button>
              
              <AnimatePresence>
                {isUnlocked && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    className="overflow-hidden"
                  >
                    <div className="p-4 pt-0 text-slate-400 text-sm leading-relaxed border-t border-white/5">
                      {hint.content}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default HintPanel;
