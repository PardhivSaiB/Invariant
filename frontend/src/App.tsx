import React from 'react'
import Editor from '@monaco-editor/react'
import { Play, Lightbulb, Activity, Layers } from 'lucide-react'

function App() {
  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col">
      <header className="p-4 border-b border-slate-800 flex justify-between items-center">
        <h1 className="text-xl font-bold text-blue-400">AI DSA Mentor</h1>
        <div className="flex gap-4">
          <button className="px-4 py-2 bg-slate-800 rounded-md hover:bg-slate-700 transition">Login</button>
        </div>
      </header>
      
      <main className="flex-1 flex overflow-hidden">
        {/* Left: Code Editor */}
        <div className="w-1/2 border-r border-slate-800 flex flex-col">
          <div className="p-2 bg-slate-800 flex justify-between items-center">
            <span className="text-sm font-medium">editor.py</span>
            <button className="flex items-center gap-2 px-3 py-1 bg-blue-600 rounded hover:bg-blue-500 text-sm">
              <Play size={16} /> Run Analysis
            </button>
          </div>
          <div className="flex-1">
            <Editor
              height="100%"
              defaultLanguage="python"
              defaultValue="# Write your DSA solution here..."
              theme="vs-dark"
              options={{ minimap: { enabled: false } }}
            />
          </div>
        </div>
        
        {/* Right: Insights & Visualization */}
        <div className="w-1/2 flex flex-col overflow-y-auto">
          <div className="p-4 space-y-6">
            <section>
              <h2 className="text-lg font-semibold flex items-center gap-2 mb-4">
                <Activity size={20} className="text-emerald-400" /> Visualization Panel
              </h2>
              <div className="aspect-video bg-slate-800 rounded-lg border border-slate-700 flex items-center justify-center">
                <p className="text-slate-400 italic">Algorithm execution will be visualized here</p>
              </div>
            </section>
            
            <section className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-slate-800 rounded-lg border border-slate-700">
                <h3 className="text-sm font-medium text-slate-400 flex items-center gap-2 mb-2">
                  <Layers size={16} /> Pattern Detected
                </h3>
                <p className="text-lg font-bold">Sliding Window</p>
              </div>
              <div className="p-4 bg-slate-800 rounded-lg border border-slate-700">
                <h3 className="text-sm font-medium text-slate-400 flex items-center gap-2 mb-2">
                  <Activity size={16} /> Complexity
                </h3>
                <p className="text-lg font-bold">T: O(N) | S: O(1)</p>
              </div>
            </section>
            
            <section>
              <h2 className="text-lg font-semibold flex items-center gap-2 mb-4">
                <Lightbulb size={20} className="text-yellow-400" /> Mentor Hints
              </h2>
              <div className="space-y-3">
                <div className="p-3 bg-slate-800 border-l-4 border-yellow-500 rounded">
                  <p className="text-sm">Try expanding the right pointer until the condition is met.</p>
                </div>
              </div>
            </section>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
