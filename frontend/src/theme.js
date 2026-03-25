import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'light', 
    primary: {
      main: '#70826b', // Sage green
      dark: '#5c6e58', // Dark sage green
    },
    secondary: {
      main: '#2f3e46', // Dark slate
    },
    background: {
      default: '#f4f1ea', // Matte, textured, off-white wall background (cream)
      paper: '#f9f8f4',   // Light cream background for cards
    },
    text: {
      primary: '#2f3e46', // Dark slate for text
      secondary: '#4d5d53', // Darker green/grey for secondary text
    }
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
      color: '#2f3e46',
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      color: '#2f3e46',
    },
    h4: {
      color: '#5c6e58', // Dark sage green
    },
    h6: {
      color: '#5c6e58', // Dark sage green
    },
    button: {
      textTransform: 'none', 
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          boxShadow: 'none',
          '&:hover': {
            boxShadow: 'none',
          }
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundImage: 'none', 
          backgroundColor: '#f9f8f4', // Light cream
          border: '1px solid #e8e0d5',
          boxShadow: '0 4px 12px rgba(0,0,0,0.03)',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'url("data:image/svg+xml,%3Csvg width=\'20\' height=\'20\' viewBox=\'0 0 20 20\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'%23000000\' fill-opacity=\'0.02\' fill-rule=\'evenodd\'%3E%3Ccircle cx=\'3\' cy=\'3\' r=\'3\'/%3E%3Ccircle cx=\'13\' cy=\'13\' r=\'3\'/%3E%3C/g%3E%3C/svg%3E")', // subtle texture
          backgroundColor: '#f4f1ea',
          border: '1px solid #e8e0d5',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          backgroundColor: '#e8e0d5', // Deeper beige/tan
          borderRight: '1px solid #dcd3c6',
          backgroundImage: 'none',
        }
      }
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#f4f1ea', // Match off-white wall
          borderBottom: '1px solid #e8e0d5',
          color: '#2f3e46',
        }
      }
    },
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundImage: 'url("data:image/svg+xml,%3Csvg width=\'20\' height=\'20\' viewBox=\'0 0 20 20\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'%23000000\' fill-opacity=\'0.02\' fill-rule=\'evenodd\'%3E%3Ccircle cx=\'3\' cy=\'3\' r=\'3\'/%3E%3Ccircle cx=\'13\' cy=\'13\' r=\'3\'/%3E%3C/g%3E%3C/svg%3E")',
        }
      }
    }
  },
});

export default theme;
