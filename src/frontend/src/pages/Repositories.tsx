import React, { useState } from 'react';
import {
  Box,
  Typography,
  Grid,
  TextField,
  Paper,
  Button,
  Card,
  CardContent,
  CardActions,
  Chip,
  Link,
  CircularProgress,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  GitHub as GitHubIcon,
  OpenInNew as OpenIcon,
  Code as CodeIcon,
  BugReport as BugIcon,
  Add as AddIcon,
} from '@mui/icons-material';
import { useWorkflow } from '../contexts/WorkflowContext';

const Repositories: React.FC = () => {
  const { repositories, loading, error, refreshData } = useWorkflow();
  const [searchTerm, setSearchTerm] = useState('');

  // Filter repositories based on search term
  const filteredRepositories = repositories.filter((repo) => {
    return repo.name.toLowerCase().includes(searchTerm.toLowerCase());
  });

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
          Repositories
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            color="primary"
          >
            Add Repository
          </Button>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={refreshData}
          >
            Refresh
          </Button>
        </Box>
      </Box>

      <Paper sx={{ p: 2, mb: 3 }}>
        <TextField
          label="Search repositories"
          variant="outlined"
          size="small"
          fullWidth
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </Paper>

      {filteredRepositories.length === 0 ? (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Typography variant="h6">No repositories found</Typography>
          <Typography variant="body2" color="text.secondary">
            Try adjusting your search or add a new repository
          </Typography>
        </Box>
      ) : (
        <Grid container spacing={3}>
          {filteredRepositories.map((repo) => (
            <Grid item xs={12} sm={6} md={4} key={repo.id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Typography variant="h6" component="div">
                      {repo.name}
                    </Typography>
                    <Chip
                      icon={<GitHubIcon fontSize="small" />}
                      label="GitHub"
                      size="small"
                      color="primary"
                      variant="outlined"
                    />
                  </Box>
                  
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Box
                      sx={{
                        width: 12,
                        height: 12,
                        borderRadius: '50%',
                        bgcolor: repo.status === 'active' ? 'success.main' : 'warning.main',
                        mr: 1,
                      }}
                    />
                    <Typography variant="body2" color="text.secondary">
                      {repo.status === 'active' ? 'Active' : 'Inactive'}
                    </Typography>
                  </Box>
                  
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {repo.url}
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button
                    size="small"
                    startIcon={<CodeIcon />}
                    onClick={() => window.location.href = `/repositories/${repo.id}`}
                  >
                    Details
                  </Button>
                  <Button
                    size="small"
                    startIcon={<BugIcon />}
                    onClick={() => window.location.href = `/issues?repo=${repo.id}`}
                  >
                    Issues
                  </Button>
                  <Box sx={{ flexGrow: 1 }} />
                  <Tooltip title="Open in GitHub">
                    <IconButton
                      size="small"
                      component={Link}
                      href={repo.url}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      <OpenIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};

export default Repositories;