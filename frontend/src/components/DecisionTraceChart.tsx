import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { DecisionTrace } from '../services/api'

interface DecisionTraceChartProps {
  decisionTrace: DecisionTrace
}

export default function DecisionTraceChart({ decisionTrace }: DecisionTraceChartProps) {
  const data = [
    { name: 'Coverage', count: decisionTrace.coverage_clauses },
    { name: 'Limits', count: decisionTrace.limit_clauses },
    { name: 'Conditions', count: decisionTrace.condition_clauses },
    { name: 'Exclusions', count: decisionTrace.exclusion_clauses },
  ]

  const colors = ['#10b981', '#f59e0b', '#3b82f6', '#ef4444']

  return (
    <div className="card p-8">
      <h3 className="font-semibold text-white mb-6">Decision Breakdown</h3>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="name" stroke="#cbd5e1" />
          <YAxis stroke="#cbd5e1" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1e293b',
              border: '1px solid #334155',
              borderRadius: '8px',
            }}
          />
          <Bar dataKey="count" fill="#3b82f6" radius={[8, 8, 0, 0]}>
            {data.map((_entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[index]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
