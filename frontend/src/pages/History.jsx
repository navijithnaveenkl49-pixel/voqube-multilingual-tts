import React, { useState, useEffect } from 'react';
import { Box, Typography, Card, CardContent, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, IconButton, Chip, Tabs, Tab, Tooltip } from '@mui/material';
import { PlayArrow as PlayIcon, Download as DownloadIcon, Delete as DeleteIcon, Restore as RestoreIcon, DeleteForever as DeleteForeverIcon } from '@mui/icons-material';
import api from '../services/api';

export default function History() {
  const [history, setHistory] = useState([]);
  const [trash, setTrash] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentTab, setCurrentTab] = useState(0);

  const fetchHistory = async () => {
    try {
      const res = await api.get('/tts/history');
      setHistory(res.data);
    } catch (err) {
      console.error("Failed to fetch history", err);
    }
  };

  const fetchTrash = async () => {
    try {
      const res = await api.get('/tts/trash');
      setTrash(res.data);
    } catch (err) {
      console.error("Failed to fetch trash", err);
    }
  };

  const fetchData = async () => {
    setLoading(true);
    await Promise.all([fetchHistory(), fetchTrash()]);
    setLoading(false);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleDownload = async (item) => {
    await api.post(`/tts/track_download/${item.id}`);
    const a = document.createElement('a');
    a.href = item.file_path;
    a.download = `voqube-${item.language}.mp3`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const playAudio = (path) => {
    const audio = new Audio(path);
    audio.play();
  };

  const handleMoveToTrash = async (item) => {
    try {
      await api.post(`/tts/history/${item.id}/trash`);
      fetchData();
    } catch (err) {
      console.error("Failed to move to trash", err);
    }
  };

  const handleRestore = async (item) => {
    try {
      await api.post(`/tts/trash/${item.id}/restore`);
      fetchData();
    } catch (err) {
      console.error("Failed to restore", err);
    }
  };

  const handleDeletePermanently = async (item) => {
    if (window.confirm("Are you sure you want to permanently delete this item?")) {
      try {
        await api.delete(`/tts/trash/${item.id}`);
        fetchData();
      } catch (err) {
        console.error("Failed to delete permanently", err);
      }
    }
  };

  const activeData = currentTab === 0 ? history : trash;

  const handleTabChange = (event, newValue) => {
    setCurrentTab(newValue);
  };

  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" sx={{ fontSize: { xs: '1.75rem', sm: '2.125rem' } }} gutterBottom>
        Generation History
      </Typography>
      <Typography color="text.secondary" sx={{ mb: 2, fontSize: { xs: '0.875rem', md: '1rem' } }}>
        View and manage your previously generated voices.
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={currentTab} onChange={handleTabChange}>
          <Tab label="History" />
          <Tab label="Trash" />
        </Tabs>
      </Box>

      <TableContainer component={Paper} elevation={2}>
        <Table>
          <TableHead sx={{ bgcolor: 'rgba(255,255,255,0.05)' }}>
            <TableRow>
              <TableCell><strong>Date Created</strong></TableCell>
              <TableCell><strong>Text Preview</strong></TableCell>
              <TableCell><strong>Language</strong></TableCell>
              <TableCell><strong>Voice Type</strong></TableCell>
              <TableCell align="right"><strong>Actions</strong></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {activeData.length === 0 && !loading ? (
              <TableRow>
                <TableCell colSpan={5} align="center" sx={{ py: 6 }}>
                  <Typography color="text.secondary">
                    {currentTab === 0 ? "No generation history found. Start creating!" : "Your trash is empty."}
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              activeData.map((item) => (
                <TableRow key={item.id} hover>
                  <TableCell>{new Date(item.created_at).toLocaleString()}</TableCell>
                  <TableCell sx={{ maxWidth: 300, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    <Typography variant="body2">{item.text}</Typography>
                    {item.translated_text && (
                      <Typography variant="caption" color="text.secondary">
                        {item.translated_text}
                      </Typography>
                    )}
                  </TableCell>
                  <TableCell>
                    <Chip label={item.language} size="small" color="primary" variant="outlined" />
                  </TableCell>
                  <TableCell>{item.voice_type}</TableCell>
                  <TableCell align="right">
                    {currentTab === 0 ? (
                      <>
                        <Tooltip title="Play">
                          <IconButton color="secondary" onClick={() => playAudio(item.file_path)} sx={{ mr: 1 }}>
                            <PlayIcon />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Download">
                          <IconButton color="primary" onClick={() => handleDownload(item)} sx={{ mr: 1 }}>
                            <DownloadIcon />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Move to Trash">
                          <IconButton color="error" onClick={() => handleMoveToTrash(item)}>
                            <DeleteIcon />
                          </IconButton>
                        </Tooltip>
                      </>
                    ) : (
                      <>
                        <Tooltip title="Restore">
                          <IconButton color="primary" onClick={() => handleRestore(item)} sx={{ mr: 1 }}>
                            <RestoreIcon />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Delete Permanently">
                          <IconButton color="error" onClick={() => handleDeletePermanently(item)}>
                            <DeleteForeverIcon />
                          </IconButton>
                        </Tooltip>
                      </>
                    )}
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
