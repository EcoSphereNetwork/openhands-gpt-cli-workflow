import axios from 'axios';

const API_URL = '/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Mock data for development
const mockRepositories = [
  { id: 1, name: 'openhands-gpt-cli-workflow', url: 'https://github.com/EcoSphereNetwork/openhands-gpt-cli-workflow', status: 'active' },
  { id: 2, name: 'Dev-Server-Workflow', url: 'https://github.com/EcoSphereNetwork/Dev-Server-Workflow', status: 'active' },
];

const mockIssues = [
  { id: 1, title: 'Fix API integration', repository: 'openhands-gpt-cli-workflow', status: 'open', created_at: '2025-05-10T10:00:00Z' },
  { id: 2, title: 'Update documentation', repository: 'openhands-gpt-cli-workflow', status: 'in_progress', created_at: '2025-05-09T14:30:00Z' },
  { id: 3, title: 'Add new feature', repository: 'Dev-Server-Workflow', status: 'fixed', created_at: '2025-05-08T09:15:00Z' },
];

const mockWorkflowStatus = {
  workflow: {
    running: true,
    lastRun: '2025-05-10T12:30:00Z',
    activeIssues: 2,
  },
  devServer: {
    running: true,
    components: [
      { name: 'n8n', status: 'running' },
      { name: 'mcp-hub', status: 'running' },
      { name: 'docker-mcp', status: 'running' },
      { name: 'openhands-mcp', status: 'stopped' },
    ],
  },
};

// API functions
export const getRepositories = async () => {
  try {
    // In a real implementation, this would be:
    // const response = await api.get('/repositories');
    // return response.data;
    
    // For now, return mock data
    return mockRepositories;
  } catch (error) {
    console.error('Error fetching repositories:', error);
    throw error;
  }
};

export const getIssues = async () => {
  try {
    // In a real implementation, this would be:
    // const response = await api.get('/issues');
    // return response.data;
    
    // For now, return mock data
    return mockIssues;
  } catch (error) {
    console.error('Error fetching issues:', error);
    throw error;
  }
};

export const getWorkflowStatus = async () => {
  try {
    // In a real implementation, this would be:
    // const response = await api.get('/status');
    // return response.data;
    
    // For now, return mock data
    return mockWorkflowStatus;
  } catch (error) {
    console.error('Error fetching workflow status:', error);
    throw error;
  }
};

export const startWorkflow = async () => {
  try {
    // In a real implementation, this would be:
    // const response = await api.post('/workflow/start');
    // return response.data;
    
    // For now, return mock data
    return { success: true, message: 'Workflow started successfully' };
  } catch (error) {
    console.error('Error starting workflow:', error);
    throw error;
  }
};

export const stopWorkflow = async () => {
  try {
    // In a real implementation, this would be:
    // const response = await api.post('/workflow/stop');
    // return response.data;
    
    // For now, return mock data
    return { success: true, message: 'Workflow stopped successfully' };
  } catch (error) {
    console.error('Error stopping workflow:', error);
    throw error;
  }
};

export const startDevServer = async (component = 'all') => {
  try {
    // In a real implementation, this would be:
    // const response = await api.post('/dev-server/start', { component });
    // return response.data;
    
    // For now, return mock data
    return { success: true, message: `Dev-Server component ${component} started successfully` };
  } catch (error) {
    console.error('Error starting Dev-Server:', error);
    throw error;
  }
};

export const stopDevServer = async (component = 'all') => {
  try {
    // In a real implementation, this would be:
    // const response = await api.post('/dev-server/stop', { component });
    // return response.data;
    
    // For now, return mock data
    return { success: true, message: `Dev-Server component ${component} stopped successfully` };
  } catch (error) {
    console.error('Error stopping Dev-Server:', error);
    throw error;
  }
};

export default api;