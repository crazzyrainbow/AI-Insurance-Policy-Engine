import { useState } from 'react'

interface UploadPolicyProps {
  onUploadSuccess: () => void
  isLoading: boolean
}

export default function UploadPolicy({ onUploadSuccess, isLoading }: UploadPolicyProps) {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    e.currentTarget.classList.add('bg-slate-800')
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.currentTarget.classList.remove('bg-slate-800')
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.currentTarget.classList.remove('bg-slate-800')
    
    const files = e.dataTransfer.files
    if (files.length > 0) {
      const pdfFile = files[0]
      if (pdfFile.type === 'application/pdf') {
        setFile(pdfFile)
        setError(null)
      } else {
        setError('Please select a PDF file')
      }
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files.length > 0) {
      const pdfFile = files[0]
      if (pdfFile.type === 'application/pdf') {
        setFile(pdfFile)
        setError(null)
      } else {
        setError('Please select a PDF file')
      }
    }
  }

  const handleUpload = async () => {
    if (!file) return

    setUploading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(`${(import.meta.env as any).VITE_API_URL}/upload-policy`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Upload failed')
      }

      onUploadSuccess()
      setFile(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="card p-8 mb-8">
      <h2 className="text-xl font-semibold text-white mb-4">Upload Policy Document</h2>
      
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className="border-2 border-dashed border-slate-700 rounded-lg p-8 text-center hover:border-slate-600 transition-colors"
      >
        <svg
          className="mx-auto h-12 w-12 text-slate-400 mb-2"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 4v16m8-8H4"
          />
        </svg>
        
        <p className="text-slate-300 mb-2">Drag and drop your PDF here</p>
        <p className="text-slate-500 text-sm mb-4">or</p>
        
        <label>
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileSelect}
            className="hidden"
            disabled={uploading}
          />
          <span className="btn-secondary cursor-pointer inline-block">
            Select File
          </span>
        </label>

        {file && (
          <div className="mt-4 p-3 bg-slate-800 rounded-lg">
            <p className="text-sm text-slate-300">
              <span className="font-medium">Selected:</span> {file.name}
            </p>
          </div>
        )}
      </div>

      {error && (
        <div className="mt-4 p-3 bg-red-900/20 border border-red-700 rounded-lg">
          <p className="text-sm text-red-300">{error}</p>
        </div>
      )}

      {file && (
        <button
          onClick={handleUpload}
          disabled={uploading || isLoading}
          className="btn-primary mt-4 w-full"
        >
          {uploading ? 'Uploading...' : 'Upload Policy'}
        </button>
      )}
    </div>
  )
}
