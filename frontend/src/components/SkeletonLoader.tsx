export default function SkeletonLoader() {
  return (
    <div className="space-y-6 animate-pulse">
      {/* Query Metadata Skeleton */}
      <div className="card p-4 mb-6 border-l-4 border-blue-500">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <div className="h-4 bg-slate-700 rounded w-24 mb-2"></div>
            <div className="h-6 bg-slate-700 rounded w-32"></div>
          </div>
          <div>
            <div className="h-4 bg-slate-700 rounded w-24 mb-2"></div>
            <div className="h-6 bg-slate-700 rounded w-40"></div>
          </div>
          <div>
            <div className="h-4 bg-slate-700 rounded w-32 mb-2"></div>
            <div className="h-6 bg-slate-700 rounded w-16"></div>
          </div>
        </div>
      </div>

      {/* Structured Answer Skeleton */}
      <div className="card p-4 mb-6 border-l-4 border-cyan-500">
        <div className="h-6 bg-slate-700 rounded w-48 mb-4"></div>
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="p-3 bg-slate-800/50 rounded-lg">
              <div className="h-4 bg-slate-700 rounded w-full mb-2"></div>
              <div className="h-4 bg-slate-700 rounded w-3/4 mb-3"></div>
              <div className="flex gap-2">
                <div className="h-6 bg-slate-700 rounded-full w-20"></div>
                <div className="h-6 bg-slate-700 rounded-full w-24"></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Verdict Card Skeleton */}
      <div className="card p-6 mb-8 border-l-4 border-green-500">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <div className="h-4 bg-slate-700 rounded w-20 mb-2"></div>
            <div className="h-10 bg-slate-700 rounded w-32"></div>
          </div>
          <div>
            <div className="h-4 bg-slate-700 rounded w-24 mb-2"></div>
            <div className="h-2 bg-slate-700 rounded w-full"></div>
          </div>
        </div>
      </div>

      {/* Evidence List Skeleton */}
      <div className="card p-4">
        <div className="h-6 bg-slate-700 rounded w-40 mb-4"></div>
        <div className="space-y-2">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-12 bg-slate-700/50 rounded"></div>
          ))}
        </div>
      </div>
    </div>
  )
}
