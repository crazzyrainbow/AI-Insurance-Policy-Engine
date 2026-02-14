import { useState } from 'react'
import QueryGuide from './QueryGuide'

interface QuestionFormProps {
  onSubmit: (question: string) => Promise<void>
  isLoading: boolean
  policyUploaded: boolean
}

export default function QuestionForm({ onSubmit, isLoading, policyUploaded }: QuestionFormProps) {
  const [question, setQuestion] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (question.trim()) {
      await onSubmit(question)
      setQuestion('')
    }
  }

  const handleSelectExample = (example: string) => {
    setQuestion(example)
  }

  return (
    <>
      {policyUploaded && <QueryGuide onSelectExample={handleSelectExample} />}
      
      <form onSubmit={handleSubmit} className="card p-8 mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-white">Ask a Question</h2>
          {isLoading && (
            <div className="flex items-center gap-2">
              <div className="animate-spin">
                <svg className="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <span className="text-sm text-blue-300">Analyzing...</span>
            </div>
          )}
        </div>
        
        {isLoading && (
          <div className="mb-4 p-3 bg-blue-900/20 border border-blue-700/50 rounded-lg">
            <div className="flex items-center gap-2 text-xs text-blue-300">
              <div className="flex gap-1">
                <div className="w-1 h-3 bg-blue-400 rounded-full animate-pulse"></div>
                <div className="w-1 h-3 bg-blue-400 rounded-full animate-pulse delay-100"></div>
                <div className="w-1 h-3 bg-blue-400 rounded-full animate-pulse delay-200"></div>
              </div>
              <span>Processing your question...</span>
            </div>
          </div>
        )}
        
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder={policyUploaded ? "Ask about coverage, exclusions, limits..." : "Upload a policy first..."}
          disabled={!policyUploaded || isLoading}
          className="w-full h-24 bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        />
        
        <button
          type="submit"
          disabled={!policyUploaded || isLoading || !question.trim()}
          className="btn-primary mt-4 w-full disabled:opacity-50 relative overflow-hidden"
        >
          {isLoading ? (
            <span className="flex items-center justify-center gap-2">
              <span className="inline-block w-2 h-2 bg-current rounded-full animate-pulse"></span>
              Analyzing Policy...
            </span>
          ) : (
            'Analyze Policy'
          )}
        </button>
      </form>
    </>
  )
}
