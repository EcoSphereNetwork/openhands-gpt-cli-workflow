import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  Button,
  Link,
} from '@mui/material';
import {
  BugReport as BugIcon,
  Build as BuildIcon,
  CheckCircle as CheckIcon,
  OpenInNew as OpenIcon,
} from '@mui/icons-material';

interface IssueCardProps {
  id: number;
  title: string;
  repository: string;
  status: 'open' | 'in_progress' | 'fixed';
  created_at: string;
  onFix?: (id: number) => void;
  onVerify?: (id: number) => void;
  url?: string;
}

const IssueCard: React.FC<IssueCardProps> = ({
  id,
  title,
  repository,
  status,
  created_at,
  onFix,
  onVerify,
  url,
}) => {
  const getStatusColor = () => {
    switch (status) {
      case 'open':
        return 'error';
      case 'in_progress':
        return 'warning';
      case 'fixed':
        return 'success';
      default:
        return 'default';
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'open':
        return 'Open';
      case 'in_progress':
        return 'In Progress';
      case 'fixed':
        return 'Fixed';
      default:
        return 'Unknown';
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case 'open':
        return <BugIcon fontSize="small" />;
      case 'in_progress':
        return <BuildIcon fontSize="small" />;
      case 'fixed':
        return <CheckIcon fontSize="small" />;
      default:
        return null;
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Typography variant="h6" component="div" sx={{ mb: 1 }}>
            {title}
          </Typography>
          <Chip
            icon={getStatusIcon()}
            label={getStatusText()}
            color={getStatusColor()}
            size="small"
          />
        </Box>
        
        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
          Repository: {repository}
        </Typography>
        
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          Created: {formatDate(created_at)}
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
          {status === 'open' && onFix && (
            <Button
              variant="outlined"
              size="small"
              startIcon={<BuildIcon />}
              onClick={() => onFix(id)}
            >
              Fix Issue
            </Button>
          )}
          
          {status === 'in_progress' && onVerify && (
            <Button
              variant="outlined"
              size="small"
              startIcon={<CheckIcon />}
              onClick={() => onVerify(id)}
            >
              Verify Fix
            </Button>
          )}
          
          {url && (
            <Button
              variant="outlined"
              size="small"
              startIcon={<OpenIcon />}
              component={Link}
              href={url}
              target="_blank"
              rel="noopener noreferrer"
            >
              Open Issue
            </Button>
          )}
        </Box>
      </CardContent>
    </Card>
  );
};

export default IssueCard;