import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  CircularProgress,
  Alert,
  Snackbar,
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  Stop as StopIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import ServiceList from '../components/ServiceList';
import { useWorkflow } from '../contexts/WorkflowContext';
import { startDevServer, stopDevServer } from '../services/api';

const DevServer: React.FC = () => {
  const { devServerStatus, refreshData } = useWorkflow();
  const [loading, setLoading] = useState(false);
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success' | 'error' }>({
    open: false,
    message: '',
    severity: 'success',
  });

  const handleStartService = async (id: string) => {
    setLoading(true);
    try {
      await startDevServer(id);
      setSnackbar({
        open: true,
        message: `Service ${id} started successfully`,
        severity: 'success',
      });
      await refreshData();
    } catch (err) {
      console.error(`Error starting service ${id}:`, err);
      setSnackbar({
        open: true,
        message: `Failed to start service ${id}`,
        severity: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleStopService = async (id: string) => {
    setLoading(true);
    try {
      await stopDevServer(id);
      setSnackbar({
        open: true,
        message: `Service ${id} stopped successfully`,
        severity: 'success',
      });
      await refreshData();
    } catch (err) {
      console.error(`Error stopping service ${id}:`, err);
      setSnackbar({
        open: true,
        message: `Failed to stop service ${id}`,
        severity: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleRestartService = async (id: string) => {
    setLoading(true);
    try {
      await stopDevServer(id);
      await startDevServer(id);
      setSnackbar({
        open: true,
        message: `Service ${id} restarted successfully`,
        severity: 'success',
      });
      await refreshData();
    } catch (err) {
      console.error(`Error restarting service ${id}:`, err);
      setSnackbar({
        open: true,
        message: `Failed to restart service ${id}`,
        severity: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleStartAll = async () => {
    setLoading(true);
    try {
      await startDevServer('all');
      setSnackbar({
        open: true,
        message: 'All services started successfully',
        severity: 'success',
      });
      await refreshData();
    } catch (err) {
      console.error('Error starting all services:', err);
      setSnackbar({
        open: true,
        message: 'Failed to start all services',
        severity: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleStopAll = async () => {
    setLoading(true);
    try {
      await stopDevServer('all');
      setSnackbar({
        open: true,
        message: 'All services stopped successfully',
        severity: 'success',
      });
      await refreshData();
    } catch (err) {
      console.error('Error stopping all services:', err);
      setSnackbar({
        open: true,
        message: 'Failed to stop all services',
        severity: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  // Convert components to services format
  const services = devServerStatus.components.map((component) => ({
    id: component.name,
    name: component.name.charAt(0).toUpperCase() + component.name.slice(1),
    status: component.status as 'running' | 'stopped' | 'error',
    description: `${component.name} service for Dev-Server-Workflow`,
    lastUpdated: new Date().toISOString(),
    category: 'dev-server',
  }));

  const categories = [
    { id: 'dev-server', name: 'Dev Server Components' },
  ];

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Dev Server
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            color="primary"
            startIcon={<PlayIcon />}
            onClick={handleStartAll}
            disabled={loading}
          >
            Start All
          </Button>
          <Button
            variant="outlined"
            color="warning"
            startIcon={<StopIcon />}
            onClick={handleStopAll}
            disabled={loading}
          >
            Stop All
          </Button>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={refreshData}
            disabled={loading}
          >
            Refresh
          </Button>
          {loading && <CircularProgress size={24} />}
        </Box>
      </Box>

      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Dev Server Status
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box
            sx={{
              width: 12,
              height: 12,
              borderRadius: '50%',
              bgcolor: devServerStatus.running ? 'success.main' : 'warning.main',
              mr: 1,
            }}
          />
          <Typography>
            {devServerStatus.running ? 'Running' : 'Stopped'}
          </Typography>
        </Box>
        <Alert severity="info" sx={{ mb: 2 }}>
          The Dev Server provides a comprehensive development environment with n8n workflows, MCP servers, and monitoring tools.
        </Alert>
      </Paper>

      <ServiceList
        services={services}
        categories={categories}
        onStart={handleStartService}
        onStop={handleStopService}
        onRestart={handleRestartService}
        loading={loading}
      />

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default DevServer;