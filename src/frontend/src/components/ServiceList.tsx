import React, { useState } from 'react';
import {
  Box,
  Grid,
  TextField,
  ToggleButtonGroup,
  ToggleButton,
  Typography,
  Divider,
  Paper,
} from '@mui/material';
import StatusCard from './StatusCard';

interface Service {
  id: string;
  name: string;
  status: 'running' | 'stopped' | 'error';
  description: string;
  lastUpdated?: string;
  category?: string;
}

interface ServiceListProps {
  services: Service[];
  categories?: { id: string; name: string }[];
  onStart?: (id: string) => void;
  onStop?: (id: string) => void;
  onRestart?: (id: string) => void;
  loading?: boolean;
}

const ServiceList: React.FC<ServiceListProps> = ({
  services,
  categories,
  onStart,
  onStop,
  onRestart,
  loading = false,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'running' | 'stopped' | 'error'>('all');

  // Filter services based on search term and status filter
  const filteredServices = services.filter((service) => {
    const matchesSearch = service.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         service.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || service.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  // Group services by category if categories are provided
  const renderServices = () => {
    if (filteredServices.length === 0) {
      return (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Typography variant="h6">No services found</Typography>
          <Typography variant="body2" color="text.secondary">
            Try adjusting your search or filters
          </Typography>
        </Box>
      );
    }

    if (!categories || categories.length === 0) {
      return (
        <Grid container spacing={3}>
          {filteredServices.map((service) => (
            <Grid item xs={12} sm={6} md={4} key={service.id}>
              <StatusCard
                title={service.name}
                status={service.status}
                description={service.description}
                lastUpdated={service.lastUpdated}
                onStart={() => onStart?.(service.id)}
                onStop={() => onStop?.(service.id)}
                onRestart={() => onRestart?.(service.id)}
                loading={loading}
              />
            </Grid>
          ))}
        </Grid>
      );
    }

    // Group by category
    return categories.map((category) => {
      const categoryServices = filteredServices.filter(
        (service) => service.category === category.id
      );

      if (categoryServices.length === 0) return null;

      return (
        <Box key={category.id} sx={{ mb: 4 }}>
          <Typography variant="h5" sx={{ mb: 2 }}>
            {category.name}
          </Typography>
          <Grid container spacing={3}>
            {categoryServices.map((service) => (
              <Grid item xs={12} sm={6} md={4} key={service.id}>
                <StatusCard
                  title={service.name}
                  status={service.status}
                  description={service.description}
                  lastUpdated={service.lastUpdated}
                  onStart={() => onStart?.(service.id)}
                  onStop={() => onStop?.(service.id)}
                  onRestart={() => onRestart?.(service.id)}
                  loading={loading}
                />
              </Grid>
            ))}
          </Grid>
        </Box>
      );
    });
  };

  return (
    <Box>
      <Paper sx={{ p: 2, mb: 3 }}>
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, gap: 2, mb: 2 }}>
          <TextField
            label="Search services"
            variant="outlined"
            size="small"
            fullWidth
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            sx={{ flexGrow: 1 }}
          />
          <ToggleButtonGroup
            value={statusFilter}
            exclusive
            onChange={(_, newValue) => {
              if (newValue !== null) {
                setStatusFilter(newValue);
              }
            }}
            aria-label="status filter"
            size="small"
          >
            <ToggleButton value="all">All</ToggleButton>
            <ToggleButton value="running">Running</ToggleButton>
            <ToggleButton value="stopped">Stopped</ToggleButton>
            <ToggleButton value="error">Error</ToggleButton>
          </ToggleButtonGroup>
        </Box>
      </Paper>

      {renderServices()}
    </Box>
  );
};

export default ServiceList;