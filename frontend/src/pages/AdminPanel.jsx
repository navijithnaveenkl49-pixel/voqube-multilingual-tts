import React, { useState, useEffect, useRef } from 'react';
import { Box, Typography, Grid, Card, CardContent, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Chip, IconButton, Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, Tabs, Tab, Tooltip } from '@mui/material';
import { PeopleAlt as UsersIcon, VolumeUp as VolumeIcon, Download as DownloadIcon, Edit as EditIcon, PlayArrow as PlayIcon, Stop as StopIcon, ArrowBack as ArrowBackIcon } from '@mui/icons-material';
import api from '../services/api';

function StatCard({ title, value, icon, color }) {
  return (
    <Card elevation={2}>
      <CardContent sx={{ display: 'flex', alignItems: 'center', p: 3 }}>
        <Box sx={{ 
          bgcolor: `${color}.main`, 
          color: 'white', 
          p: 2, 
          borderRadius: 2, 
          mr: 3,
          display: 'flex',
          boxShadow: `0 4px 20px 0 rgba(0,0,0,.14), 0 7px 10px -5px rgba(255,255,255,.4)`
        }}>
          {icon}
        </Box>
        <Box>
          <Typography color="text.secondary" variant="subtitle2" fontWeight="bold" textTransform="uppercase">
            {title}
          </Typography>
          <Typography variant="h4" fontWeight="bold">
            {value}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
}

function TabPanel(props) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`admin-tabpanel-${index}`}
      aria-labelledby={`admin-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ pt: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

export default function AdminPanel() {
  const [tabValue, setTabValue] = useState(0);
  const [stats, setStats] = useState({ total_users: 0, total_generations: 0, total_downloads: 0 });
  const [users, setUsers] = useState([]);
  const [generations, setGenerations] = useState([]);
  const [loading, setLoading] = useState(true);
  
  const [selectedUser, setSelectedUser] = useState(null); 
  const [editUser, setEditUser] = useState(null);
  const [newTokens, setNewTokens] = useState(0);
  const [openDialog, setOpenDialog] = useState(false);
  const [playingId, setPlayingId] = useState(null);
  
  const audioRef = useRef(null);

  const fetchData = async () => {
    try {
      const [statsRes, usersRes, genRes] = await Promise.all([
        api.get('/admin/stats'),
        api.get('/admin/users'),
        api.get('/admin/generations')
      ]);
      setStats(statsRes.data);
      setUsers(usersRes.data);
      setGenerations(genRes.data);
    } catch (err) {
      console.error("Admin fetch failed", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
    };
  }, []);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
    if (audioRef.current) {
      audioRef.current.pause();
      setPlayingId(null);
    }
  };

  const handleEditTokens = (user, e) => {
    if (e) e.stopPropagation(); 
    setEditUser(user);
    setNewTokens(user.free_generations_left);
    setOpenDialog(true);
  };

  const handleUpdateTokens = async () => {
    try {
      await api.put(`/admin/users/${editUser.id}/tokens`, { tokens: parseInt(newTokens) });
      setOpenDialog(false);
      await fetchData(); 
      
      if (selectedUser && selectedUser.id === editUser.id) {
        setSelectedUser(prev => ({ ...prev, free_generations_left: parseInt(newTokens) }));
      }
    } catch (err) {
      alert("Failed to update tokens");
    }
  };

  const handleTogglePlay = (gen) => {
    if (playingId === gen.id) {
      audioRef.current.pause();
      setPlayingId(null);
    } else {
      if (audioRef.current) {
        audioRef.current.pause();
      }
      const audio = new Audio(gen.file_path);
      audio.onended = () => setPlayingId(null);
      audioRef.current = audio;
      audio.play().catch(e => console.error("Audio playback error:", e));
      setPlayingId(gen.id);
    }
  };

  const handleDownload = async (gen) => {
    try {
      const response = await fetch(gen.file_path);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = gen.file_path.split('/').pop() || 'voice.mp3';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error("Download failed", error);
    }
  };

  const renderGenerationsTable = (gens) => (
    <TableContainer component={Paper} elevation={2}>
      <Table>
        <TableHead sx={{ bgcolor: 'rgba(255,255,255,0.05)' }}>
          <TableRow>
            <TableCell><strong>ID</strong></TableCell>
            <TableCell><strong>User</strong></TableCell>
            <TableCell><strong>Original Text</strong></TableCell>
            <TableCell><strong>Language & Voice</strong></TableCell>
            <TableCell><strong>Date</strong></TableCell>
            <TableCell align="center"><strong>Manage</strong></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {gens.map((gen) => (
            <TableRow key={gen.id} hover>
              <TableCell>{gen.id}</TableCell>
              <TableCell>
                <Typography variant="subtitle2">{gen.user?.username || `User #${gen.user_id}`}</Typography>
                <Typography variant="caption" color="text.secondary">{gen.user?.email}</Typography>
              </TableCell>
              <TableCell sx={{ maxWidth: 300 }}>
                <Typography noWrap variant="body2" title={gen.text}>{gen.text}</Typography>
                {gen.translated_text && (
                  <Typography noWrap variant="caption" color="primary" title={gen.translated_text}>
                    Translated: {gen.translated_text}
                  </Typography>
                )}
              </TableCell>
              <TableCell>
                <Chip label={gen.language} size="small" sx={{ mr: 1, mb: 0.5 }} />
                <Chip label={gen.voice_type} size="small" variant="outlined" />
              </TableCell>
              <TableCell>{new Date(gen.created_at).toLocaleString()}</TableCell>
              <TableCell align="center">
                <Tooltip title={playingId === gen.id ? "Stop" : "Play"}>
                  <IconButton 
                    color={playingId === gen.id ? "secondary" : "primary"} 
                    onClick={() => handleTogglePlay(gen)}
                  >
                    {playingId === gen.id ? <StopIcon /> : <PlayIcon />}
                  </IconButton>
                </Tooltip>
                <Tooltip title="Download">
                  <IconButton color="success" onClick={() => handleDownload(gen)}>
                    <DownloadIcon />
                  </IconButton>
                </Tooltip>
              </TableCell>
            </TableRow>
          ))}
          {gens.length === 0 && (
            <TableRow>
              <TableCell colSpan={6} align="center">
                <Typography variant="body2" sx={{ py: 3, color: 'text.secondary' }}>No generations found.</Typography>
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );

  return (
    <Box>
      {selectedUser ? (
        <Box>
          <Button 
             startIcon={<ArrowBackIcon />} 
             onClick={() => setSelectedUser(null)} 
             sx={{ mb: 3 }}
             variant="outlined"
          >
            Back to Admin Panel
          </Button>

          <Typography variant="h4" fontWeight="bold" sx={{ fontSize: { xs: '1.75rem', sm: '2.125rem' } }} gutterBottom>
            User Details: {selectedUser.username}
          </Typography>
          <Typography color="text.secondary" sx={{ mb: 4, fontSize: { xs: '0.875rem', md: '1rem' } }}>
            Manage user tokens and review their specific generated voices.
          </Typography>

          <Grid container spacing={4} sx={{ mb: 6 }}>
            <Grid size={{ xs: 12, md: 6 }}>
              <Card elevation={2} sx={{ height: '100%' }}>
                <CardContent sx={{ p: 4 }}>
                  <Typography variant="h6" fontWeight="bold" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                    <UsersIcon sx={{ mr: 1, color: 'primary.main' }} /> Profile Information
                  </Typography>
                  <Box sx={{ mt: 2 }}>
                    <Typography sx={{ mb: 1 }}><strong>Account ID:</strong> {selectedUser.id}</Typography>
                    <Typography sx={{ mb: 1 }}><strong>Email Address:</strong> {selectedUser.email}</Typography>
                    <Typography sx={{ mb: 1 }}>
                      <strong>Account Role:</strong> <Chip label={selectedUser.role} size="small" color={selectedUser.role === 'admin' ? 'error' : 'default'} sx={{ ml: 1 }} />
                    </Typography>
                    <Typography><strong>Date Joined:</strong> {new Date(selectedUser.created_at).toLocaleDateString()}</Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <Card elevation={2} sx={{ height: '100%' }}>
                <CardContent sx={{ p: 4, display: 'flex', flexDirection: 'column', height: '100%' }}>
                  <Typography variant="h6" fontWeight="bold" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                    <EditIcon sx={{ mr: 1, color: 'secondary.main' }} /> Token Management
                  </Typography>
                  <Box sx={{ mt: 2, flexGrow: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
                    <Typography variant="h3" fontWeight="bold" color="primary.main" gutterBottom>
                      {selectedUser.free_generations_left}
                    </Typography>
                    <Typography color="text.secondary" sx={{ mb: 3 }}>
                      Available Free Generations
                    </Typography>
                    <Button variant="contained" color="primary" onClick={() => handleEditTokens(selectedUser)} startIcon={<EditIcon />}>
                      Update Limits
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          <Typography variant="h5" fontWeight="bold" gutterBottom>
            Generated Voices by {selectedUser.username}
          </Typography>
          {renderGenerationsTable(generations.filter(gen => gen.user_id === selectedUser.id))}
        </Box>
      ) : (
        <Box>
          <Typography variant="h4" fontWeight="bold" sx={{ fontSize: { xs: '1.75rem', sm: '2.125rem' } }} gutterBottom>
            Admin Control Panel
          </Typography>
          <Typography color="text.secondary" sx={{ mb: 4, fontSize: { xs: '0.875rem', md: '1rem' } }}>
            Monitor system usage and user activity.
          </Typography>

          <Grid container spacing={4} sx={{ mb: 4 }}>
            <Grid size={{ xs: 12, sm: 4 }}>
              <StatCard title="Total Users" value={stats.total_users} icon={<UsersIcon fontSize="large" />} color="primary" />
            </Grid>
            <Grid size={{ xs: 12, sm: 4 }}>
              <StatCard title="Total Generations" value={stats.total_generations} icon={<VolumeIcon fontSize="large" />} color="secondary" />
            </Grid>
            <Grid size={{ xs: 12, sm: 4 }}>
              <StatCard title="Total Downloads" value={stats.total_downloads} icon={<DownloadIcon fontSize="large" />} color="success" />
            </Grid>
          </Grid>

          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={tabValue} onChange={handleTabChange} aria-label="admin tabs">
              <Tab label="Users & Limits" />
              <Tab label="All Generations" />
            </Tabs>
          </Box>

          <TabPanel value={tabValue} index={0}>
            <Typography variant="h5" fontWeight="bold" gutterBottom>
              Registered Users
            </Typography>
            <Typography variant="body2" color="primary" sx={{ mb: 2 }}>
              Hint: Click on a user's row below to view their details and generations.
            </Typography>
            <TableContainer component={Paper} elevation={2}>
              <Table>
                <TableHead sx={{ bgcolor: 'rgba(255,255,255,0.05)' }}>
                  <TableRow>
                    <TableCell><strong>ID</strong></TableCell>
                    <TableCell><strong>Username</strong></TableCell>
                    <TableCell><strong>Email</strong></TableCell>
                    <TableCell><strong>Role</strong></TableCell>
                    <TableCell><strong>Tokens Left</strong></TableCell>
                    <TableCell><strong>Joined</strong></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {users.map((u) => (
                    <TableRow 
                      key={u.id} 
                      hover 
                      onClick={() => setSelectedUser(u)}
                      sx={{ cursor: 'pointer', '&:hover': { bgcolor: 'rgba(112, 130, 107, 0.05)' } }}
                    >
                      <TableCell>{u.id}</TableCell>
                      <TableCell>
                        <Tooltip title="View User Details">
                          <Typography fontWeight="bold" color="primary.main" sx={{ textDecoration: 'underline', textUnderlineOffset: 3 }}>
                            {u.username}
                          </Typography>
                        </Tooltip>
                      </TableCell>
                      <TableCell>{u.email}</TableCell>
                      <TableCell>
                        <Chip 
                          label={u.role} 
                          size="small" 
                          color={u.role === 'admin' ? 'error' : 'default'} 
                          variant={u.role === 'admin' ? 'filled' : 'outlined'} 
                        />
                      </TableCell>
                      <TableCell onClick={(e) => e.stopPropagation()}>
                        {u.free_generations_left}
                        <Tooltip title="Edit Tokens">
                          <IconButton size="small" sx={{ ml: 1 }} onClick={(e) => handleEditTokens(u, e)}>
                            <EditIcon fontSize="inherit" />
                          </IconButton>
                        </Tooltip>
                      </TableCell>
                      <TableCell>{new Date(u.created_at).toLocaleDateString()}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <Typography variant="h5" fontWeight="bold" gutterBottom>
              All Users Generations
            </Typography>
            {renderGenerationsTable(generations)}
          </TabPanel>
        </Box>
      )}

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
        <DialogTitle>Update Tokens for {editUser?.username}</DialogTitle>
        <DialogContent sx={{ minWidth: 300, pt: 2 }}>
          <TextField
            fullWidth
            type="number"
            label="Tokens (Free Generations)"
            value={newTokens}
            onChange={(e) => setNewTokens(e.target.value)}
            variant="outlined"
            margin="normal"
          />
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button onClick={handleUpdateTokens} variant="contained">Update</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
