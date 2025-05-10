import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Divider,
  FormControlLabel,
  Switch,
  Alert,
  Snackbar,
  InputAdornment,
  IconButton,
} from '@mui/material';
import {
  Save as SaveIcon,
  Visibility as VisibilityIcon,
  VisibilityOff as VisibilityOffIcon,
} from '@mui/icons-material';

const Settings: React.FC = () => {
  const [githubToken, setGithubToken] = useState('');
  const [anthropicApiKey, setAnthropicApiKey] = useState('');
  const [showGithubToken, setShowGithubToken] = useState(false);
  const [showAnthropicApiKey, setShowAnthropicApiKey] = useState(false);
  const [autoStartWorkflow, setAutoStartWorkflow] = useState(true);
  const [checkInterval, setCheckInterval] = useState('300');
  const [maxRetries, setMaxRetries] = useState('3');
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success' | 'error' }>({
    open: false,
    message: '',
    severity: 'success',
  });

  const handleSaveApiKeys = () => {
    // In a real implementation, this would save the API keys
    console.log('Saving API keys');
    setSnackbar({
      open: true,
      message: 'API keys saved successfully',
      severity: 'success',
    });
  };

  const handleSaveWorkflowSettings = () => {
    // In a real implementation, this would save the workflow settings
    console.log('Saving workflow settings');
    setSnackbar({
      open: true,
      message: 'Workflow settings saved successfully',
      severity: 'success',
    });
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" sx={{ mb: 3 }}>
        Settings
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card sx={{ mb: 3 }}>
            <CardHeader title="API Keys" />
            <Divider />
            <CardContent>
              <Alert severity="info" sx={{ mb: 3 }}>
                API keys are required for GitHub and Anthropic integration. These keys are stored securely and are not shared.
              </Alert>

              <TextField
                label="GitHub Token"
                variant="outlined"
                fullWidth
                margin="normal"
                value={githubToken}
                onChange={(e) => setGithubToken(e.target.value)}
                type={showGithubToken ? 'text' : 'password'}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        onClick={() => setShowGithubToken(!showGithubToken)}
                        edge="end"
                      >
                        {showGithubToken ? <VisibilityOffIcon /> : <VisibilityIcon />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
              />

              <TextField
                label="Anthropic API Key"
                variant="outlined"
                fullWidth
                margin="normal"
                value={anthropicApiKey}
                onChange={(e) => setAnthropicApiKey(e.target.value)}
                type={showAnthropicApiKey ? 'text' : 'password'}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        onClick={() => setShowAnthropicApiKey(!showAnthropicApiKey)}
                        edge="end"
                      >
                        {showAnthropicApiKey ? <VisibilityOffIcon /> : <VisibilityIcon />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
              />

              <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<SaveIcon />}
                  onClick={handleSaveApiKeys}
                >
                  Save API Keys
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="Workflow Settings" />
            <Divider />
            <CardContent>
              <Alert severity="info" sx={{ mb: 3 }}>
                Configure how the workflow loop operates. These settings affect the behavior of the automated issue fixing process.
              </Alert>

              <FormControlLabel
                control={
                  <Switch
                    checked={autoStartWorkflow}
                    onChange={(e) => setAutoStartWorkflow(e.target.checked)}
                    color="primary"
                  />
                }
                label="Auto-start workflow on system startup"
                sx={{ mb: 2, display: 'block' }}
              />

              <TextField
                label="Check Interval (seconds)"
                variant="outlined"
                fullWidth
                margin="normal"
                value={checkInterval}
                onChange={(e) => setCheckInterval(e.target.value)}
                type="number"
                inputProps={{ min: 60, max: 3600 }}
              />

              <TextField
                label="Max Retries"
                variant="outlined"
                fullWidth
                margin="normal"
                value={maxRetries}
                onChange={(e) => setMaxRetries(e.target.value)}
                type="number"
                inputProps={{ min: 1, max: 10 }}
              />

              <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<SaveIcon />}
                  onClick={handleSaveWorkflowSettings}
                >
                  Save Workflow Settings
                </Button>
              </Box>
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

export default Settings;