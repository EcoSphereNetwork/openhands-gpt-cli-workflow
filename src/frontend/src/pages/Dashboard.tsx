import React from 'react';
import {
  Box,
  Grid,
  Typography,
  Paper,
  Divider,
  Button,
  CircularProgress,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  BugReport as BugIcon,
  Code as CodeIcon,
  Storage as ServerIcon,
  Loop as LoopIcon,
  PlayArrow as PlayIcon,
  Stop as StopIcon,
} from '@mui/icons-material';
import DashboardCard from '../components/DashboardCard';
import IssueCard from '../components/IssueCard';
import { useWorkflow } from '../contexts/WorkflowContext';
import { startWorkflow, stopWorkflow } from '../services/api';

const Dashboard: React.FC = () => {
  const { repositories, issues, devServerStatus, workflowStatus, loading, error, refreshData } = useWorkflow();
  const [actionLoading, setActionLoading] = React.useState(false);

  const handleStartWorkflow = async () => {
    setActionLoading(true);
    try {
      await startWorkflow();
      await refreshData();
    } catch (err) {
      console.error('Error starting workflow:', err);
    } finally {
      setActionLoading(false);
    }
  };

  const handleStopWorkflow = async () => {
    setActionLoading(true);
    try {
      await stopWorkflow();
      await refreshData();
    } catch (err) {
      console.error('Error stopping workflow:', err);
    } finally {
      setActionLoading(false);
    }
  };

  const handleFixIssue = async (id: number) => {
    console.log('Fix issue:', id);
    // Implement fix issue logic
  };

  const handleVerifyFix = async (id: number) => {
    console.log('Verify fix:', id);
    // Implement verify fix logic
  };

  if (loading) {
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
          Dashboard
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          {workflowStatus.running ? (
            <Button
              variant="outlined"
              color="warning"
              startIcon={<StopIcon />}
              onClick={handleStopWorkflow}
              disabled={actionLoading}
            >
              Stop Workflow
            </Button>
          ) : (
            <Button
              variant="contained"
              color="primary"
              startIcon={<PlayIcon />}
              onClick={handleStartWorkflow}
              disabled={actionLoading}
            >
              Start Workflow
            </Button>
          )}
          <Button
            variant="outlined"
            onClick={refreshData}
            disabled={actionLoading}
          >
            Refresh
          </Button>
        </Box>
      </Box>

      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <DashboardCard
            title="Repositories"
            value={repositories.length}
            icon={<CodeIcon />}
            linkTo="/repositories"
            color="#2196f3"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <DashboardCard
            title="Active Issues"
            value={workflowStatus.activeIssues}
            icon={<BugIcon />}
            linkTo="/issues"
            color="#f44336"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <DashboardCard
            title="Dev Server"
            value={devServerStatus.running ? 'Running' : 'Stopped'}
            icon={<ServerIcon />}
            linkTo="/dev-server"
            color={devServerStatus.running ? '#4caf50' : '#ff9800'}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <DashboardCard
            title="Workflow Status"
            value={workflowStatus.running ? 'Running' : 'Stopped'}
            icon={<LoopIcon />}
            linkTo="/workflow-monitor"
            color={workflowStatus.running ? '#4caf50' : '#ff9800'}
          />
        </Grid>
      </Grid>

      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" sx={{ mb: 2 }}>
          System Status
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle1">Workflow</Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <Box
                sx={{
                  width: 12,
                  height: 12,
                  borderRadius: '50%',
                  bgcolor: workflowStatus.running ? 'success.main' : 'warning.main',
                  mr: 1,
                }}
              />
              <Typography>
                {workflowStatus.running ? 'Running' : 'Stopped'}
              </Typography>
            </Box>
            {workflowStatus.lastRun && (
              <Typography variant="body2" color="text.secondary">
                Last run: {new Date(workflowStatus.lastRun).toLocaleString()}
              </Typography>
            )}
          </Grid>
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle1">Dev Server Components</Typography>
            {devServerStatus.components.map((component) => (
              <Box key={component.name} sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Box
                  sx={{
                    width: 12,
                    height: 12,
                    borderRadius: '50%',
                    bgcolor: component.status === 'running' ? 'success.main' : 'warning.main',
                    mr: 1,
                  }}
                />
                <Typography>
                  {component.name}: {component.status}
                </Typography>
              </Box>
            ))}
          </Grid>
        </Grid>
      </Paper>

      <Typography variant="h5" sx={{ mb: 2 }}>
        Recent Issues
      </Typography>
      <Grid container spacing={3}>
        {issues.slice(0, 3).map((issue) => (
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
      {issues.length > 3 && (
        <Box sx={{ textAlign: 'center', mt: 2 }}>
          <Button variant="text" onClick={() => window.location.href = '/issues'}>
            View All Issues
          </Button>
        </Box>
      )}
    </Box>
  );
};

export default Dashboard;