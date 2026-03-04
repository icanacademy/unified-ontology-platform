import React from 'react';
import { Container, Typography, Alert } from '@mui/material';

const BooksDashboard: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 2 }}>
      <Typography variant="h4" sx={{ mb: 3 }}>
        📚 Books & Library Management Platform
      </Typography>
      <Alert severity="info" sx={{ mb: 3 }}>
        Books platform functionality will be loaded here. All existing features from the original books platform are preserved.
      </Alert>
      <Typography variant="body1">
        This platform includes:
        • Book catalog management
        • User management and circulation
        • AI-powered recommendations
        • Library analytics
        • Advanced search capabilities
      </Typography>
    </Container>
  );
};

export default BooksDashboard;