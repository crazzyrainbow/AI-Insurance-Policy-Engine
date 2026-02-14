import { StructuredAnswer } from '../services/api'

interface StructuredAnswerProps {
  answer: StructuredAnswer
}

export default function StructuredAnswerComponent({ answer }: StructuredAnswerProps) {
  if (!answer) return null

  const renderContent = () => {
    const type = answer.answer_type

    // Coverage check
    if (type === 'coverage_check') {
      return (
        <div className="space-y-3">
          <div className="p-3 bg-green-900/20 border border-green-700/50 rounded-lg">
            <p className="text-sm text-green-300 font-semibold">✅ {answer.direct_answer}</p>
          </div>
          {answer.coverage_clauses && answer.coverage_clauses.length > 0 && (
            <div>
              <p className="text-xs text-slate-400 font-semibold mb-2">Coverage Details:</p>
              <ul className="space-y-1">
                {answer.coverage_clauses.map((clause: string, idx: number) => (
                  <li key={idx} className="text-xs text-slate-300 pl-3 border-l-2 border-green-700">
                    {clause.substring(0, 100)}...
                  </li>
                ))}
              </ul>
            </div>
          )}
          {answer.recommendation && (
            <p className="text-xs text-slate-400 italic">💡 {answer.recommendation}</p>
          )}
        </div>
      )
    }

    // Limits
    if (type === 'limits') {
      return (
        <div className="space-y-3">
          <div className="flex items-center justify-between mb-3">
            <p className="text-sm font-semibold text-yellow-300">{answer.summary}</p>
            <span className="text-xs bg-yellow-900/30 text-yellow-300 px-2 py-1 rounded">
              {answer.total_found} clauses
            </span>
          </div>
          
          {answer.identified_limits && answer.identified_limits.length > 0 ? (
            <div className="space-y-2">
              {answer.identified_limits.map((limit: any, idx: number) => (
                <div key={idx} className="p-3 bg-slate-800/50 rounded-lg border border-slate-700/50">
                  <p className="text-xs text-slate-300 leading-relaxed mb-2">{limit.clause}</p>
                  <div className="flex flex-wrap gap-2">
                    {limit.percentages && limit.percentages.length > 0 && (
                      <div className="text-xs bg-orange-900/30 text-orange-300 px-2 py-1 rounded">
                        📊 {limit.percentages.join(', ')}%
                      </div>
                    )}
                    {limit.amounts && limit.amounts.length > 0 && (
                      <div className="text-xs bg-green-900/30 text-green-300 px-2 py-1 rounded">
                        💰 {limit.amounts.slice(0, 2).join(', ')}
                      </div>
                    )}
                    {limit.durations && limit.durations.length > 0 && (
                      <div className="text-xs bg-blue-900/30 text-blue-300 px-2 py-1 rounded">
                        ⏱️ {limit.durations.map((d: any) => `${d[0]} ${d[1]}`).join(', ')}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-xs text-slate-400 italic">No specific limit values extracted</p>
          )}
        </div>
      )
    }

    // Exclusions
    if (type === 'exclusions') {
      return (
        <div className="space-y-2">
          <p className="text-sm font-semibold text-red-300">⚠️ {answer.warning}</p>
          <p className="text-xs text-slate-400">Found {answer.count} exclusions:</p>
          <ul className="space-y-1">
            {answer.excluded_items.slice(0, 5).map((item: string, idx: number) => (
              <li key={idx} className="text-xs text-slate-300 pl-3 border-l-2 border-red-700">
                {item.substring(0, 100)}...
              </li>
            ))}
          </ul>
        </div>
      )
    }

    // Requirements
    if (type === 'requirements') {
      const reqs = answer.required_items || {}
      return (
        <div className="space-y-3">
          <p className="text-sm font-semibold text-slate-200">Total Requirements: {answer.total_requirements}</p>
          
          {reqs.documents && reqs.documents.length > 0 && (
            <div>
              <p className="text-xs text-blue-300 font-semibold mb-1">📄 Documents:</p>
              <ul className="text-xs text-slate-300 space-y-1 ml-3">
                {reqs.documents.map((doc: string, idx: number) => (
                  <li key={idx} className="list-disc">{doc.substring(0, 80)}...</li>
                ))}
              </ul>
            </div>
          )}
          
          {reqs.approvals && reqs.approvals.length > 0 && (
            <div>
              <p className="text-xs text-green-300 font-semibold mb-1">✅ Approvals:</p>
              <ul className="text-xs text-slate-300 space-y-1 ml-3">
                {reqs.approvals.map((approval: string, idx: number) => (
                  <li key={idx} className="list-disc">{approval.substring(0, 80)}...</li>
                ))}
              </ul>
            </div>
          )}
          
          {reqs.notices && reqs.notices.length > 0 && (
            <div>
              <p className="text-xs text-yellow-300 font-semibold mb-1">🔔 Notices:</p>
              <ul className="text-xs text-slate-300 space-y-1 ml-3">
                {reqs.notices.map((notice: string, idx: number) => (
                  <li key={idx} className="list-disc">{notice.substring(0, 80)}...</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )
    }

    // Financial queries (deductible, copay, maximum_claim, reimbursement)
    if (type === 'deductible' || type === 'copay' || type === 'maximum_claim' || type === 'reimbursement') {
      return (
        <div className="space-y-3">
          <div className="flex items-center justify-between mb-3">
            <p className="text-sm font-semibold text-green-300">{answer.summary}</p>
            <span className="text-xs bg-green-900/30 text-green-300 px-2 py-1 rounded">
              {answer.total_clauses} items
            </span>
          </div>
          
          {answer.financial_details && answer.financial_details.length > 0 ? (
            <div className="space-y-2">
              {answer.financial_details.map((item: any, idx: number) => (
                <div key={idx} className="p-3 bg-slate-800/50 rounded-lg border border-slate-700/50">
                  <p className="text-xs text-slate-300 leading-relaxed mb-2">{item.description}</p>
                  <div className="flex flex-wrap gap-2">
                    {item.percentages && item.percentages.length > 0 && (
                      <div className="text-xs bg-blue-900/30 text-blue-300 px-2 py-1 rounded">
                        📊 {item.percentages.join(', ')}%
                      </div>
                    )}
                    {item.amounts && item.amounts.length > 0 && (
                      <div className="text-xs bg-green-900/30 text-green-300 px-2 py-1 rounded">
                        💰 {item.amounts.slice(0, 2).join(' / ')}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-xs text-slate-400 italic">No financial details extracted</p>
          )}
        </div>
      )
    }

    // Risk Analysis
    if (type === 'risk_analysis') {
      const risks = answer.risks_identified || {}
      return (
        <div className="space-y-2">
          <p className="text-sm font-semibold text-slate-200">Total Risks: {answer.total_risks}</p>
          {risks.high_risk && risks.high_risk.length > 0 && (
            <div className="p-2 bg-red-900/20 border border-red-700/50 rounded">
              <p className="text-xs text-red-300 font-semibold mb-1">🔴 High Risk ({risks.high_risk.length})</p>
              <p className="text-xs text-slate-300">{risks.high_risk[0].substring(0, 100)}...</p>
            </div>
          )}
          {risks.medium_risk && risks.medium_risk.length > 0 && (
            <div className="p-2 bg-yellow-900/20 border border-yellow-700/50 rounded">
              <p className="text-xs text-yellow-300 font-semibold mb-1">🟡 Medium Risk ({risks.medium_risk.length})</p>
              <p className="text-xs text-slate-300">{risks.medium_risk[0].substring(0, 100)}...</p>
            </div>
          )}
        </div>
      )
    }

    // Ambiguity Alert
    if (type === 'ambiguity_alert') {
      return (
        <div className="space-y-2">
          <div className="p-3 bg-orange-900/20 border border-orange-700/50 rounded-lg">
            <p className="text-sm text-orange-300 font-semibold">⚠️ Ambiguous Clauses Detected</p>
            <p className="text-xs text-orange-200 mt-2">{answer.recommendation}</p>
          </div>
          <div className="space-y-1">
            {answer.ambiguous_clauses.map((clause: string, idx: number) => (
              <p key={idx} className="text-xs text-slate-300 pl-3 border-l-2 border-orange-700">
                {clause.substring(0, 100)}...
              </p>
            ))}
          </div>
        </div>
      )
    }

    // Default
    return (
      <div className="text-xs text-slate-300">
        <p className="font-semibold mb-2">Answer Type: {type}</p>
        <p>{JSON.stringify(answer, null, 2)}</p>
      </div>
    )
  }

  return (
    <div className="card p-4 mb-6 border-l-4 border-cyan-500">
      <p className="text-sm font-semibold text-slate-200 mb-3">📊 Structured Analysis</p>
      {renderContent()}
    </div>
  )
}
