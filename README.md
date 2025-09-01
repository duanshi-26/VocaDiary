# 🎙️ VocaDiary

> *“Your voice. Your mood. Your diary.”*

**VocaDiary** is a **voice-controlled mood tracker** powered by **Speech Recognition, NLP, and Data Visualization**.
It lets you **speak out your thoughts**, converts them into text, runs **sentiment analysis**, generates **summaries**, and stores your entries securely in **MongoDB**.

---

## ✨ Features

* 🗣 **Voice Input** → Record diary entries using **SpeechRecognition API**
* 🔤 **Speech-to-Text** → Convert spoken words into structured text
* 🧠 **Sentiment Analysis** → Detect mood polarity using **TextBlob**
* 📚 **Summarization** → Auto-generate concise summaries with **Sumy**
* 📊 **Mood Charts** → Visualize emotional trends over time (positive / neutral / negative)
* 🔒 **Secure Storage** → Entries encrypted & saved in **MongoDB**
* ⚡ **Modern Stack** → React frontend + FastAPI backend + Node.js services

---

## 🗂 Project Structure

```
VocaDiary/
├── frontend/                 # React frontend
│   ├── src/                  # Components, Pages, Services
│   └── package.json          # Frontend dependencies
├── main.py                   # FastAPI backend entrypoint
├── new.ipynb                 # Notebook for prototyping NLP pipeline
├── requirements.txt           # Python backend dependencies
└── README.md                  # This file
```

---

## 🧰 Tech Stack

* **Frontend**: React, Chart.js/Recharts for mood graphs
* **Backend**: FastAPI (Python) + Node.js microservices
* **Database**: MongoDB (with encryption for secure storage)
* **Speech & NLP**:

  * SpeechRecognition API
  * TextBlob (Sentiment Analysis)
  * Sumy (Text Summarization)
* **Other Tools**: Pandas, Matplotlib (for exploration & notebook work)

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/duanshi-26/VocaDiary.git
cd VocaDiary
```

### 2️⃣ Backend Setup (FastAPI + Python)

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

➡️ Runs backend at: `http://127.0.0.1:8000`

### 3️⃣ Frontend Setup (React + Node.js)

```bash
cd frontend
npm install
npm start
```

➡️ Runs frontend at: `http://localhost:3000`

---

## 🚀 How It Works

1. 🎙 Speak your diary entry
2. 🔤 SpeechRecognition API converts it to text
3. 🧠 NLP pipeline:

   * Sentiment analysis (**TextBlob**) → mood score
   * Summarization (**Sumy**) → short summary
4. 📊 Mood graph updates in real time (React frontend)
5. 🔒 Data stored securely in MongoDB with encryption

---

## 📊 Sample Output

* **User Entry**:

  > “Today I felt really anxious about my exams, but after some revision I felt more confident.”

* **Sentiment Analysis**:

  * Polarity: `0.35` → *Positive*
  * Subjectivity: `0.60`

* **Summary**:

  > “Felt anxious about exams, but improved after revision.”

* **Mood Chart**: <img src="docs/mood-chart.png" width="500"/>

---

## 🛠 Future Improvements
* 🧾 Add **daily/weekly reports** export (PDF/CSV)
* 🔔 Integrate reminders & mood streaks gamification

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/awesome-feature`
3. Commit changes: `git commit -m "Add awesome feature"`
4. Push: `git push origin feature/awesome-feature`
5. Open a Pull Request 🚀

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Maintainer

**Duanshi Chawla**
🌐 [GitHub](https://github.com/duanshi-26)
