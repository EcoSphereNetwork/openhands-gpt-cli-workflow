import React, { useState } from 'react';
import {
  Box,
  Typography,
  Grid,
  TextField,
  ToggleButtonGroup,
  ToggleButton,
  Paper,
  Button,
  CircularProgress,
  Snackbar,
  Alert,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  BugReport as BugIcon,
  Build as BuildIcon,
  CheckCircle as CheckIcon,
} from '@mui/icons-material';
import IssueCard from '../components/IssueCard';
import { useWorkflow } from '../contexts/WorkflowContext';

const Issues: React.FC = () => {
  const { issues, loading, error, refreshData } = useWorkflow();
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'open' | 'in_progress' | 'fixed'>('all');
  const [actionLoading, setActionLoading] = useState(false);
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success' | 'error' }>({
    open: false,
    message: '',
    severity: 'success',
  });

  const handleFixIssue = async (id: number) => {
    setActionLoading(true);
    try {
      // In a real implementation, this would call an API
      console.log(`Fixing issue ${id}`);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setSnackbar({
        open: true,
        message: `Issue #${id} fix initiated successfully`,
        severity: 'success',
      });
      
      await refreshData();
    } catch (err) {
      console.error(`Error fixing issue ${id}:`, err);
      setSnackbar({
        open: true,
        message: `Failed to fix issue #${id}`,
        severity: 'error',
      });
    } finally {
      setActionLoading(false);
    }
  };

  const handleVerifyFix = async (id: number) => {
    setActionLoading(true);
    try {
      // In a real implementation, this would call an API
      console.log(`Verifying fix for issue ${id}`);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setSnackbar({
        open: true,
        message: `Issue #${id} fix verified successfully`,
        severity: 'success',
      });
      
      await refreshData();
    } catch (err) {
      console.error(`Error verifying fix for issue ${id}:`, err);
      setSnackbar({
        open: true,
        message: `Failed to verify fix for issue #${id}`,
        severity: 'error',
      });
    } finally {
      setActionLoading(false);
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  // Filter issues based on search term and status filter
  const filteredIssues = issues.filter((issue) => {
    const matchesSearch = issue.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         issue.repository.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || issue.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  if (loading && !actionLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ textAlign: 'center', py: 4 }}>
        <Typography variant="h6" color="error">{error}</Typography>
        <Button variant="contained" onClick={refreshData} sx={{ mt: 2 }}>
          Retry
        </Button>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Issues
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={refreshData}
            disabled={actionLoading}
          >
            Refresh
          </Button>
          {actionLoading && <CircularProgress size={24} />}
        </Box>
      </Box>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, gap: 2, mb: 2 }}>
          <TextField
            label="Search issues"
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
            <ToggleButton value="open">
              <BugIcon fontSize="small" sx={{ mr: 0.5 }} />
              Open
            </ToggleButton>
            <ToggleButton value="in_progress">
              <BuildIcon fontSize="small" sx={{ mr: 0.5 }} />
              In Progress
            </ToggleButton>
            <ToggleButton value="fixed">
              <CheckIcon fontSize="small" sx={{ mr: 0.5 }} />
              Fixed
            </ToggleButton>
          </ToggleButtonGroup>
        </Box>
      </Paper>

      {filteredIssues.length === 0 ? (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Typography variant="h6">No issues found</Typography>
          <Typography variant="body2" color="text.secondary">
            Try adjusting your search or filters
          </Typography>
        </Box>
      ) : (
        <Grid container spacing={3}>
          {filteredIssues.map((issue) => (
            <Grid item xs={12} sm={6} md={4} key={issue.id}>
              <IssueCard
                id={issue.id}
                title={issue.title}
                repository={issue.repository}
                status={issue.status as 'open' | 'in_progress' | 'fixed'}
                created_at={issue.created_at}
                onFix={issue.status === 'open' ? handleFixIssue : undefined}
                onVerify={issue.status === 'in_progress' ? handleVerifyFix : undefined}
                url={`https://github.com/EcoSphereNetwork/${issue.repository}/issues/${issue.id}`}
              />
            </Grid>
          ))}
        </Grid>
      )}

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

export default Issues;