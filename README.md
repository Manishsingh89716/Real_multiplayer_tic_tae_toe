# 🎮 Multiplayer Tic-Tac-Toe Game

A real-time **multiplayer Tic-Tac-Toe game** built using **FastAPI (Backend)** and **HTML, CSS, JavaScript (Frontend)**.  
This project is designed to be **mobile-friendly** and **deployable**, allowing players to compete in real-time using WebSocket communication.

---

## 🚀 Features

- 🎯 Real-time gameplay using **WebSockets**
- 👥 Multiplayer support (Player X and Player O)
- 📱 Mobile-friendly responsive design
- 🧩 Clear game info section (Current Player, You Play By, and Winner Info)
- ⚡ Lightweight — no frameworks needed for frontend
- 🗄️ FastAPI + SQLite backend for simplicity
- 🧠 Stateless gameplay handled by backend for synchronization

---

## 🏗️ Project Structure

- tic_tac_toe/
- ├── backend/
- │ ├── main.py #fastAPI app with REST and WebSocket endpoints
- │ └── requirements.txt 
- │
- ├── frontend/
- │ ├── index.html #main HTML page
- │ ├── style.css #styling for the game board
- │ └── script.js #frontend logic and WebSocket handling │
- └── README.md

--- 

## 🎨 Design Choices

| Component                   | Choice                           | Reason                                                    |
| --------------------------- | -------------------------------- | --------------------------------------------------------- |
| **Backend Framework**       | FastAPI                          | Lightweight, async WebSocket support, easy deployment     |
| **Database**                | SQLite                           | Minimal storage for testing and local sessions            |
| **Frontend**                | Vanilla HTML, CSS, JS            | Simplicity, zero dependencies, easy mobile responsiveness |
| **WebSocket Communication** | JSON-based events                | Keeps real-time updates clean and structured              |
| **Mobile Design**           | Responsive grid layout           | Works seamlessly on mobile browsers                       |
| **Architecture**            | Client-Server (WebSocket bridge) | Ensures both players stay synced via server messages      |


--- 

## 🧠 Game Architecture Overview
Player 1 (X)       Player 2 (O)
     ↓                   ↓
   ┌───────────────────────────┐
   │      WebSocket Server     │
   │ (FastAPI, async endpoint) │
   └───────────────────────────┘
              ↓
     Game State Logic
  (Board updates, winner checks)

--- 
## Flow:

- Players connect via WebSocket (/ws endpoint).

- Server assigns Player X and O automatically.

- Each move updates the shared board state.

- Server broadcasts updated state to both players.

- Once a winner or draw is detected → both clients display results.

--- 

## 📱 Responsive Design Example

- On mobile screens, the game grid adjusts to full width.

- Info panel displays:

- Current Player: X

- You Play By: O

- Info: Player X won!

---

## 🧩 Example Gameplay
## Action	Player X	Player O
- Start Game Connected	Connected
- X plays (1,1)	
- Move sent	
- Move received
- O plays (2,2)	
- Move sent	
- Move received
- X wins	
- Result shown	
- Result shown

--- 
## 🧑‍💻 Future Improvements

- Add player login and matchmaking

- Persistent game state with database

- Spectator mode

- Deploy on Render (backend) + Netlify (frontend)

---

## 💻 Tech Stack

- Backend: FastAPI, WebSocket, Uvicorn, SQLite

- Frontend: HTML, CSS, Vanilla JS

- Communication: JSON-based WebSocket protocol

---
## ⚡ Run Demo (Locally)
- Start backend: uvicorn main:app --reload

- Open frontend/index.html in two browser windows.

- Play real-time multiplayer Tic-Tac-Toe.
