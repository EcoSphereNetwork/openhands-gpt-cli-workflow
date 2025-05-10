import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  CircularProgress,
  Button,
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  Stop as StopIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';

interface StatusCardProps {
  title: string;
  status: 'running' | 'stopped' | 'error';
  description?: string;
  lastUpdated?: string;
  onStart?: () => void;
  onStop?: () => void;
  onRestart?: () => void;
  loading?: boolean;
}

const StatusCard: React.FC<StatusCardProps> = ({
  title,
  status,
  description,
  lastUpdated,
  onStart,
  onStop,
  onRestart,
  loading = false,
}) => {
  const getStatusColor = () => {
    switch (status) {
      case 'running':
        return 'success';
      case 'stopped':
        return 'warning';
      case 'error':
        return 'error';
      default:
        return 'default';
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'running':
        return 'Running';
      case 'stopped':
        return 'Stopped';
      case 'error':
        return 'Error';
      default:
        return 'Unknown';
    }
  };

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" component="div">
            {title}
          </Typography>
          <Chip
            label={getStatusText()}
            color={getStatusColor()}
            size="small"
          />
        </Box>
        
        {description && (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {description}
          </Typography>
        )}
        
        {lastUpdated && (
          <Typography variant="caption" color="text.secondary">
            Last updated: {lastUpdated}
          </Typography>
        )}
        
        <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
          {status === 'stopped' || status === 'error' ? (
            <Button
              variant="outlined"
              size="small"
              startIcon={<PlayIcon />}
              onClick={onStart}
              disabled={loading || !onStart}
            >
              Start
            </Button>
          ) : (
            <Button
              variant="outlined"
              size="small"
              startIcon={<StopIcon />}
              onClick={onStop}
              disabled={loading || !onStop}
            >
              Stop
            </Button>
          )}
          
          <Button
            variant="outlined"
            size="small"
            startIcon={<RefreshIcon />}
            onClick={onRestart}
            disabled={loading || !onRestart || status === 'stopped'}
          >
            Restart
          </Button>
          
          {loading && <CircularProgress size={24} />}
        </Box>
      </CardContent>
    </Card>
  );
};

export default StatusCard;