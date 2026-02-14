#!/bin/bash
# Startup script to pre-initialize backend

echo "🚀 Starting AI Insurance Policy Engine..."
echo ""

# Start backend
echo "⚙️ Starting backend (port 8888)..."
cd /Users/ankit/ai-insurance
/Users/ankit/ai-insurance/.venv/bin/python -m uvicorn app.main:app --reload --port 8888 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "✓ Backend PID: $BACKEND_PID"

# Wait for backend to start
sleep 3

# Pre-warm embeddings
echo "🔥 Pre-warming embedding model..."
/Users/ankit/ai-insurance/.venv/bin/python << 'PYWARM' > /dev/null 2>&1
import sys
sys.path.insert(0, '/Users/ankit/ai-insurance')
try:
    from app.infrastructure.embeddings import generate_embedding
    # Warm up the model by generating one embedding
    _ = generate_embedding("test")
    print("✓ Embeddings ready")
except Exception as e:
    print(f"✗ Embedding warm-up failed: {e}")
PYWARM

# Start frontend
echo "🎨 Starting frontend (port 3000)..."
cd /Users/ankit/ai-insurance/frontend
npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✓ Frontend PID: $FRONTEND_PID"

sleep 2

echo ""
echo "════════════════════════════════════════════"
echo "✅ AI Insurance Policy Engine Ready!"
echo "════════════════════════════════════════════"
echo ""
echo "Frontend:  http://localhost:3000"
echo "Backend:   http://localhost:8888"
echo ""
echo "Logs:"
echo "  Backend:  tail -f /tmp/backend.log"
echo "  Frontend: tail -f /tmp/frontend.log"
echo ""
echo "To stop: kill $BACKEND_PID $FRONTEND_PID"
echo ""

wait
