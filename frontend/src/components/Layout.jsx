import React, { useState } from 'react';
import { Box, Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Typography, IconButton, AppBar, Toolbar, Divider, Avatar, Card, CardContent, Button } from '@mui/material';
import { Home as HomeIcon, History as HistoryIcon, AdminPanelSettings as AdminIcon, Logout as LogoutIcon, Menu as MenuIcon, Brightness4 as DarkModeIcon, Brightness7 as LightModeIcon } from '@mui/icons-material';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useColorMode } from '../theme';
import { useTheme } from '@mui/material/styles';

const drawerWidth = 260;

export default function Layout() {
  const { user, logout } = useAuth();
  const colorMode = useColorMode();
  const theme = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const menuItems = [
    { text: 'Home Page', icon: <HomeIcon />, path: '/dashboard' },
    { text: 'History', icon: <HistoryIcon />, path: '/dashboard/history' },
  ];

  if (user?.role === 'admin') {
    menuItems.push({ text: 'Admin Panel', icon: <AdminIcon />, path: '/dashboard/admin' });
  }

  const drawer = (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <Box sx={{ p: 3, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Typography variant="h5" fontWeight="bold" sx={{ color: '#2f3e46' }}>
          VoQube
        </Typography>
      </Box>
      <Divider sx={{ borderColor: '#dcd3c6' }} />
      <List sx={{ flexGrow: 1, px: 2, py: 2 }}>
        {menuItems.map((item) => {
          const isSelected = location.pathname === item.path;
          return (
            <ListItem 
              key={item.text} 
              disablePadding
              sx={{ mb: 1 }}
            >
              <ListItemButton
                onClick={() => { navigate(item.path); setMobileOpen(false); }}
                sx={{
                  borderRadius: 2,
                  bgcolor: isSelected ? 'primary.main' : 'transparent',
                  color: isSelected ? '#f4f1ea' : '#2f3e46',
                  '&:hover': {
                    bgcolor: isSelected ? 'primary.main' : 'rgba(112, 130, 107, 0.1)',
                  }
                }}
              >
                <ListItemIcon sx={{ color: isSelected ? '#f4f1ea' : '#2f3e46', minWidth: 40 }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText 
                  primary={item.text} 
                  primaryTypographyProps={{ 
                    fontWeight: isSelected ? 600 : 500,
                  }} 
                />
              </ListItemButton>
            </ListItem>
          )
        })}
      </List>
      <Box sx={{ p: 2 }}>
        <Card sx={{ bgcolor: 'transparent', boxShadow: 'none', border: 'none', mb: 2 }}>
          <CardContent sx={{ py: 1.5, px: 2, '&:last-child': { pb: 1.5 } }}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Avatar sx={{ bgcolor: '#70826b', color: '#f4f1ea', width: 40, height: 40, mr: 1.5, fontWeight: 'bold' }}>
                {user?.username?.[0]?.toUpperCase() || 'A'}
              </Avatar>
              <Box>
                <Typography variant="subtitle2" noWrap sx={{ maxWidth: 120, color: '#2f3e46', fontWeight: 600 }}>
                  {user?.username || 'admin'}
                </Typography>
                <Typography variant="caption" sx={{ color: '#4d5d53', fontWeight: 500 }}>
                  Tokens: {user?.free_generations_left ?? 10001}
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
        <Button 
          fullWidth 
          variant="outlined" 
          startIcon={<LogoutIcon />}
          onClick={handleLogout}
          sx={{ 
            borderRadius: 2, 
            borderColor: '#2f3e46', 
            color: '#2f3e46',
            '&:hover': {
              borderColor: '#2f3e46',
              bgcolor: 'rgba(47, 62, 70, 0.05)'
            }
          }}
        >
          Logout
        </Button>
      </Box>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ color: 'text.primary', fontWeight: 600, flexGrow: 1 }}>
            {menuItems.find(m => m.path === location.pathname)?.text || 'VoQube User Portal'}
          </Typography>
          <IconButton onClick={colorMode.toggleColorMode} color="inherit">
            {theme.palette.mode === 'dark' ? <LightModeIcon /> : <DarkModeIcon />}
          </IconButton>
        </Toolbar>
      </AppBar>

      <Box component="nav" sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}>
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }}
          sx={{
            display: { xs: 'block', sm: 'none' },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      <Box component="main" sx={{ flexGrow: 1, p: { xs: 2, sm: 3, md: 4 }, mt: 8, width: { xs: '100%', sm: `calc(100% - ${drawerWidth}px)` } }}>
        <Outlet />
      </Box>
    </Box>
  );
}
