import { Analysis } from '../services/api'

interface VerdictCardProps {
  analysis: Analysis
  confidence: number
}

const verdictConfig = {
  covered: {
    bg: 'bg-green-900/20',
    border: 'border-green-700',
    text: 'text-green-100',
    badge: 'bg-green-600',
    label: 'Covered',
  },
  limited: {
    bg: 'bg-yellow-900/20',
    border: 'border-yellow-700',
    text: 'text-yellow-100',
    badge: 'bg-yellow-600',
    label: 'Limited Coverage',
  },
  conditional: {
    bg: 'bg-blue-900/20',
    border: 'border-blue-700',
    text: 'text-blue-100',
    badge: 'bg-blue-600',
    label: 'Conditional',
  },
  excluded: {
    bg: 'bg-red-900/20',
    border: 'border-red-700',
    text: 'text-red-100',
    badge: 'bg-red-600',
    label: 'Excluded',
  },
  not_specified: {
    bg: 'bg-slate-800',
    border: 'border-slate-700',
    text: 'text-slate-300',
    badge: 'bg-slate-600',
    label: 'Not Specified',
  },
  out_of_scope: {
    bg: 'bg-slate-900',
    border: 'border-slate-800',
    text: 'text-slate-400',
    badge: 'bg-slate-700',
    label: 'Out of Scope',
  },
}

export default function VerdictCard({ analysis, confidence }: VerdictCardProps) {
  const config = verdictConfig[analysis.verdict]
  const confidencePercent = Math.round(confidence * 100)

  return (
    <div className={`card border-2 ${config.border} ${config.bg} p-8 mb-8`}>
      <div className="mb-6">
        <span className={`inline-block px-4 py-2 rounded-lg font-semibold text-white ${config.badge}`}>
          {config.label}
        </span>
      </div>

      <div className="space-y-4">
        <div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-sm font-medium text-slate-300">Confidence Score</label>
            <span className="text-2xl font-bold text-white">{confidencePercent}%</span>
          </div>
          <div className="h-3 rounded-full bg-slate-800 overflow-hidden">
            <div
              className={`h-full rounded-full transition-all duration-300 ${config.badge}`}
              style={{ width: `${confidencePercent}%` }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  )
}
