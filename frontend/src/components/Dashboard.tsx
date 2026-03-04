import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Alert,
  CircularProgress,
  Chip,
  Button,
} from '@mui/material';
import {
  LibraryBooks,
  School,
  People,
  Class,
  Psychology,
  Launch,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import api from '../services/api';

interface Platform {
  id: string;
  name: string;
  description: string;
  url: string;
  icon: React.ReactNode;
  status: string;
  color: string;
}

interface DashboardProps {
  onPlatformSelect: (platform: string) => void;
}

const Dashboard: React.FC<DashboardProps> = ({ onPlatformSelect }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const platforms: Platform[] = [
    {
      id: 'books',
      name: 'Books & Library',
      description: 'Comprehensive library management with AI-powered features',
      url: '/api/books',
      icon: <LibraryBooks sx={{ fontSize: 48 }} />,
      status: 'active',
      color: '#2e7d32',
    },
    {
      id: 'faculty',
      name: 'Faculty Analytics',
      description: 'Faculty performance and research analytics platform',
      url: '/api/faculty',
      icon: <School sx={{ fontSize: 48 }} />,
      status: 'active',
      color: '#ed6c02',
    },
    {
      id: 'students',
      name: 'Student Analytics',
      description: 'Student performance tracking and analytics',
      url: '/api/students',
      icon: <People sx={{ fontSize: 48 }} />,
      status: 'active',
      color: '#9c27b0',
    },
    {
      id: 'classes',
      name: 'Class Management',
      description: 'ESL curriculum and class management system',
      url: '/api/classes',
      icon: <Class sx={{ fontSize: 48 }} />,
      status: 'active',
      color: '#d32f2f',
    },
    {
      id: 'ontology',
      name: 'Ontology Platform',
      description: 'Advanced ontology management and analysis',
      url: '/api/ontology',
      icon: <Psychology sx={{ fontSize: 48 }} />,
      status: 'active',
      color: '#0288d1',
    },
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <Typography 
            variant="h1" 
            sx={{ 
              mb: 2, 
              background: 'linear-gradient(45deg, #1976d2, #42a5f5)', 
              WebkitBackgroundClip: 'text', 
              WebkitTextFillColor: 'transparent',
              fontSize: { xs: '2rem', md: '3rem' }
            }}
          >
            🎓 Unified Ontology Platform
          </Typography>
          <Typography variant="h5" color="text.secondary" sx={{ mb: 3 }}>
            Integrated Educational Analytics Platform
          </Typography>
          <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, flexWrap: 'wrap' }}>
            <Chip 
              label="Multi-Platform Integration" 
              color="primary" 
              variant="outlined" 
            />
            <Chip 
              label="Educational Analytics" 
              color="secondary" 
              variant="outlined" 
            />
            <Chip 
              label="AI-Powered Insights" 
              color="primary" 
              variant="outlined" 
            />
          </Box>
        </motion.div>
      </Box>

      {/* Platform Cards */}
      <Grid container spacing={3}>
        {platforms.map((platform, index) => (
          <Grid item xs={12} sm={6} md={4} key={platform.id}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card 
                sx={{ 
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: '0 8px 25px rgba(0,0,0,0.15)',
                  },
                }}
                onClick={() => onPlatformSelect(platform.id)}
              >
                <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
                  <Box sx={{ color: platform.color, mb: 2 }}>
                    {platform.icon}
                  </Box>
                  <Typography variant="h6" sx={{ mb: 1, fontWeight: 600 }}>
                    {platform.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {platform.description}
                  </Typography>
                  <Chip
                    label={platform.status}
                    color="success"
                    size="small"
                    sx={{ textTransform: 'capitalize' }}
                  />
                </CardContent>
                <Box sx={{ p: 2, pt: 0 }}>
                  <Button
                    fullWidth
                    variant="contained"
                    sx={{ 
                      backgroundColor: platform.color,
                      '&:hover': {
                        backgroundColor: platform.color,
                        filter: 'brightness(0.9)',
                      },
                    }}
                    endIcon={<Launch />}
                    onClick={(e) => {
                      e.stopPropagation();
                      onPlatformSelect(platform.id);
                    }}
                  >
                    Launch Platform
                  </Button>
                </Box>
              </Card>
            </motion.div>
          </Grid>
        ))}
      </Grid>

      {/* System Overview */}
      <Box sx={{ mt: 6 }}>
        <Card sx={{ background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)', color: 'white' }}>
          <CardContent>
            <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
              🚀 System Overview
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="body1" sx={{ mb: 2 }}>
                  Welcome to the Unified Ontology Platform - your comprehensive educational analytics solution integrating:
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                  <Chip label="📚 Library Management System" sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white', justifyContent: 'flex-start' }} />
                  <Chip label="👨‍🏫 Faculty Analytics Platform" sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white', justifyContent: 'flex-start' }} />
                  <Chip label="🎓 Student Analytics Platform" sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white', justifyContent: 'flex-start' }} />
                  <Chip label="📋 Class Management System" sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white', justifyContent: 'flex-start' }} />
                  <Chip label="🧠 Ontology Management Platform" sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white', justifyContent: 'flex-start' }} />
                </Box>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" sx={{ mb: 2 }}>
                  Platform Features
                </Typography>
                <Typography variant="body2" sx={{ mb: 1 }}>
                  • Single unified API endpoint (Port 8000)
                </Typography>
                <Typography variant="body2" sx={{ mb: 1 }}>
                  • Integrated navigation between platforms
                </Typography>
                <Typography variant="body2" sx={{ mb: 1 }}>
                  • Preserved individual platform functionality
                </Typography>
                <Typography variant="body2" sx={{ mb: 1 }}>
                  • Comprehensive analytics and reporting
                </Typography>
                <Typography variant="body2">
                  • AI-powered insights across all domains
                </Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </Box>

      {/* Footer Info */}
      <Box sx={{ mt: 4, textAlign: 'center' }}>
        <Typography variant="body2" color="text.secondary">
          Unified Ontology Platform v1.0.0 • Backend API: http://localhost:8000
        </Typography>
      </Box>
    </Container>
  );
};

export default Dashboard;