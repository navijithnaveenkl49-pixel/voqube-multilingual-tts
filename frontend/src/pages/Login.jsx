import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Container, Card, CardContent } from '@mui/material';
import { useAuth } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(username, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    }
  };

  return (
    <Container maxWidth="sm" sx={{ display: 'flex', flexDirection: 'column', height: '100vh', justifyContent: 'center' }}>
      <Card elevation={3} sx={{ mx: { xs: 2, sm: 0 } }}>
        <CardContent sx={{ p: { xs: 3, sm: 4 } }}>
          <Typography variant="h4" component="h1" gutterBottom align="center" fontWeight="bold" sx={{ fontSize: { xs: '1.75rem', sm: '2.125rem' } }}>
            VoQube
          </Typography>
          <Typography variant="subtitle1" gutterBottom align="center" color="text.secondary">
            Log in to your account
          </Typography>

          {error && <Typography color="error" align="center" sx={{ mt: 2 }}>{error}</Typography>}

          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
            <TextField
              fullWidth
              label="Username"
              variant="outlined"
              margin="normal"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <TextField
              fullWidth
              label="Password"
              type="password"
              variant="outlined"
              margin="normal"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
            <Typography align="center" variant="body2">
              Don't have an account? <Link to="/register" style={{ color: '#6366f1' }}>Sign Up</Link>
            </Typography>
          </Box>
        </CardContent>
      </Card>
    </Container>
  );
}
