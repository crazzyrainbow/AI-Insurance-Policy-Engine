# ⚡ QUICK REFERENCE CARD

## 🚀 START PROJECT IN 2 MINUTES

### Terminal 1: Backend
```bash
cd /Users/ankit/ai-insurance
/Users/ankit/ai-insurance/.venv/bin/python -m uvicorn app.main:app --reload --port 8888
```
✅ Backend running at: **http://localhost:8888**

### Terminal 2: Frontend
```bash
cd /Users/ankit/ai-insurance/frontend
npm run dev
```
✅ Frontend running at: **http://localhost:3000**

---

## 📍 KEY LINKS

| Resource | URL | Purpose |
|----------|-----|---------|
| Frontend App | http://localhost:3000 | Main UI |
| API Docs | http://localhost:8888/docs | Swagger UI |
| API Base | http://localhost:8888 | REST endpoints |

---

## 📝 API CALL EXAMPLE

```bash
curl -X POST http://localhost:8888/policy/qa \
  -H "Content-Type: application/json" \
  -d '{"question":"Is accidental damage covered?"}'
```

---

## 🎨 UI COMPONENTS

| Component | Purpose | File |
|-----------|---------|------|
| Header | Title & branding | `Header.tsx` |
| Form | Question input | `QuestionForm.tsx` |
| Verdict | Result display | `VerdictCard.tsx` |
| Accordion | Analysis sections | `AnalysisAccordion.tsx` |
| Chart | Visualization | `DecisionTraceChart.tsx` |
| Evidence | Citations | `EvidenceList.tsx` |

---

## 🎯 VERDICT COLORS

```
🟢 Covered      → Green
🟡 Limited      → Yellow
🔵 Conditional  → Blue
🔴 Excluded     → Red
⚪ Not Specified → Gray
⚫ Out of Scope  → Dark Gray
```

---

## 📦 INSTALL DEPENDENCIES

```bash
cd frontend
npm install
```

---

## 🏗️ BUILD FOR PRODUCTION

```bash
npm run build
# Creates dist/ folder ready to deploy
```

---

## 🔧 ENVIRONMENT FILE

**File**: `/Users/ankit/ai-insurance/frontend/.env.local`

```env
VITE_API_BASE_URL=http://localhost:8888
VITE_ENV=development
```

---

## 📂 PROJECT STRUCTURE

```
ai-insurance/
├── app/                    # Backend
│   ├── main.py
│   ├── api/routers/
│   ├── services/
│   └── infrastructure/
├── frontend/               # Frontend
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
└── DEPLOYMENT_GUIDE.md
```

---

## 🆘 TROUBLESHOOTING

### Port Already In Use
```bash
# Check what's using port 3000/8888
lsof -i :3000
# Kill process if needed
kill -9 <PID>
```

### API Connection Error
- Verify backend running: `curl http://localhost:8888/`
- Check `.env.local` has correct URL
- Ensure CORS enabled on backend

### Missing Dependencies
```bash
rm -rf node_modules package-lock.json
npm install
```

### TypeScript Errors
```bash
npx tsc --noEmit
```

---

## ✅ QUICK CHECKLIST

- [ ] Backend running on 8888
- [ ] Frontend running on 3000
- [ ] Can access http://localhost:3000
- [ ] `.env.local` configured
- [ ] Dependencies installed (`npm install`)
- [ ] API responding (`curl http://localhost:8888/`)

---

## 📊 TECH STACK SUMMARY

| Layer | Technology | Version |
|-------|-----------|---------|
| UI Framework | React | 18.2 |
| Language | TypeScript | 5.2 |
| Build Tool | Vite | 5.0 |
| Styling | TailwindCSS | 3.3 |
| HTTP Client | Axios | 1.6 |
| Charts | Recharts | 2.10 |

---

## 🎓 FILE LOCATIONS

| Documentation | Path |
|---------------|------|
| Setup Guide | `frontend/SETUP.md` |
| README | `frontend/README.md` |
| API Services | `frontend/src/services/api.ts` |
| Main Component | `frontend/src/App.tsx` |
| Deployment Guide | `DEPLOYMENT_GUIDE.md` |
| Implementation | `IMPLEMENTATION_SUMMARY.md` |

---

## 🚀 DEPLOYMENT

### Vercel
```bash
npm i -g vercel
cd frontend
vercel
```

### Netlify
```bash
npm i -g netlify-cli
cd frontend
netlify deploy --prod --dir=dist
```

---

## 💡 TIPS

- Use React DevTools browser extension for debugging
- Check Network tab for API calls
- Use TailwindCSS IntelliSense VS Code extension
- Hot reload active - changes reflect instantly
- API responses fully typed in TypeScript

---

## 📞 SUPPORT

1. Check `SETUP.md` for common issues
2. Review component source in `src/components/`
3. Check API in `src/services/api.ts`
4. Read `DEPLOYMENT_GUIDE.md` for production

---

**Everything you need to run the complete AI Insurance Policy Decision Engine!** 🎉

Status: ✅ READY TO USE
