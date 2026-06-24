# MockMate 🤖🎙️

MockMate is an AI-powered mock interview platform designed to help users prepare for technical interviews. The application generates topic-specific interview questions, provides an interactive interface for users to submit their answers, and delivers detailed performance reports—including strengths, weaknesses, actionable recommendations, and ideal answers—powered by the Gemini API.

---

## 🚀 Key Features

* **User Authentication**: Secure signup, login, and token-based authentication using JWT.
* **Customized Interview Setup**: Choose interview topics (e.g., SQL, Java) and difficulty levels to configure custom sessions.
* **Interactive Interview Sessions**: Experience a simulated interview environment answering structured technical questions.
* **AI-Powered Evaluation**: Get detailed, constructive critiques, lists of strengths, weaknesses, and improvement recommendations powered by the Gemini 2.5 Flash model.
* **Ideal Answers & Keywords**: Compare your responses against AI-suggested ideal answers and key concepts for each question.

---

## 🛠️ Tech Stack

### Backend
* **FastAPI**: Modern, high-performance web framework for building APIs with Python 3.8+.
* **SQLAlchemy**: SQL toolkit and Object-Relational Mapper (ORM) for database interactions.
* **PostgreSQL**: Relational database used for storing users, interviews, and feedback.
* **Gemini API (`google-generativeai`)**: Used for interview evaluation and recommendation generation.
* **Pydantic**: Data validation and settings management.

### Frontend
* **React + Vite**: A fast build tool and frontend framework for a smooth user experience.
* **Tailwind CSS**: A utility-first CSS framework for modern, responsive UI design.
* **Axios**: Promise-based HTTP client for interacting with the backend API.
* **React Router**: Client-side routing.

---

## 📦 Project Structure

```
MockMate/
├── backend/
│   ├── app/                # FastAPI application package
│   ├── .env.example        # Reference environment configuration for backend
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/                # React source code (pages, components, router, context)
│   ├── .env.example        # Reference environment configuration for frontend
│   ├── package.json        # Frontend configuration and scripts
│   └── vite.config.js      # Vite configuration
└── .gitignore              # Project-wide Git ignore rules
```

---

## ⚙️ Getting Started

### Prerequisites
* **Python** (v3.10 or higher recommended)
* **Node.js** (v18 or higher recommended) and **npm** or **pnpm**
* **PostgreSQL** instance running locally or on a cloud provider

---

### 1. Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # On Windows:
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Copy `.env.example` to a new file named `.env`:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and fill in your details:
   - `DATABASE_URL`: Your PostgreSQL connection string.
   - `GEMINI_API_KEY`: Your Google Gemini API Key.
   - `JWT_SECRET_KEY`: A secure random string for JWT signatures.

5. **Run the FastAPI development server**:
   ```bash
   uvicorn app.main:app --reload
   ```
   The backend API will run at `http://localhost:8000`. You can view the interactive documentation at `http://localhost:8000/docs`.

---

### 2. Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd ../frontend
   ```

2. **Install node packages**:
   ```bash
   # If using npm:
   npm install

   # If using pnpm:
   pnpm install
   ```

3. **Configure environment variables**:
   Copy `.env.example` to a new file named `.env`:
   ```bash
   cp .env.example .env
   ```
   Ensure the `VITE_API_BASE_URL` points to your backend instance (default: `http://localhost:8000/api`).

4. **Run the frontend dev server**:
   ```bash
   # If using npm:
   npm run dev

   # If using pnpm:
   pnpm run dev
   ```
   The frontend will run at `http://localhost:5173`. Open this URL in your browser to interact with MockMate!

