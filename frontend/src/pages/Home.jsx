import React from 'react';
import { Box, Typography, Button, Container, Grid, Paper, Stack } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { Login as LoginIcon, PersonAdd as RegisterIcon, VolumeUp as VolumeIcon, Brightness4 as DarkModeIcon, Brightness7 as LightModeIcon } from '@mui/icons-material';
import { useColorMode } from '../theme';
import { useTheme, IconButton } from '@mui/material';

export default function Home() {
  const navigate = useNavigate();
  const theme = useTheme();
  const colorMode = useColorMode();
  
  return (
    <Box sx={{ 
      minHeight: '100vh', 
      display: 'flex', 
      flexDirection: 'column',
      bgcolor: 'background.default'
    }}>
      {/* Navbar */}
      <Box sx={{ p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #e8e0d5' }}>
        <Typography variant="h5" fontWeight="bold" color="primary">
          VoQube
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <IconButton onClick={colorMode.toggleColorMode} sx={{ mr: 2 }} color="inherit">
            {theme.palette.mode === 'dark' ? <LightModeIcon /> : <DarkModeIcon />}
          </IconButton>
          <Button onClick={() => navigate('/login')} sx={{ mr: 2 }}>Login</Button>
          <Button variant="contained" onClick={() => navigate('/register')}>Sign Up</Button>
        </Box>
      </Box>

      {/* Hero Section */}
      <Container maxWidth="lg" sx={{ flexGrow: 1, display: 'flex', alignItems: 'center', py: 8 }}>
        <Grid container spacing={8} alignItems="center">
          <Grid item xs={12} md={6}>
            <Box sx={{ pr: { md: 4 } }}>
              <Typography variant="h1" gutterBottom sx={{ fontSize: { xs: '3rem', md: '4.5rem' } }}>
                The Voice of <span style={{ color: '#70826b' }}>Expression</span>
              </Typography>
              <Typography variant="h5" color="text.secondary" paragraph sx={{ mb: 4, lineHeight: 1.6 }}>
                Generate stunning, high-quality audio from text in seconds. Whether it's for 
                narrations, translations, or gaming, VoQube delivers professional multilingual TTS.
              </Typography>
              
              <Stack direction={{ xs: 'column', sm: 'row' }} spacing={3}>
                {/* User wants login feature on the left side button */}
                <Button 
                  variant="contained" 
                  size="large" 
                  startIcon={<LoginIcon />}
                  onClick={() => navigate('/login')}
                  sx={{ px: 4, py: 1.5, fontSize: '1.1rem' }}
                >
                  Join Now
                </Button>
                <Button 
                  variant="outlined" 
                  size="large" 
                  startIcon={<VolumeIcon />}
                  onClick={() => navigate('/login')} // Redirect to dashboard/login
                  sx={{ px: 4, py: 1.5, fontSize: '1.1rem' }}
                >
                  Try Demo
                </Button>
              </Stack>
            </Box>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Paper elevation={10} sx={{ 
              p: 4, 
              borderRadius: 4, 
              bgcolor: 'rgba(112, 130, 107, 0.05)',
              border: '2px solid rgba(112, 130, 107, 0.2)',
              position: 'relative',
              overflow: 'hidden'
            }}>
                <Box sx={{ position: 'relative', zIndex: 1 }}>
                    <Typography variant="h6" fontWeight="bold" gutterBottom>
                        Experience Premium TTS
                    </Typography>
                    <Box sx={{ 
                        height: 200, 
                        bgcolor: 'background.paper', 
                        borderRadius: 2, 
                        display: 'flex', 
                        alignItems: 'center', 
                        justifyContent: 'center',
                        border: '1px dashed #70826b'
                    }}>
                        <Typography color="text.secondary">
                            [ Voice Visualization Demo ]
                        </Typography>
                    </Box>
                </Box>
                {/* Decorative Elements */}
                <Box sx={{ 
                  position: 'absolute', 
                  top: -20, 
                  right: -20, 
                  width: 100, 
                  height: 100, 
                  borderRadius: '50%', 
                  bgcolor: 'primary.main', 
                  opacity: 0.1 
                }} />
            </Paper>
          </Grid>
        </Grid>
      </Container>

      {/* Footer */}
      <Box sx={{ p: 4, textAlign: 'center', bgcolor: 'rgba(47, 62, 70, 0.03)' }}>
        <Typography variant="body2" color="text.secondary">
          © 2026 VoQube. All Rights Reserved.
        </Typography>
      </Box>
    </Box>
  );
}
