import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Chip,
} from '@mui/material';
import {
  LibraryBooks,
  School,
  People,
  Class,
  Psychology,
  Dashboard as DashboardIcon,
} from '@mui/icons-material';

interface NavigationProps {
  currentPlatform: string;
  onPlatformChange: (platform: string) => void;
}

const Navigation: React.FC<NavigationProps> = ({ currentPlatform, onPlatformChange }) => {
  const platforms = [
    {
      id: 'dashboard',
      name: 'Dashboard',
      icon: <DashboardIcon />,
      color: '#1976d2',
    },
    {
      id: 'books',
      name: 'Books & Library',
      icon: <LibraryBooks />,
      color: '#2e7d32',
    },
    {
      id: 'faculty',
      name: 'Faculty Analytics',
      icon: <School />,
      color: '#ed6c02',
    },
    {
      id: 'students',
      name: 'Student Analytics',
      icon: <People />,
      color: '#9c27b0',
    },
    {
      id: 'classes',
      name: 'Class Management',
      icon: <Class />,
      color: '#d32f2f',
    },
    {
      id: 'ontology',
      name: 'Ontology Platform',
      icon: <Psychology />,
      color: '#0288d1',
    },
  ];

  return (
    <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 0, mr: 4 }}>
          Unified Ontology Platform
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', flexGrow: 1 }}>
          {platforms.map((platform) => (
            <Button
              key={platform.id}
              onClick={() => onPlatformChange(platform.id)}
              sx={{
                color: 'white',
                backgroundColor: currentPlatform === platform.id ? 'rgba(255,255,255,0.2)' : 'transparent',
                '&:hover': {
                  backgroundColor: 'rgba(255,255,255,0.1)',
                },
                borderRadius: 2,
                minHeight: 40,
                px: 2,
              }}
              startIcon={platform.icon}
            >
              {platform.name}
            </Button>
          ))}
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Chip
            label="v1.0.0"
            size="small"
            sx={{
              backgroundColor: 'rgba(255,255,255,0.2)',
              color: 'white',
              fontWeight: 'bold',
            }}
          />
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navigation;