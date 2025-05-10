import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  CircularProgress,
  Button,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

interface DashboardCardProps {
  title: string;
  value: string | number;
  description?: string;
  icon?: React.ReactNode;
  loading?: boolean;
  linkTo?: string;
  linkText?: string;
  color?: string;
}

const DashboardCard: React.FC<DashboardCardProps> = ({
  title,
  value,
  description,
  icon,
  loading = false,
  linkTo,
  linkText = 'View Details',
  color,
}) => {
  const navigate = useNavigate();

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" component="div" color="text.secondary">
            {title}
          </Typography>
          {icon && (
            <Box sx={{ color: color || 'primary.main' }}>
              {icon}
            </Box>
          )}
        </Box>
        
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          {loading ? (
            <CircularProgress size={24} />
          ) : (
            <Typography variant="h4" component="div" sx={{ color: color || 'text.primary' }}>
              {value}
            </Typography>
          )}
        </Box>
        
        {description && (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {description}
          </Typography>
        )}
        
        {linkTo && (
          <Box sx={{ mt: 'auto' }}>
            <Button
              variant="text"
              size="small"
              onClick={() => navigate(linkTo)}
              sx={{ color: color || 'primary.main' }}
            >
              {linkText}
            </Button>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default DashboardCard;