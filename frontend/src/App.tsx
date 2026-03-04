import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Navigation from './components/Navigation';
import Dashboard from './components/Dashboard';

// Import platform components
import BooksDashboard from './components/platforms/books/BooksDashboard';
import FacultyDashboard from './components/platforms/faculty/FacultyDashboard';
import StudentDashboard from './components/platforms/student/StudentDashboard';
import ClassesDashboard from './components/platforms/classes/ClassesDashboard';
import OntologyDashboard from './components/platforms/ontology/OntologyDashboard';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 700,
    },
    h4: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 600,
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },
  },
});

function App() {
  const [currentPlatform, setCurrentPlatform] = useState('dashboard');

  const renderPlatform = () => {
    switch (currentPlatform) {
      case 'books':
        return <BooksDashboard />;
      case 'faculty':
        return <FacultyDashboard />;
      case 'students':
        return <StudentDashboard />;
      case 'classes':
        return <ClassesDashboard />;
      case 'ontology':
        return <OntologyDashboard />;
      default:
        return <Dashboard onPlatformSelect={setCurrentPlatform} />;
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Navigation 
        currentPlatform={currentPlatform} 
        onPlatformChange={setCurrentPlatform} 
      />
      <main style={{ marginTop: '80px', padding: '20px' }}>
        {renderPlatform()}
      </main>
    </ThemeProvider>
  );
}

export default App;
