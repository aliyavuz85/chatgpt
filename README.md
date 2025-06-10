# chatgpt

This repo contains a minimal chat application with a React frontend and an Express backend using Socket.IO.

## Getting Started

Both servers require Node.js installed. Run the following commands from the project root to install dependencies and start each service.

### Backend

```bash
cd backend
npm install
npm start
```

The backend runs on port `3001` and exposes a `/login` endpoint for authentication and a WebSocket endpoint for chat messages.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend starts Vite's dev server on port `5173`. It provides a login form and, after a successful login, a basic real-time chat interface.

Make sure the backend is running before starting the frontend so the login and WebSocket connections can succeed.
