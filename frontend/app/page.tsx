'use client';

import React, { useState } from "react";

export default function Dashboard() {
  const [question, setQuestion] = useState("What are the top 3 countries with the highest total order quantity?");
  const [loading, setLoading] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [response, setResponse] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResponse(null);
    setLogs([]);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/stream-query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      if (!res.ok) throw new Error("Failed to connect to agent swarm");

      const reader = res.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) throw new Error("Stream reader unavailable");

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split("\n\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const jsonStr = line.replace("data: ", "");
            const data = JSON.parse(jsonStr);

            setLogs((prev) => [...prev, data.message]);

            if (data.step === "complete") {
              setResponse(data);
            }
            if (data.step === "error") {
              setError(data.message);
            }
          }
        }
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-8 font-sans">
      <div className="max-w-5xl mx-auto space-y-8">
        
        {/* Header */}
        <div className="border-b border-slate-800 pb-6 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">
              SchemaPilot FDE Console
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Autonomous Multi-Agent Analytics & Self-Healing Governance Engine
            </p>
          </div>
          <div className="flex gap-2">
            <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 text-xs font-semibold rounded-full border border-emerald-500/20">
              ? Swarm Live
            </span>
            <span className="px-3 py-1 bg-blue-500/10 text-blue-400 text-xs font-semibold rounded-full border border-blue-500/20">
              DuckDB + dbt
            </span>
          </div>
        </div>

        {/* Input Form */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
          <form onSubmit={handleQuery} className="space-y-4">
            <label className="block text-sm font-medium text-slate-300">
              Natural Language Data Question
            </label>
            <div className="flex gap-3">
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-100"
                placeholder="Ask an analytical question..."
              />
              <button
                type="submit"
                disabled={loading}
                className="bg-blue-600 hover:bg-blue-500 text-white font-semibold px-6 py-3 rounded-lg text-sm transition-all disabled:opacity-50 flex items-center gap-2"
              >
                {loading ? "Swarm Thinking..." : "Execute Swarm"}
              </button>
            </div>
          </form>
        </div>

        {/* Live Thought Stream */}
        {logs.length > 0 && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-3">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              Live Multi-Agent Thought Stream
            </h3>
            <div className="bg-slate-950 p-4 rounded-lg font-mono text-xs space-y-2 border border-slate-800 max-h-48 overflow-y-auto">
              {logs.map((log, idx) => (
                <p key={idx} className="text-slate-300">{log}</p>
              ))}
            </div>
          </div>
        )}

        {/* Error Banner */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4 text-red-400 text-sm">
            ?? <strong>Error:</strong> {error}
          </div>
        )}

        {/* Results Section */}
        {response && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            {/* Generated SQL & Metrics */}
            <div className="md:col-span-1 space-y-6">
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-3">
                <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                  Generated DuckDB SQL
                </h3>
                <pre className="bg-slate-950 p-3 rounded-lg text-xs font-mono text-blue-300 overflow-x-auto border border-slate-800">
                  {response.generated_sql}
                </pre>
              </div>

              <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex justify-between items-center">
                <div>
                  <p className="text-xs font-bold text-slate-400 uppercase">Execution Latency</p>
                  <p className="text-lg font-bold text-slate-200 mt-1">{response.latency_ms} ms</p>
                </div>
                <div>
                  <p className="text-xs font-bold text-slate-400 uppercase">Status</p>
                  <span className="inline-block mt-1 px-2.5 py-0.5 bg-emerald-500/20 text-emerald-400 text-xs font-semibold rounded">
                    {response.status}
                  </span>
                </div>
              </div>
            </div>

            {/* Data Results Table */}
            <div className="md:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col">
              <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">
                Structured Result Set
              </h3>
              <div className="flex-1 overflow-x-auto border border-slate-800 rounded-lg bg-slate-950">
                <table className="w-full text-left border-collapse text-sm">
                  <tbody>
                    {response.results.map((row: any, idx: number) => (
                      <tr key={idx} className="border-b border-slate-900 hover:bg-slate-900/50">
                        {row.map((val: any, vIdx: number) => (
                          <td key={vIdx} className="px-4 py-3 text-slate-300">
                            {String(val)}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

          </div>
        )}

      </div>
    </main>
  );
}
