import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';

const socket = io('http://localhost:3001');

function Chat({ username }) {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    socket.on('chat message', (msg) => {
      setMessages((prev) => [...prev, msg]);
    });
    return () => socket.off('chat message');
  }, []);

  const sendMessage = () => {
    if (message.trim()) {
      const msg = { user: username, text: message };
      socket.emit('chat message', msg);
      setMessages((prev) => [...prev, msg]);
      setMessage('');
    }
  };

  return (
    <div>
      <div id="messages">
        {messages.map((m, i) => (
          <div key={i}><strong>{m.user}:</strong> {m.text}</div>
        ))}
      </div>
      <input value={message} onChange={e => setMessage(e.target.value)} placeholder="Message" />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);

  const login = async () => {
    const res = await fetch('http://localhost:3001/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
      credentials: 'include'
    });
    if (res.ok) setLoggedIn(true);
  };

  if (!loggedIn) {
    return (
      <div>
        <h1>Login</h1>
        <input placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
        <button onClick={login}>Login</button>
      </div>
    );
  }

  return <Chat username={username} />;
}
