# BioSync AI
BioSync AI is an AI‑based academic web project designed to analyze user lifestyle data and generate wellness insights and predictions. The project demonstrates integration of a machine learning model with a web interface for educational purposes.
---
## 🚀 Features
* Collects user lifestyle inputs
* Sends data to ML prediction module
* Displays analysis results and insights
* Simple dashboard view of outputs
* Clean responsive interface
* REST API communication between frontend and backend
---
## 🧠 Tech Stack
### Frontend
* React.js
* HTML5 / CSS3 / JavaScript
* Axios
### Backend
* Node.js
* Express.js
### Machine Learning Module
* Python
* Flask API (local communication only)
### Database
* JSON / Local storage (for academic testing)
---
## 📂 Project Structure
```
BioSync-AI/
│
├── frontend/        # React UI
├── backend/         # Express API
├── ml-model/        # Python prediction model
├── public/
├── package.json
└── README.md
```
## ⚙️ Installation & Setup (Local Only)
### 1. Clone Repository
```
git clone https://github.com/yourusername/biosync-ai.git
cd biosync-ai
```
### 2. Run Backend
```
cd backend
npm install
npm start
```
### 3. Run Frontend
```
cd frontend
npm install
npm start
```
### 4. Run ML Model
```
cd ml-model
pip install -r requirements.txt
python app.py
```
> This project is intended to run locally for demonstration and academic evaluation. No hosting or mobile application is included.
---
## 📊 API Endpoints
| Method | Endpoint | Description                |
| ------ | -------- | -------------------------- |
| POST   | /predict | Send user data to ML model |
| POST   | /user    | Store user input           |
| GET    | /result  | Retrieve prediction result |
---
## 🎓 Academic Purpose
This project was developed as a Computer Science mini/major project to demonstrate:
* Full‑stack development
* API communication
* Machine learning integration in web applications
---
## 👨‍💻 Author
**Jaya Ramalingam**
Computer Science Engineering Student
For academic and learning purposes only.
