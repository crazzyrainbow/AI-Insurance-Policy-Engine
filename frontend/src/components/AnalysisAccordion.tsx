import { useState } from 'react'

interface AccordionItem {
  title: string
  items: string[]
}

interface AnalysisAccordionProps {
  coverage: string[]
  exclusions: string[]
  limits: string[]
  conditions: string[]
}

export default function AnalysisAccordion({
  coverage,
  exclusions,
  limits,
  conditions,
}: AnalysisAccordionProps) {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(0)

  const sections: AccordionItem[] = [
    { title: 'Coverage', items: coverage },
    { title: 'Exclusions', items: exclusions },
    { title: 'Limits', items: limits },
    { title: 'Conditions', items: conditions },
  ]

  return (
    <div className="space-y-3 mb-8">
      {sections.map((section, index) => (
        <div key={index} className="card border-slate-800">
          <button
            onClick={() => setExpandedIndex(expandedIndex === index ? null : index)}
            className="w-full text-left p-4 flex items-center justify-between hover:bg-slate-800/50 transition-colors"
          >
            <div className="flex items-center space-x-3">
              <span className="font-semibold text-white">{section.title}</span>
              <span className="text-xs font-medium text-slate-400 bg-slate-800 px-2 py-1 rounded">
                {section.items.length}
              </span>
            </div>
            <svg
              className={`h-5 w-5 text-slate-400 transition-transform ${
                expandedIndex === index ? 'rotate-180' : ''
              }`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
            </svg>
          </button>

          {expandedIndex === index && (
            <div className="border-t border-slate-800 p-4 bg-slate-800/50">
              {section.items.length === 0 ? (
                <p className="text-sm text-slate-500 italic">No items</p>
              ) : (
                <ul className="space-y-2">
                  {section.items.map((item, i) => (
                    <li key={i} className="flex items-start space-x-3 text-sm text-slate-300">
                      <span className="text-slate-600 mt-1">•</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
