import React, { useState } from 'react';
import { Box, Card, CardContent, Typography, TextField, Button, MenuItem, Select, FormControl, InputLabel, Grid, CircularProgress, Alert, Switch, FormControlLabel } from '@mui/material';
import { VolumeUp as VolumeUpIcon, Download as DownloadIcon, Star as StarIcon } from '@mui/icons-material';
import api, { SERVER_URL } from '../services/api';
import { useAuth } from '../context/AuthContext';

const languages = [
  'English', 'Hindi', 'Tamil', 'Malayalam', 'Telugu', 'Kannada', 'Bengali', 
  'Marathi', 'Gujarati', 'Punjabi', 'Urdu', 'Spanish', 'French', 'German', 
  'Japanese', 'Korean', 'Chinese'
];

export default function Dashboard() {
  const { user } = useAuth();
  const [text, setText] = useState('');
  const [language, setLanguage] = useState('English');
  const [voiceType, setVoiceType] = useState('Female');
  const [styleParam, setStyleParam] = useState('Formal'); // Added visual dropdown state
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [generatedAudio, setGeneratedAudio] = useState(null);
  const [autoTranslate, setAutoTranslate] = useState(true);

  const handleGenerate = async () => {
    if (!text.trim()) {
      setError("Please enter some text");
      return;
    }
    
    setLoading(true);
    setError('');
    setGeneratedAudio(null);
    
    try {
      console.log("DEBUG: Sending TTS generation request...");
      const res = await api.post('/tts/generate', {
        text,
        language,
        voice_type: voiceType,
        auto_translate: autoTranslate
      });
      console.log("DEBUG: API Response received:", res.data);
      setGeneratedAudio(res.data);
    } catch (err) {
      console.error("DEBUG: API Error:", err);
      setError(err.response?.data?.detail || "Error generating voice");
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadUrl = async () => {
    if(!generatedAudio) return;
    try {
      await api.post(`/tts/track_download/${generatedAudio.id}`);
      const url = `${SERVER_URL}/${generatedAudio.file_path}`;
      const a = document.createElement('a');
      a.href = url;
      a.download = `voqube-${generatedAudio.language}.mp3`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    } catch(err) {
      console.error("Failed tracking download", err);
    }
  }

  return (
    <Box>
      <Typography variant="h3" fontWeight="bold" sx={{ color: '#2f3e46', mb: 3, fontSize: { xs: '2rem', sm: '2.5rem', md: '3rem' } }}>
        Home Page
      </Typography>

      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

      <Grid container spacing={4}>
        <Grid item xs={12} md={8}>
          <Typography variant="h5" fontWeight="bold" sx={{ color: '#5c6e58', mb: 1, fontSize: { xs: '1.25rem', md: '1.5rem' } }}>
            Voice Generator
          </Typography>
          <Typography color="text.secondary" sx={{ mb: 4, fontSize: { xs: '0.875rem', md: '1rem' } }}>
            Convert your text to lifelike speech in seconds. 
            {user?.role !== 'admin' && (
              <Box component="span" sx={{ color: '#70826b', fontWeight: 'bold', ml: 1 }}>
                Tokens remaining: {user?.free_generations_left}
              </Box>
            )}
          </Typography>

          <Card elevation={0} sx={{ border: '1px solid #e8e0d5', borderRadius: 3, bgcolor: '#f9f8f4' }}>
            <CardContent sx={{ p: 4 }}>
              <TextField
                fullWidth
                multiline
                rows={8}
                variant="outlined"
                placeholder="Type or paste your text here..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                helperText={`${text.length} characters (Supported up to 10,000+)`}
                sx={{ 
                  mb: 4, 
                  '& .MuiOutlinedInput-root': { 
                    bgcolor: '#ffffff', 
                    borderRadius: 2,
                    '& fieldset': { borderColor: '#e8e0d5' },
                    '&:hover fieldset': { borderColor: '#70826b' },
                    '&.Mui-focused fieldset': { borderColor: '#5c6e58' },
                  },
                  '& .MuiInputBase-input': { color: '#2f3e46' },
                  '& .MuiFormHelperText-root': { color: '#4d5d53' }
                }}
              />
              
              <Grid container spacing={3}>
                <Grid item xs={12} sm={4}>
                  <FormControl fullWidth sx={{
                    '& .MuiOutlinedInput-root': { bgcolor: '#70826b', color: '#ffffff', '& fieldset': { borderColor: '#5c6e58' }, '&:hover fieldset': { borderColor: '#5c6e58' }, '&.Mui-focused fieldset': { borderColor: '#5c6e58' }, '& .MuiSvgIcon-root': { color: '#ffffff' } },
                    '& .MuiInputLabel-root': { color: '#2f3e46', fontWeight: 600, transform: 'translate(14px, -20px) scale(0.75)' },
                    '& .MuiSelect-select': { py: 1.5 }
                  }}>
                    <InputLabel shrink>Language</InputLabel>
                    <Select
                      value={language}
                      onChange={(e) => setLanguage(e.target.value)}
                      displayEmpty
                    >
                      {languages.map(lang => (
                        <MenuItem key={lang} value={lang}>{lang}</MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <FormControl fullWidth sx={{
                     '& .MuiOutlinedInput-root': { bgcolor: '#70826b', color: '#ffffff', '& fieldset': { borderColor: '#5c6e58' }, '&:hover fieldset': { borderColor: '#5c6e58' }, '&.Mui-focused fieldset': { borderColor: '#5c6e58' }, '& .MuiSvgIcon-root': { color: '#ffffff' } },
                     '& .MuiInputLabel-root': { color: '#2f3e46', fontWeight: 600, transform: 'translate(14px, -20px) scale(0.75)' },
                     '& .MuiSelect-select': { py: 1.5 }
                  }}>
                    <InputLabel shrink>Voice Selection</InputLabel>
                    <Select
                      value={voiceType}
                      onChange={(e) => setVoiceType(e.target.value)}
                    >
                      <MenuItem value="Female">
                        {language === 'Malayalam' ? 'Sobhana (Female)' : 'Female Voice'}
                      </MenuItem>
                      <MenuItem value="Male">
                        {language === 'Malayalam' ? 'Midhun (Male)' : 'Male Voice'}
                      </MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <FormControl fullWidth sx={{
                     '& .MuiOutlinedInput-root': { bgcolor: '#70826b', color: '#ffffff', '& fieldset': { borderColor: '#5c6e58' }, '&:hover fieldset': { borderColor: '#5c6e58' }, '&.Mui-focused fieldset': { borderColor: '#5c6e58' }, '& .MuiSvgIcon-root': { color: '#ffffff' } },
                     '& .MuiInputLabel-root': { color: '#2f3e46', fontWeight: 600, transform: 'translate(14px, -20px) scale(0.75)' },
                     '& .MuiSelect-select': { py: 1.5 }
                  }}>
                    <InputLabel shrink>Style</InputLabel>
                    <Select
                      value={styleParam}
                      onChange={(e) => setStyleParam(e.target.value)}
                    >
                      <MenuItem value="Formal">Formal</MenuItem>
                      <MenuItem value="Casual">Casual</MenuItem>
                      <MenuItem value="Expressive">Expressive</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
              </Grid>

              <Box sx={{ mt: { xs: 3, md: 5 }, display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, justifyContent: 'space-between', alignItems: { xs: 'stretch', sm: 'center' }, gap: { xs: 3, sm: 0 } }}>
                <FormControlLabel
                  control={<Switch checked={autoTranslate} onChange={(e) => setAutoTranslate(e.target.checked)} sx={{ '& .MuiSwitch-switchBase.Mui-checked': { color: '#5c6e58' }, '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': { backgroundColor: '#70826b' } }} />}
                  label={<Typography sx={{ color: '#4d5d53', fontWeight: 500, fontSize: { xs: '0.875rem', md: '1rem' } }}>Auto Translate to target language</Typography>}
                />
                <Button
                  variant="contained"
                  size="large"
                  onClick={handleGenerate}
                  disabled={loading || !text.trim()}
                  startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <VolumeUpIcon />}
                  sx={{ px: { xs: 2, sm: 5 }, py: 1.5, bgcolor: '#5c6e58', color: '#ffffff', '&:hover': { bgcolor: '#4a5946' }, width: { xs: '100%', sm: 'auto' }, borderRadius: 2 }}
                >
                  {loading ? 'Generating...' : 'Generate Voice'}
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Typography variant="h6" fontWeight="bold" sx={{ color: '#5c6e58', mb: 2, fontSize: { xs: '1.125rem', md: '1.25rem' } }}>
            Preview & Download
          </Typography>
          <Card elevation={0} sx={{ bgcolor: '#70826b', borderRadius: 3, border: 'none', position: 'relative', overflow: 'hidden' }}>
            <CardContent sx={{ p: 4, textAlign: 'center', minHeight: 300, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
              
              <Typography sx={{ color: '#e8e0d5', mb: 3, fontWeight: 500 }}>
                Your generated audio will appear here.
              </Typography>

              {!generatedAudio ? (
                 <Box sx={{ py: 6 }}>
                    <VolumeUpIcon sx={{ fontSize: 48, color: 'rgba(255,255,255,0.2)' }} />
                 </Box>
              ) : (
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3, zIndex: 1 }}>
                  {generatedAudio.translated_text && (
                    <Box sx={{ p: 2, bgcolor: 'rgba(255,255,255,0.1)', borderRadius: 2, textAlign: 'left', mb: 1 }}>
                      <Typography variant="caption" sx={{ color: '#e8e0d5', fontWeight: 'bold', textTransform: 'uppercase' }} gutterBottom>
                        Translated ({generatedAudio.language})
                      </Typography>
                      <Typography variant="body2" sx={{ mt: 0.5, color: '#ffffff' }}>
                        {generatedAudio.translated_text}
                      </Typography>
                    </Box>
                  )}
                  
                  <Box sx={{ 
                    p: 2, 
                    bgcolor: 'rgba(255, 255, 255, 0.15)', 
                    borderRadius: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: 2
                  }}>
                    <Box sx={{
                      width: '100%',
                      borderRadius: '50px',
                      overflow: 'hidden',
                      display: 'flex',
                      bgcolor: '#f4f1ea'
                    }}>
                      <audio 
                        controls 
                        src={`${SERVER_URL}/${generatedAudio.file_path}`} 
                        style={{ 
                          width: '100%', 
                          outline: 'none', 
                          height: '40px' 
                        }}
                      />
                    </Box>
                  </Box>

                  <Typography sx={{ color: '#e8e0d5', mt: 1, fontWeight: 500 }}>
                    Your generated audio will appear here.
                  </Typography>

                  <Button
                    variant="contained"
                    startIcon={<DownloadIcon />}
                    onClick={handleDownloadUrl}
                    fullWidth
                    size="large"
                    sx={{ mt: 2, py: 1.5, fontWeight: 'bold', bgcolor: '#ffffff', color: '#5c6e58', '&:hover': { bgcolor: '#f4f1ea' }, borderRadius: 2 }}
                  >
                    Download Audio
                  </Button>
                </Box>
              )}

              <Box sx={{ position: 'absolute', bottom: 16, right: 16 }}>
                <StarIcon sx={{ color: '#ffd700', fontSize: 24, opacity: 0.8 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
