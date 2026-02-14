# 🎯 QUICK START GUIDE

## ✅ WHAT YOU NOW HAVE

A production-ready React + TypeScript frontend fully connected to your backend AI Policy Decision Engine.

---

## 🚀 START THE APPLICATION

### Option 1: Already Running

✅ **Frontend** - http://localhost:3000  
✅ **Backend** - http://localhost:8000

Just open http://localhost:3000 in your browser!

### Option 2: Start From Scratch

#### Terminal 1: Frontend
```bash
cd /Users/ankit/ai-insurance/frontend
npm run dev
```

#### Terminal 2: Backend
```bash
cd /Users/ankit/ai-insurance
/path/to/.venv/bin/python -m uvicorn app.main:app --reload --port 8000
```

---

## 📖 HOW TO USE

### Step 1: Upload a Policy
1. Go to http://localhost:3000
2. Either:
   - **Drag & drop** a PDF file onto the upload zone
   - **Click "Select File"** to choose from file picker
3. Click **"Upload Policy"** button
4. Wait for success message

### Step 2: Ask Questions
1. In the "Ask a Question" section, type your question
   - Examples:
     - "Is accidental damage covered?"
     - "What are the coverage limits?"
     - "Are pre-existing conditions excluded?"
2. Click **"Analyze Policy"** button
3. View the results:
   - **Verdict Card**: Shows if covered/limited/conditional/excluded
   - **Confidence Score**: 0-100% confidence in the analysis
   - **Coverage/Exclusions/Limits/Conditions**: Expandable sections
   - **Decision Breakdown**: Bar chart of analyzed clauses
   - **Evidence**: Supporting clauses with page numbers

---

## 📦 PROJECT FILES

### Frontend Location
```
/Users/ankit/ai-insurance/frontend/
```

### Key Files
- **`src/App.tsx`** - Main application
- **`src/components/`** - 7 React components
- **`src/services/api.ts`** - Backend integration
- **`package.json`** - Dependencies
- **`.env`** - API configuration
- **`index.html`** - HTML template

---

## 🔧 COMMANDS

### Development
```bash
cd frontend
npm run dev
```

### Build for Production
```bash
npm run build
npm run preview
```

### Install Dependencies
```bash
npm install
```

---

## 🎨 UI COMPONENTS

| Component | Purpose |
|-----------|---------|
| Header | App title and branding |
| UploadPolicy | PDF file upload with drag & drop |
| QuestionForm | Question input and submit |
| VerdictCard | Color-coded verdict with confidence |
| AnalysisAccordion | Coverage/Exclusions/Limits/Conditions |
| DecisionTraceChart | Bar chart visualization |
| EvidenceList | Supporting evidence citations |

---

## 🌐 API ENDPOINTS

Your frontend connects to:
- `POST /upload-policy` - Upload PDF
- `POST /ask` - Ask question about policy

---

## ✅ QUALITY ASSURANCE

- ✓ TypeScript strict mode
- ✓ No mock data
- ✓ Full error handling
- ✓ Loading states
- ✓ Responsive design
- ✓ Production-ready code

---

## 🎯 VERDICT COLORS

- 🟢 **Green** - Covered
- 🟡 **Yellow** - Limited
- 🔵 **Blue** - Conditional
- 🔴 **Red** - Excluded
- ⚪ **Gray** - Not Specified
- ⚫ **Dark Gray** - Out of Scope

---

## 🆘 NEED HELP?

### Frontend won't load?
```bash
cd frontend
rm -rf node_modules
npm install
npm run dev
```

### API errors?
1. Verify backend: http://localhost:8000
2. Check `.env` file has: `VITE_API_URL=http://localhost:8000`
3. Restart both frontend and backend

### Port 3000 in use?
```bash
npm run dev -- --port 3001
```

---

## 📱 RESPONSIVE DESIGN

Works on:
- ✓ Desktop (1024px+)
- ✓ Tablet (640px-1024px)
- ✓ Mobile (< 640px)

---

## 🚢 DEPLOY TO PRODUCTION

### Vercel (Easiest)
```bash
npm i -g vercel
vercel
```

### Netlify
```bash
npm i -g netlify-cli
netlify deploy --prod --dir=dist
```

### Your Own Server
```bash
npm run build
# Copy 'dist' folder to your server
```

---

## 📊 TECH STACK

- React 18
- TypeScript 5
- Vite 5
- TailwindCSS 3
- Axios
- Recharts

---

## 🎉 YOU'RE ALL SET!

Your AI Policy Decision Engine frontend is ready to use!

**Open**: http://localhost:3000

---

**Questions?** Check `frontend/README.md` for detailed documentation.
