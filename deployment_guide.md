# 🚀 Personal AI Job Finder — Deployment & Usage Guide

Here are the best ways to deploy and use your **Personal AI Job Finder**:

---

## 💻 Option 1: 1-Click Local Desktop Use (Recommended for Daily Personal Use)

You can run the full system on your Windows laptop completely free without needing cloud servers or monthly fees.

### How to Launch:
1. Open the folder: `c:\Users\Venkata Sravani\Downloads\ai-job-finder`
2. Double-click **`start_job_finder.bat`**
3. It will automatically start your backend and frontend servers, and open **`http://localhost:3000`** in your web browser!

---

## ☁️ Option 2: Free Cloud Deployment (Access from Anywhere on Phone & Laptop)

If you want to access your AI Job Finder from your smartphone, tablet, or another computer anywhere in the world:

### Step 1: Deploy Frontend on Vercel (100% Free)
1. Push your project folder to your GitHub account (e.g. `https://github.com/your-username/ai-job-finder`).
2. Go to **[Vercel.com](https://vercel.com)** and log in with GitHub.
3. Click **"Add New Project"** ➔ Import `ai-job-finder`.
4. Set **Root Directory** to `frontend`.
5. Add Environment Variable:
   - `NEXT_PUBLIC_API_URL` = `https://your-backend-api-url.onrender.com/api/v1`
6. Click **Deploy**! (Your app will be live at `https://ai-job-finder.vercel.app`).

### Step 2: Deploy Backend on Render or Railway (Free Tier)
1. Go to **[Render.com](https://render.com)** ➔ Click **"New Web Service"**.
2. Connect your GitHub repository `ai-job-finder`.
3. Set **Root Directory** to `backend`.
4. Set **Environment**: Python 3.11+.
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. Add Environment Variables:
   - `GEMINI_API_KEY` (optional, for Gemini AI parsing)
   - `OPENAI_API_KEY` (optional, for OpenAI GPT-4o-mini parsing)
8. Click **Create Web Service**!

---

## 🐳 Option 3: Docker Container Deployment

If you have Docker Desktop installed:

```bash
cd "c:\Users\Venkata Sravani\Downloads\ai-job-finder"
docker compose up --build -d
```

Access your application at `http://localhost:3000`.

---

## 📊 Summary of What You Built

- 💼 **13 Active Job Collectors**: Ingests postings from Naukri, LinkedIn, Instahyre, Internshala, Wellfound, Foundit, Greenhouse, Lever, Ashby, RemoteOK, WeWorkRemotely, Indeed, and Glassdoor.
- 🎯 **Location & Remote Intelligence**: Auto-classifies Remote India, Remote Worldwide, and Indian tech hubs (Bangalore, Hyderabad, Pune, Chennai).
- 🧠 **Explainable AI Matching**: Weighted candidate matching algorithm evaluating skills, experience bounds, and role relevance.
- 📌 **Kanban Application CRM**: Pipeline tracking stage (`New` ➔ `Saved` ➔ `Applied` ➔ `Screening` ➔ `Interview` ➔ `Offer`).
