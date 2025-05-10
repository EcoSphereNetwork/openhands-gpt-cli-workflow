import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { getWorkflowStatus, getRepositories, getIssues } from '../services/api';

interface Repository {
  id: number;
  name: string;
  url: string;
  status: string;
}

interface Issue {
  id: number;
  title: string;
  repository: string;
  status: string;
  created_at: string;
}

interface DevServerStatus {
  running: boolean;
  components: {
    name: string;
    status: string;
  }[];
}

interface WorkflowContextType {
  repositories: Repository[];
  issues: Issue[];
  devServerStatus: DevServerStatus;
  workflowStatus: {
    running: boolean;
    lastRun: string | null;
    activeIssues: number;
  };
  loading: boolean;
  error: string | null;
  refreshData: () => Promise<void>;
}

const WorkflowContext = createContext<WorkflowContextType | undefined>(undefined);

export const WorkflowProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [issues, setIssues] = useState<Issue[]>([]);
  const [devServerStatus, setDevServerStatus] = useState<DevServerStatus>({
    running: false,
    components: []
  });
  const [workflowStatus, setWorkflowStatus] = useState({
    running: false,
    lastRun: null,
    activeIssues: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      // In a real implementation, these would be actual API calls
      // For now, we'll use mock data
      const reposData = await getRepositories();
      const issuesData = await getIssues();
      const statusData = await getWorkflowStatus();
      
      setRepositories(reposData);
      setIssues(issuesData);
      setWorkflowStatus(statusData.workflow);
      setDevServerStatus(statusData.devServer);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to fetch data. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    
    // Set up polling every 30 seconds
    const interval = setInterval(fetchData, 30000);
    
    return () => clearInterval(interval);
  }, []);

  const refreshData = async () => {
    await fetchData();
  };

  return (
    <WorkflowContext.Provider
      value={{
        repositories,
        issues,
        devServerStatus,
        workflowStatus,
        loading,
        error,
        refreshData
      }}
    >
      {children}
    </WorkflowContext.Provider>
  );
};

export const useWorkflow = () => {
  const context = useContext(WorkflowContext);
  if (context === undefined) {
    throw new Error('useWorkflow must be used within a WorkflowProvider');
  }
  return context;
};