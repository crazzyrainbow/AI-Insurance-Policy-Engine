import { StructuredAnswer } from '../services/api'

interface UserFriendlyAnswerProps {
  answer: StructuredAnswer
}

export default function UserFriendlyAnswerDisplay({ answer }: UserFriendlyAnswerProps) {
  if (!answer) return null

  const type = answer.answer_type

  // Coverage Check - Simple Yes/No with next steps
  if (type === 'coverage_check') {
    const isGreen = answer.is_covered
    const bgColor = isGreen ? 'bg-green-900/20 border-green-700/50' : 'bg-red-900/20 border-red-700/50'
    const textColor = isGreen ? 'text-green-300' : 'text-red-300'
    const icon = isGreen ? '✅' : '❌'

    return (
      <div className="card p-4 mb-6 border-l-4 border-cyan-500">
        <p className="text-sm font-semibold text-slate-200 mb-4">📊 Your Question Answered</p>
        
        <div className={`p-4 rounded-lg border ${bgColor} mb-4`}>
          <p className={`text-lg font-bold ${textColor}`}>
            {icon} {answer.verdict}
          </p>
        </div>

        {answer.key_points && answer.key_points.length > 0 && (
          <div className="mb-4">
            <p className="text-xs text-slate-400 font-semibold mb-2">Why?</p>
            <ul className="space-y-1">
              {answer.key_points.map((point: string, idx: number) => (
                <li key={idx} className="text-xs text-slate-300 pl-3 border-l-2 border-cyan-700">
                  • {point}
                </li>
              ))}
            </ul>
          </div>
        )}

        {answer.next_step && (
          <div className="p-3 bg-slate-800/50 rounded border border-slate-700 text-xs text-slate-300 italic">
            💡 Next Step: {answer.next_step}
          </div>
        )}
      </div>
    )
  }

  // Limits - Clean table-like display
  if (type === 'limits') {
    return (
      <div className="card p-4 mb-6 border-l-4 border-yellow-500">
        <p className="text-sm font-semibold text-slate-200 mb-3">📋 Policy Limits Found</p>
        
        {answer.message && (
          <p className="text-xs text-slate-400 mb-3 italic">{answer.message}</p>
        )}

        {answer.limits_breakdown && answer.limits_breakdown.length > 0 ? (
          <div className="space-y-2">
            {answer.limits_breakdown.map((limit: any, idx: number) => (
              <div key={idx} className="p-3 bg-slate-800/30 rounded border border-slate-700/50">
                <p className="text-xs text-slate-300 mb-2">{limit.description}</p>
                <div className="flex flex-wrap gap-2">
                  {limit.percentage && (
                    <span className="text-xs px-2 py-1 rounded bg-blue-900/40 text-blue-300">
                      📊 {limit.percentage}%
                    </span>
                  )}
                  {limit.amount && (
                    <span className="text-xs px-2 py-1 rounded bg-green-900/40 text-green-300">
                      💰 {limit.amount}
                    </span>
                  )}
                  {limit.duration && (
                    <span className="text-xs px-2 py-1 rounded bg-purple-900/40 text-purple-300">
                      ⏱️ {limit.duration}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-400">No specific limits extracted</p>
        )}
      </div>
    )
  }

  // Exclusions - Red warning style
  if (type === 'exclusions') {
    return (
      <div className="card p-4 mb-6 border-l-4 border-red-500">
        <p className="text-sm font-semibold text-slate-200 mb-3">⚠️ NOT COVERED</p>
        
        <div className="bg-red-900/20 border border-red-700/50 p-3 rounded mb-3">
          <p className="text-xs text-red-300 font-semibold">{answer.warning}</p>
        </div>

        {answer.excluded_items && answer.excluded_items.length > 0 ? (
          <div className="space-y-2">
            {answer.excluded_items.map((item: string, idx: number) => (
              <div key={idx} className="p-2 bg-slate-800/50 rounded text-xs text-slate-300 border-l-2 border-red-700">
                • {item}
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-400">No exclusions found</p>
        )}

        {answer.recommendation && (
          <p className="text-xs text-yellow-300 mt-3 italic">💡 {answer.recommendation}</p>
        )}
      </div>
    )
  }

  // Requirements - Organized checklist
  if (type === 'requirements') {
    return (
      <div className="card p-4 mb-6 border-l-4 border-blue-500">
        <p className="text-sm font-semibold text-slate-200 mb-3">📝 Requirements Checklist</p>
        
        {answer.required_documents && answer.required_documents.length > 0 && (
          <div className="mb-3">
            <p className="text-xs text-blue-300 font-semibold mb-2">📄 Documents Needed:</p>
            <ul className="space-y-1 ml-2">
              {answer.required_documents.map((doc: string, idx: number) => (
                <li key={idx} className="text-xs text-slate-300">☐ {doc}</li>
              ))}
            </ul>
          </div>
        )}

        {answer.required_approvals && answer.required_approvals.length > 0 && (
          <div className="mb-3">
            <p className="text-xs text-green-300 font-semibold mb-2">✅ Approvals Needed:</p>
            <ul className="space-y-1 ml-2">
              {answer.required_approvals.map((approval: string, idx: number) => (
                <li key={idx} className="text-xs text-slate-300">☐ {approval}</li>
              ))}
            </ul>
          </div>
        )}

        {answer.required_notices && answer.required_notices.length > 0 && (
          <div className="mb-3">
            <p className="text-xs text-yellow-300 font-semibold mb-2">🔔 Notifications Required:</p>
            <ul className="space-y-1 ml-2">
              {answer.required_notices.map((notice: string, idx: number) => (
                <li key={idx} className="text-xs text-slate-300">☐ {notice}</li>
              ))}
            </ul>
          </div>
        )}

        {answer.other_requirements && answer.other_requirements.length > 0 && (
          <div>
            <p className="text-xs text-slate-400 font-semibold mb-2">📋 Other:</p>
            <ul className="space-y-1 ml-2">
              {answer.other_requirements.map((item: string, idx: number) => (
                <li key={idx} className="text-xs text-slate-300">☐ {item}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    )
  }

  // Conditions - Important info style
  if (type === 'conditions') {
    return (
      <div className="card p-4 mb-6 border-l-4 border-orange-500">
        <p className="text-sm font-semibold text-slate-200 mb-3">⚡ Important Conditions</p>
        
        {answer.warning && (
          <div className="bg-orange-900/20 border border-orange-700/50 p-3 rounded mb-3">
            <p className="text-xs text-orange-300 font-semibold">{answer.warning}</p>
          </div>
        )}

        {answer.conditions_list && answer.conditions_list.length > 0 ? (
          <div className="space-y-2">
            {answer.conditions_list.map((condition: string, idx: number) => (
              <div key={idx} className="p-2 bg-slate-800/50 rounded text-xs text-slate-300 border-l-2 border-orange-700">
                {idx + 1}. {condition}
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-400">No conditions found</p>
        )}
      </div>
    )
  }

  // Financial (Deductible, Copay, etc.)
  if (['deductible', 'copay', 'maximum_claim', 'reimbursement'].includes(type)) {
    const icons: Record<string, string> = {
      deductible: '💸',
      copay: '💳',
      maximum_claim: '💰',
      reimbursement: '💵'
    }
    const colors: Record<string, string> = {
      deductible: 'border-red-500 text-red-300',
      copay: 'border-yellow-500 text-yellow-300',
      maximum_claim: 'border-green-500 text-green-300',
      reimbursement: 'border-blue-500 text-blue-300'
    }
    const colorBg: Record<string, string> = {
      deductible: 'bg-red-900/20',
      copay: 'bg-yellow-900/20',
      maximum_claim: 'bg-green-900/20',
      reimbursement: 'bg-blue-900/20'
    }

    return (
      <div className={`card p-4 mb-6 border-l-4 ${colors[type] || 'border-cyan-500'}`}>
        <p className="text-sm font-semibold text-slate-200 mb-3">
          {icons[type] || '💡'} {type.replace('_', ' ').toUpperCase()}
        </p>

        {answer.message && (
          <p className="text-xs text-slate-400 mb-3 italic">{answer.message}</p>
        )}

        {answer.financial_details && answer.financial_details.length > 0 ? (
          <div className="space-y-2">
            {answer.financial_details.map((item: any, idx: number) => (
              <div key={idx} className={`p-3 rounded border border-slate-700/50 ${colorBg[type] || 'bg-slate-800/30'}`}>
                <p className="text-xs text-slate-300 mb-2">{item.description}</p>
                <div className="flex flex-wrap gap-2">
                  {item.percentage && (
                    <span className="text-xs px-2 py-1 rounded bg-blue-900/40 text-blue-300">
                      📊 {item.percentage}%
                    </span>
                  )}
                  {item.amount && (
                    <span className="text-xs px-2 py-1 rounded bg-green-900/40 text-green-300">
                      💰 {item.amount}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-400">No specific information found</p>
        )}
      </div>
    )
  }

  // Risk Analysis
  if (type === 'risk_analysis') {
    return (
      <div className="card p-4 mb-6 border-l-4 border-purple-500">
        <p className="text-sm font-semibold text-slate-200 mb-3">🎯 Risk Analysis</p>

        {answer.risks_identified && (
          <div className="space-y-2">
            {answer.risks_identified.high_risk && answer.risks_identified.high_risk.length > 0 && (
              <div className="p-3 bg-red-900/20 rounded border border-red-700/50">
                <p className="text-xs text-red-300 font-semibold mb-2">🔴 High Risk ({answer.risks_identified.high_risk.length})</p>
                <p className="text-xs text-slate-300">{answer.risks_identified.high_risk[0]}</p>
              </div>
            )}
            {answer.risks_identified.medium_risk && answer.risks_identified.medium_risk.length > 0 && (
              <div className="p-3 bg-yellow-900/20 rounded border border-yellow-700/50">
                <p className="text-xs text-yellow-300 font-semibold mb-2">🟡 Medium Risk ({answer.risks_identified.medium_risk.length})</p>
                <p className="text-xs text-slate-300">{answer.risks_identified.medium_risk[0]}</p>
              </div>
            )}
          </div>
        )}
      </div>
    )
  }

  // Ambiguity Alert
  if (type === 'ambiguity_alert') {
    return (
      <div className="card p-4 mb-6 border-l-4 border-orange-500">
        <p className="text-sm font-semibold text-slate-200 mb-3">⚠️ Ambiguous Clauses Detected</p>
        
        <div className="bg-orange-900/20 border border-orange-700/50 p-3 rounded mb-3">
          <p className="text-xs text-orange-300">{answer.recommendation}</p>
        </div>

        {answer.ambiguous_clauses && (
          <div className="space-y-2">
            {answer.ambiguous_clauses.slice(0, 5).map((clause: string, idx: number) => (
              <p key={idx} className="text-xs text-slate-300 pl-3 border-l-2 border-orange-700">
                {clause}
              </p>
            ))}
          </div>
        )}
      </div>
    )
  }

  // Fallback for unknown types
  return (
    <div className="card p-4 mb-6 bg-slate-800 rounded">
      <p className="text-sm font-semibold text-slate-200 mb-2">Answer</p>
      <p className="text-xs text-slate-400">Type: {type}</p>
    </div>
  )
}
