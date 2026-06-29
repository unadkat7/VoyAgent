# 🚀 VoyAgent

> **Your AI-Powered Travel Concierge**

VoyAgent is a full-stack AI-powered travel planning platform that helps users create personalized travel itineraries using AI. Users simply describe their travel plans in natural language, and VoyAgent generates a complete itinerary including budget estimation, day-wise plans, packing suggestions, and travel tips.

The project is designed with a scalable architecture using **Next.js**, **Express.js**, and a dedicated **FastAPI AI service** powered by **LangGraph** and **LangChain**.

---

## ✨ Features

- 🔐 Secure JWT Authentication
- 👤 User Dashboard
- ✍️ Natural Language Trip Planning
- 🤖 AI-Powered Itinerary Generation
- 📅 Day-wise Travel Plan
- 💰 Budget Estimation
- 🎒 Packing Recommendations
- 💡 Travel Tips
- 🗂 Save & View Trip History

---

## 🏗️ System Architecture

```text
                 Next.js Frontend
                        │
                        ▼
              Express.js Backend
                        │
            REST API Communication
                        │
                        ▼
             FastAPI AI Microservice
                        │
          LangGraph + LangChain
                        │
                        ▼
                 Gemini API
```

---

## 🛠️ Tech Stack

### Frontend

- Next.js
- React
- Tailwind CSS

### Backend

- Node.js
- Express.js
- MongoDB Atlas
- Mongoose
- JWT Authentication

### AI Service

- Python
- FastAPI
- LangGraph
- LangChain
- Google Gemini API

### DevOps

- Docker
- Docker Compose
- GitHub Actions

### AgentOps

- LangSmith

---

## 📂 Project Structure

```text
voyagent/
│
├── docs/
│
├── frontend/
│
├── backend/
│
├── ai-service/
│
├── .gitignore
├── README.md
├── LICENSE
└── docker-compose.yml
```

---

## 🚧 Project Status

VoyAgent is currently under active development.

The project is being built incrementally with a focus on clean architecture, scalability, and production-ready engineering practices.

---

## 🤝 Contributing

Contributions, suggestions, and feedback are always welcome.

Feel free to fork the repository, open an issue, or submit a pull request.

---
