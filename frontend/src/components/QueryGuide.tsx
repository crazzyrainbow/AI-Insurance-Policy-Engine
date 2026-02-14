import { useState } from 'react'

interface QueryGuideProps {
  onSelectExample: (question: string) => void
}

export default function QueryGuide({ onSelectExample }: QueryGuideProps) {
  const [expanded, setExpanded] = useState(false)

  const examples = {
    'Coverage & Eligibility': [
      'Is cancer treatment covered under this policy?',
      'Am I eligible for cashless treatment at any hospital?',
      'Does this policy cover maternity expenses?',
      'What treatments are excluded from coverage?',
    ],
    'Hospital/TPA Use': [
      'Can this patient avail cashless treatment at our network hospital?',
      'What is the maximum room rent eligibility?',
      'Is ICU covered fully or capped?',
      'Are pre-existing conditions declared and covered?',
    ],
    'Financial Details': [
      'What is the annual deductible?',
      'What are the copay amounts for specialist visits?',
      'What is the total claim limit for cancer treatment?',
      'How much will be reimbursed for outpatient services?',
    ],
    'Requirements & Process': [
      'What documents are mandatory for claim approval?',
      'Does the policy require pre-authorization?',
      'What is the claim filing deadline?',
      'Are consumables included or excluded?',
    ],
    'Legal & Compliance': [
      'What are the insured obligations for policy validity?',
      'Are there ambiguous clauses in this policy?',
      'Does this policy comply with regulatory requirements?',
      'What is the dispute resolution mechanism?',
    ],
    'Employer/Corporate': [
      'Are dependents included? Up to what age?',
      'Does coverage continue after employee resignation?',
      'What is the total liability exposure for the company?',
      'Are mental health treatments included?',
    ],
  }

  return (
    <div className="mb-8">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center justify-between w-full px-4 py-3 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors border border-slate-700"
      >
        <span className="font-semibold text-slate-200">📚 Query Examples & Guide</span>
        <span className="text-slate-400">{expanded ? '▼' : '▶'}</span>
      </button>

      {expanded && (
        <div className="mt-4 space-y-4">
          {Object.entries(examples).map(([category, questions]) => (
            <div key={category} className="card p-4">
              <h3 className="text-sm font-semibold text-slate-200 mb-3">{category}</h3>
              <div className="space-y-2">
                {questions.map((question, idx) => (
                  <button
                    key={idx}
                    onClick={() => onSelectExample(question)}
                    className="w-full text-left px-3 py-2 text-sm text-slate-300 hover:text-slate-100 hover:bg-slate-800 rounded transition-colors border border-slate-700/50 hover:border-slate-600"
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          ))}

          <div className="card bg-blue-900/20 border-blue-700/50 p-4">
            <h3 className="text-sm font-semibold text-blue-300 mb-2">💡 Tips for Better Results:</h3>
            <ul className="text-xs text-blue-200 space-y-1 ml-3">
              <li>• Be specific: "cancer treatment" is better than "treatment"</li>
              <li>• Ask one question at a time</li>
              <li>• Include relevant context: mention patient type, procedure name, etc.</li>
              <li>• The system will classify your query and provide targeted analysis</li>
              <li>• Use examples above as templates for your own questions</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}
