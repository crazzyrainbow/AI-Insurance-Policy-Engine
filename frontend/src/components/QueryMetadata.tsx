import { PolicyDecisionResponse } from '../services/api'

interface QueryMetadataProps {
  response: PolicyDecisionResponse
}

export default function QueryMetadata({ response }: QueryMetadataProps) {
  const metadata = response.classification_metadata
  if (!metadata) return null

  const categoryLabels: Record<string, string> = {
    coverage_check: '📋 Coverage Check',
    eligibility: '✅ Eligibility',
    exclusions: '🚫 Exclusions',
    limits: '💰 Limits',
    deductible: '💵 Deductible',
    copay: '💳 Co-pay',
    conditions: '⚠️ Conditions',
    requirements: '📄 Requirements',
    claim_process: '📝 Claim Process',
    network: '🏥 Network',
    pre_auth: '🔐 Pre-Authorization',
    waiting_period: '⏱️ Waiting Period',
    obligations: '📋 Obligations',
    gaps: '⚠️ Coverage Gaps',
    ambiguity: '❓ Ambiguity',
    risk_assessment: '🛡️ Risk Assessment',
  }

  const usecaseLabels: Record<string, string> = {
    hospital_tpa: '🏥 Hospital/TPA',
    employer: '🏢 Employer',
    bank: '🏦 Financial Institution',
    legal: '⚖️ Legal',
    broker: '🔍 Broker',
    family: '👨‍👩‍👧 Family',
    vendor: '🛍️ Vendor',
    due_diligence: '💼 Due Diligence',
    auditor: '📊 Auditor',
    data_protection: '🔐 Data Protection',
  }

  const categoryLabel = categoryLabels[metadata.category] || metadata.category
  const usecaseLabel = usecaseLabels[metadata.use_case] || metadata.use_case

  return (
    <div className="card p-4 mb-6 border-l-4 border-blue-500">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <p className="text-xs text-slate-400 uppercase tracking-wide mb-1">Query Type</p>
          <p className="text-sm font-semibold text-slate-200">{categoryLabel}</p>
        </div>
        
        <div>
          <p className="text-xs text-slate-400 uppercase tracking-wide mb-1">Use Case</p>
          <p className="text-sm font-semibold text-slate-200">{usecaseLabel}</p>
        </div>
        
        <div>
          <p className="text-xs text-slate-400 uppercase tracking-wide mb-1">Classification Confidence</p>
          <div className="flex items-center gap-2">
            <div className="flex-1 h-2 bg-slate-700 rounded-full overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-blue-500 to-cyan-500 transition-all"
                style={{ width: `${metadata.confidence * 100}%` }}
              />
            </div>
            <span className="text-sm font-mono text-slate-300">{(metadata.confidence * 100).toFixed(0)}%</span>
          </div>
        </div>
      </div>

      {metadata.focus_areas && metadata.focus_areas.length > 0 && (
        <div className="mt-4 pt-4 border-t border-slate-700">
          <p className="text-xs text-slate-400 uppercase tracking-wide mb-2">Search Focus Areas</p>
          <div className="flex flex-wrap gap-2">
            {metadata.focus_areas.slice(0, 6).map((area, idx) => (
              <span
                key={idx}
                className="px-3 py-1 text-xs rounded-full bg-blue-900/30 text-blue-300 border border-blue-700/50"
              >
                {area}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
