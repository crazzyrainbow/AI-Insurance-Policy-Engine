import { useState } from 'react'
import Header from './components/Header'
import UploadPolicy from './components/UploadPolicy'
import QuestionForm from './components/QuestionForm'
import QueryMetadata from './components/QueryMetadata'
import UserFriendlyAnswerDisplay from './components/UserFriendlyAnswerDisplay'
import VerdictCard from './components/VerdictCard'
import AnalysisAccordion from './components/AnalysisAccordion'
import DecisionTraceChart from './components/DecisionTraceChart'
import EvidenceList from './components/EvidenceList'
import SkeletonLoader from './components/SkeletonLoader'
import { askQuestion, PolicyDecisionResponse } from './services/api'
import './index.css'

function App() {
  const [policyUploaded, setPolicyUploaded] = useState(false)
  const [response, setResponse] = useState<PolicyDecisionResponse | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleUploadSuccess = () => {
    setPolicyUploaded(true)
    setResponse(null)
    setError(null)
  }

  const handleSubmit = async (question: string) => {
    if (!policyUploaded) {
      setError('Please upload a policy first')
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      const result = await askQuestion(question)
      setResponse(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to analyze question')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950">
      <Header />

      <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
        <UploadPolicy onUploadSuccess={handleUploadSuccess} isLoading={isLoading} />
        <QuestionForm onSubmit={handleSubmit} isLoading={isLoading} policyUploaded={policyUploaded} />

        {error && !response && !isLoading && (
          <div className="card border-red-700 bg-red-900/20 p-4 mb-8">
            <p className="text-sm text-red-300">{error}</p>
          </div>
        )}

        {isLoading && (
          <SkeletonLoader />
        )}

        {response && !isLoading && (
          <>
            {response.classification_metadata && (
              <QueryMetadata response={response} />
            )}

            {response.important_note && (
              <div className="card bg-blue-900/20 border-l-4 border-blue-500 p-4 mb-6">
                <p className="text-sm text-blue-300">💡 {response.important_note}</p>
              </div>
            )}

            {response.analysis.structured_answer && (
              <UserFriendlyAnswerDisplay answer={response.analysis.structured_answer} />
            )}

            <VerdictCard analysis={response.analysis} confidence={response.confidence} />

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
              <div className="lg:col-span-2">
                <AnalysisAccordion
                  coverage={response.analysis.coverage}
                  exclusions={response.analysis.exclusions}
                  limits={response.analysis.limits}
                  conditions={response.analysis.conditions}
                />
              </div>

              <div>
                <DecisionTraceChart decisionTrace={response.decision_trace} />
              </div>
            </div>

            <EvidenceList evidence={response.evidence} />
          </>
        )}
      </main>
    </div>
  )
}

export default App
