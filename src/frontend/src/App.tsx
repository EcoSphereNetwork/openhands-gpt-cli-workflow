import { Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Repositories from './pages/Repositories';
import Issues from './pages/Issues';
import Settings from './pages/Settings';
import DevServer from './pages/DevServer';
import WorkflowMonitor from './pages/WorkflowMonitor';

function App() {
  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/repositories" element={<Repositories />} />
          <Route path="/issues" element={<Issues />} />
          <Route path="/dev-server" element={<DevServer />} />
          <Route path="/workflow-monitor" element={<WorkflowMonitor />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </Box>
  );
}

export default App;