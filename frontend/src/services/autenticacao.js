import React, { createContext, useContext, useEffect, useState } from 'react';
import axios from 'axios';

const AuthContext = createContext();

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'multipart/form-data',
  }
});

const AuthProvider = ({ children }) => {
  const [authenticated, setAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [message, setMessage] = useState("");

  const login = async (email, password) => {
    try {
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);

      const response = await api.post('/api-auth-token', formData);
      const { token } = response.data;
      localStorage.setItem('token', token);
      setAuthenticated(true);
      const userResponse = await api.get('/usuario');
      setUser(userResponse.data);
      setMessage("Login realizado com sucesso!");
    } catch (error) {
      setMessage("Ocorreu um erro ao fazer login. Verifique suas credenciais e tente novamente.");
      console.error(error);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setAuthenticated(false);
    setUser(null);
    window.location.reload();
  };

  // Add token to default headers of api instance
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      api.defaults.headers.common['Authorization'] = `Token ${token}`;
    } else {
      delete api.defaults.headers.common['Authorization'];
    }
  }, [authenticated]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    console.log(token)
    if (token) {
      setAuthenticated(true);
            axios.get('api/usuario', {
                headers: { Authorization: `Token ${token}` },
            })
                .then(response => setUser(response.data))
                .catch(error => {
                    console.error(error);
                });
        }
    }, []);

  return (
    <AuthContext.Provider value={{ authenticated, user, login, logout, message }}>
      {children}
    </AuthContext.Provider>
  );
};

const useAuth = () => useContext(AuthContext);

export { AuthProvider, useAuth, api };
