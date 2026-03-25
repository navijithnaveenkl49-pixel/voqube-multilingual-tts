import React, { createContext, useState, useMemo, useContext } from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const ColorModeContext = createContext({ toggleColorMode: () => {} });

export const useColorMode = () => useContext(ColorModeContext);

export const ThemeModeProvider = ({ children }) => {
  const [mode, setMode] = useState(() => {
    return localStorage.getItem('themeMode') || 'light';
  });

  const colorMode = useMemo(
    () => ({
      toggleColorMode: () => {
        setMode((prevMode) => {
            const next = prevMode === 'light' ? 'dark' : 'light';
            localStorage.setItem('themeMode', next);
            return next;
        });
      },
    }),
    [],
  );

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode,
          ...(mode === 'light'
            ? {
                // Light Mode Palette (Premium Sage & Cream)
                primary: { main: '#70826b', dark: '#5c6e58' },
                secondary: { main: '#2f3e46' },
                background: { default: '#f4f1ea', paper: '#f9f8f4' },
                text: { primary: '#2f3e46', secondary: '#4d5d53' },
              }
            : {
                // Dark Mode Palette (Forest & Charcoal)
                primary: { main: '#9bb094', dark: '#70826b' },
                secondary: { main: '#f4f1ea' },
                background: { default: '#1a1c1a', paper: '#242624' },
                text: { primary: '#f4f1ea', secondary: '#9bb094' },
              }),
        },
        typography: {
          fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
          h1: { fontWeight: 700 },
          h2: { fontWeight: 600, color: mode === 'light' ? '#2f3e46' : '#f4f1ea' },
          h4: { color: mode === 'light' ? '#5c6e58' : '#9bb094' },
          h6: { color: mode === 'light' ? '#5c6e58' : '#9bb094' },
          button: { textTransform: 'none', fontWeight: 600 },
          subtitle2: { fontWeight: 600 }
        },
        shape: { borderRadius: 12 },
        components: {
          MuiButton: {
            styleOverrides: {
              root: { borderRadius: 8, boxShadow: 'none' },
            },
          },
          MuiCard: {
            styleOverrides: {
              root: {
                backgroundImage: 'none',
                backgroundColor: mode === 'light' ? '#f9f8f4' : '#242624',
                borderColor: mode === 'light' ? '#e8e0d5' : 'rgba(255,255,255,0.1)',
                boxShadow: '0 4px 12px rgba(0,0,0,0.03)',
              },
            },
          },
          MuiPaper: {
            styleOverrides: {
              root: {
                backgroundImage: mode === 'light' ? 'url("data:image/svg+xml,%3Csvg width=\'20\' height=\'20\' viewBox=\'0 0 20 20\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'%23000000\' fill-opacity=\'0.02\' fill-rule=\'evenodd\'%3E%3Ccircle cx=\'3\' cy=\'3\' r=\'3\'/%3E%3Ccircle cx=\'13\' cy=\'13\' r=\'3\'/%3E%3C/g%3E%3C/svg%3E")' : 'none',
                backgroundColor: mode === 'light' ? '#f4f1ea' : '#1a1c1a',
                border: mode === 'light' ? '1px solid #e8e0d5' : '1px solid rgba(255,255,255,0.1)',
              },
            },
          },
          MuiDrawer: {
            styleOverrides: {
              paper: {
                backgroundImage: 'none',
                backgroundColor: mode === 'light' ? '#e8e0d5' : '#1a1c1a',
                borderRight: mode === 'light' ? '1px solid #dcd3c6' : '1px solid rgba(255,255,255,0.1)',
              }
            }
          },
          MuiAppBar: {
            styleOverrides: {
              root: {
                boxShadow: 'none',
                backgroundImage: 'none',
                backgroundColor: mode === 'light' ? '#f4f1ea' : '#1a1c1a',
                borderBottom: mode === 'light' ? '1px solid #e8e0d5' : '1px solid rgba(255,255,255,0.1)',
                color: mode === 'light' ? '#2f3e46' : '#f4f1ea',
              }
            }
          },
          MuiCssBaseline: {
            styleOverrides: {
              body: {
                backgroundImage: mode === 'light' ? 'url("data:image/svg+xml,%3Csvg width=\'20\' height=\'20\' viewBox=\'0 0 20 20\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'%23000000\' fill-opacity=\'0.02\' fill-rule=\'evenodd\'%3E%3Ccircle cx=\'3\' cy=\'3\' r=\'3\'/%3E%3Ccircle cx=\'13\' cy=\'13\' r=\'3\'/%3E%3C/g%3E%3C/svg%3E")' : 'none',
              }
            }
          }
        },
      }),
    [mode],
  );

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        {children}
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
};
