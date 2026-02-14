import { Evidence } from '../services/api'

interface EvidenceListProps {
  evidence: Evidence[]
}

export default function EvidenceList({ evidence }: EvidenceListProps) {
  return (
    <div className="card p-8">
      <h3 className="font-semibold text-white mb-4">Supporting Evidence</h3>

      {evidence.length === 0 ? (
        <p className="text-sm text-slate-500 italic">No evidence available</p>
      ) : (
        <div className="space-y-4 max-h-96 overflow-y-auto">
          {evidence.map((item, index) => (
            <div key={index} className="border-l-2 border-blue-500 pl-4 py-3 bg-slate-800/50 rounded-r-lg">
              <p className="text-sm text-slate-200 mb-2">{item.clause}</p>
              <div className="flex items-center space-x-4 text-xs text-slate-500">
                <span>{item.source}</span>
                <span>Page {item.page}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
