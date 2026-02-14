# AI Insurance Policy Decision Engine - Frontend

Production-ready React + TypeScript frontend for the AI Policy Decision Engine.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+
- npm or yarn

### Installation

```bash
cd frontend
npm install
```

### Configuration

Create `.env` file:
```
VITE_API_URL=http://localhost:8000
```

### Development

```bash
npm run dev
```

Opens at **http://localhost:3000**

### Build

```bash
npm run build
npm run preview
```

## 📋 Features

- **PDF Upload**: Drag & drop or file picker to upload insurance policies
- **Question Analysis**: Ask questions about coverage, limits, exclusions
- **Verdict Display**: Color-coded verdicts with confidence scores
- **Analysis Breakdown**: Expandable sections for coverage, exclusions, limits, conditions
- **Decision Trace**: Bar chart visualizing decision analysis
- **Evidence Citations**: Scrollable list of supporting clauses with page numbers
- **Error Handling**: Graceful error messages and validation
- **Responsive Design**: Mobile-friendly layout

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── UploadPolicy.tsx
│   │   ├── QuestionForm.tsx
│   │   ├── VerdictCard.tsx
│   │   ├── AnalysisAccordion.tsx
│   │   ├── DecisionTraceChart.tsx
│   │   └── EvidenceList.tsx
│   ├── services/
│   │   └── api.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── index.html
├── package.json
├── vite.config.ts
├── tailwind.config.ts
├── tsconfig.json
└── postcss.config.js
```

## 🔌 API Integration

### Upload Policy
```bash
POST /upload-policy
Content-Type: multipart/form-data
Body: { file: File }
Response: { message: string }
```

### Ask Question
```bash
POST /ask
Content-Type: application/json
Body: { question: string }
Response: PolicyDecisionResponse
```

## 🎨 Color Scheme

- **Covered**: Green (#10b981)
- **Limited**: Yellow (#f59e0b)
- **Conditional**: Blue (#3b82f6)
- **Excluded**: Red (#ef4444)
- **Not Specified**: Gray (#6b7280)
- **Out of Scope**: Dark Gray (#4b5563)

## 📦 Dependencies

- React 18
- TypeScript 5
- Vite 5
- TailwindCSS 3
- Axios 1
- Recharts 2

## 🔧 Development

### Hot Module Replacement
Changes automatically reflect in browser

### TypeScript
Strict mode enabled for type safety

### Linting
Run TypeScript compiler: `tsc --noEmit`

## 🚢 Production Build

```bash
npm run build
```

Creates optimized `dist/` folder

## 📱 Responsive Breakpoints

- Mobile: < 640px
- Tablet: 640px - 1024px  
- Desktop: > 1024px

## ✅ Quality Checklist

- ✓ No console logs in production code
- ✓ No unused imports
- ✓ Full TypeScript coverage
- ✓ Error boundary handling
- ✓ Loading states for all async operations
- ✓ Disabled states for form controls
- ✓ Empty states for empty lists
- ✓ Responsive design tested

## 🆘 Troubleshooting

### Port 3000 Already In Use
```bash
npm run dev -- --port 3001
```

### API Connection Errors
- Verify backend running: `curl http://localhost:8000/`
- Check `.env` has correct `VITE_API_URL`
- Check browser console for CORS errors

### Build Errors
```bash
rm -rf node_modules
npm install
npm run build
```

## 📄 License

Proprietary - All rights reserved
