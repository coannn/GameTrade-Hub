import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './component/App';
import 'bootstrap/dist/css/bootstrap.min.css';
import { AuthProvider } from "./authentication/AuthContext";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </React.StrictMode>
);

