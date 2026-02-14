import axios from 'axios'

export interface Evidence {
  clause: string
  page?: number
  source?: string
}

export interface Source {
  source: string
  page: number
}

export interface DecisionTrace {
  mode?: string
  reason?: string
  top_similarity?: number
  coverage_clauses: number
  limit_clauses: number
  condition_clauses: number
  exclusion_clauses: number
  parsed_clauses?: number
  classification_confidence?: number
}

export interface StructuredAnswer {
  answer_type: string
  [key: string]: any
}

export interface Analysis {
  verdict: 'covered' | 'limited' | 'conditional' | 'excluded' | 'not_specified' | 'out_of_scope'
  coverage: string[]
  exclusions: string[]
  limits: string[]
  conditions: string[]
  summary_view?: {
    what_is_covered: string[]
    key_limits: string[]
    important_conditions: string[]
    major_exclusions: string[]
  }
  structured_answer?: StructuredAnswer
}

export interface ClassificationMetadata {
  category: string
  use_case: string
  confidence: number
  focus_areas?: string[]
}

export interface PolicyDecisionResponse {
  session_id: string
  question: string
  query_category?: string
  use_case?: string
  analysis: Analysis
  confidence: number
  decision_trace: DecisionTrace
  evidence: Evidence[]
  sources: Source[]
  classification_metadata?: ClassificationMetadata
  important_note?: string
}

const API_URL = (import.meta.env as any).VITE_API_URL || 'http://localhost:8888'

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
})

export const uploadPolicy = async (file: File): Promise<{ message: string }> => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await apiClient.post('/upload-policy', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    timeout: 60000, // 60 second timeout for upload
  })
  return response.data
}

export const askQuestion = async (question: string): Promise<PolicyDecisionResponse> => {
  const response = await apiClient.post('/ask', { question }, {
    timeout: 30000, // 30 second timeout
  })
  return response.data
}

export default apiClient
