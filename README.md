# 🎯 CareerPilot — AI-Based Career Guidance System

CareerPilot is a web-based intelligent system designed to help users — especially students and job seekers — identify the best career paths based on their skills, CVs, and quiz responses.  
It combines **AI analysis**, **career recommendation**, and **skill evaluation** to guide users toward suitable job roles and development opportunities.

---

## 🚀 Features

- **AI-Powered Career Analysis**  
  Analyzes CV content and quiz answers using AI to generate personalized career recommendations.

- **Automatic Skill Extraction**  
  Extracts key strengths and identifies skills the user should learn next.

- **Personalized Job Suggestions**  
  Suggests companies and roles that best fit the user’s profile.

- **Data Visualization**  
  Displays results through interactive **Chart.js** visualizations (Radar & Doughnut charts).

- **User Authentication System**  
  Includes login, registration, and password management (with hashed passwords via bcrypt).

- **Responsive UI**  
  Built with **Tailwind CSS** for a clean and fully responsive interface.

- **Django-Based Backend**  
  Handles user data, result storage, and AI communication through Django models and views.

---

## 🧠 How It Works

1. The user uploads a **CV** or completes a **career quiz**.
2. The system analyzes their responses using an AI model.
3. It generates:
   - Career recommendations
   - Key strengths
   - Recommended skills to learn
   - Personality insights
4. Results are displayed in a clear, visual, and interactive dashboard.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | HTML5, Tailwind CSS, JavaScript, Chart.js |
| **Backend** | Django (Python) |
| **Database** | MySQL |
| **AI Integration** | Custom AI analysis module |
| **Authentication** | Django Sessions + bcrypt password hashing |

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/CareerPilot.git
   cd CareerPilot
