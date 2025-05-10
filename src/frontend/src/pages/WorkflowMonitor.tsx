import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  CircularProgress,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Switch,
  FormControlLabel,
  Alert,
  Snackbar,
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  Stop as StopIcon,
  Refresh as RefreshIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  Loop as LoopIcon,
} from '@mui/icons-material';
import { useWorkflow } from '../contexts/WorkflowContext';
import { startWorkflow, stopWorkflow } from '../services/api';

// Mock workflow logs
const mockLogs = [
  { id: 1, timestamp: '2025-05-10T12:30:00Z', level: 'info', message: 'Workflow started' },
  { id: 2, timestamp: '2025-05-10T12:30:05Z', level: 'info', message: 'Checking for new issues' },
  { id: 3, timestamp: '2025-05-10T12:30:10Z', level: 'info', message: 'Found 2 open issues' },
  { id: 4, timestamp: '2025-05-10T12:30:15Z', level: 'info', message: 'Processing issue #1' },
  { id: 5, timestamp: '2025-05-10T12:30:20Z', level: 'info', message: 'Triggering OpenHands for issue #1' },
  { id: 6, timestamp: '2025-05-10T12:31:00Z', level: 'success', message: 'Fix generated for issue #1' },
  { id: 7, timestamp: '2025-05-10T12:31:05Z', level: 'info', message: 'Creating PR for issue #1' },
  { id: 8, timestamp: '2025-05-10T12:31:10Z', level: 'success', message: 'PR #42 created for issue #1' },
  { id: 9, timestamp: '2025-05-10T12:31:15Z', level: 'info', message: 'Processing issue #2' },
  { id: 10, timestamp: '2025-05-10T12:31:20Z', level: 'info', message: 'Triggering OpenHands for issue #2' },
  { id: 11, timestamp: '2025-05-10T12:32:00Z', level: 'error', message: 'Failed to generate fix for issue #2' },
  { id: 12, timestamp: '2025-05-10T12:32:05Z', level: 'info', message: 'Workflow completed' },
];

const WorkflowMonitor: React.FC = () => {
  const { workflowStatus, refreshData } = useWorkflow();
  const [loading, setLoading] = useState(false);
  const [logs, setLogs] = useState(mockLogs);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success' | 'error' }>({
    open: false,
    message: '',
    severity: 'success',
  });

  const handleStartWorkflow = async () => {
    setLoading(true);
    try {
      await startWorkflow();
      setSnackbar({
        open: true,
        message: 'Workflow started successfully',
        severity: 'success',
      });
      await refreshData();
    } catch (err) {
      console.error('Error starting workflow:', err);
      setSnackbar({
        open: true,
        message: 'Failed to start workflow',
        severity: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleStopWorkflow = async () => {
    setLoading(true);
    try {
      await stopWorkflow();
      setSnackbar({
        open: true,
        message: 'Workflow stopped successfully',
        severity: 'success',
      });
      await refreshData();
    } catch (err) {
      console.error('Error stopping workflow:', err);
      setSnackbar({
        open: true,
        message: 'Failed to stop workflow',
        severity: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  // Auto-refresh effect
  React.useEffect(() => {
    let interval: NodeJS.Timeout;
    
    if (autoRefresh) {
      interval = setInterval(() => {
        refreshData();
      }, 10000); // Refresh every 10 seconds
    }
    
    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [autoRefresh, refreshData]);

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString();
  };

  const getLogIcon = (level: string) => {
    switch (level) {
      case 'success':
        return <CheckIcon color="success" />;
      case 'error':
        return <ErrorIcon color="error" />;
      case 'warning':
        return <ErrorIcon color="warning" />;
      case 'info':
      default:
        return <InfoIcon color="info" />;
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Workflow Monitor
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          {workflowStatus.running ? (
            <Button
              variant="outlined"
              color="warning"
              startIcon={<StopIcon />}
              onClick={handleStopWorkflow}
              disabled={loading}
            >
              Stop Workflow
            </Button>
          ) : (
            <Button
              variant="contained"
              color="primary"
              startIcon={<PlayIcon />}
              onClick={handleStartWorkflow}
              disabled={loading}
            >
              Start Workflow
            </Button>
          )}
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

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardHeader title="Workflow Status" />
            <Divider />
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    width: 48,
                    height: 48,
                    borderRadius: '50%',
                    bgcolor: workflowStatus.running ? 'success.main' : 'warning.main',
                    color: 'white',
                    mr: 2,
                  }}
                >
                  <LoopIcon />
                </Box>
                <Box>
                  <Typography variant="h6">
                    {workflowStatus.running ? 'Running' : 'Stopped'}
                  </Typography>
                  {workflowStatus.lastRun && (
                    <Typography variant="body2" color="text.secondary">
                      Last run: {new Date(workflowStatus.lastRun).toLocaleString()}
                    </Typography>
                  )}
                </Box>
              </Box>

              <Alert severity="info" sx={{ mb: 2 }}>
                The workflow loop continuously monitors repositories for issues and triggers OpenHands to fix them.
              </Alert>

              <FormControlLabel
                control={
                  <Switch
                    checked={autoRefresh}
                    onChange={(e) => setAutoRefresh(e.target.checked)}
                    color="primary"
                  />
                }
                label="Auto-refresh (10s)"
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Card sx={{ height: '100%' }}>
            <CardHeader title="Workflow Logs" />
            <Divider />
            <CardContent sx={{ maxHeight: 400, overflow: 'auto' }}>
              <List dense>
                {logs.map((log) => (
                  <ListItem key={log.id}>
                    <ListItemIcon>
                      {getLogIcon(log.level)}
                    </ListItemIcon>
                    <ListItemText
                      primary={log.message}
                      secondary={formatTimestamp(log.timestamp)}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

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

export default WorkflowMonitor;