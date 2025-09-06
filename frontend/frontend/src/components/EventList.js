import React, { useState, useEffect } from 'react';
import { 
  Card, CardContent, Typography, Button, Grid, 
  FormControl, InputLabel, Select, MenuItem, Box 
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

function EventList() {
  const [events, setEvents] = useState([]);
  const [colleges, setColleges] = useState([]);
  const [filters, setFilters] = useState({
    type: '',
    college_id: '',
    status: 'active'
  });
  const navigate = useNavigate();

  useEffect(() => {
    fetchEvents();
    fetchColleges();
  }, [filters]);

  const fetchEvents = async () => {
    try {
      const params = new URLSearchParams();
      if (filters.type) params.append('event_type', filters.type);
      if (filters.college_id) params.append('college_id', filters.college_id);
      if (filters.status) params.append('status', filters.status);
      
      const response = await axios.get(`${API_BASE}/events/?${params}`);
      setEvents(response.data);
    } catch (error) {
      console.error('Error fetching events:', error);
    }
  };

  const fetchColleges = async () => {
    try {
      const response = await axios.get(`${API_BASE}/colleges/`);
      setColleges(response.data);
    } catch (error) {
      console.error('Error fetching colleges:', error);
    }
  };

  const handleFilterChange = (field, value) => {
    setFilters(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Campus Events
      </Typography>
      
      {/* Filters */}
      <Box sx={{ mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel>Event Type</InputLabel>
              <Select
                value={filters.type}
                onChange={(e) => handleFilterChange('type', e.target.value)}
              >
                <MenuItem value="">All Types</MenuItem>
                <MenuItem value="Conference">Conference</MenuItem>
                <MenuItem value="Workshop">Workshop</MenuItem>
                <MenuItem value="Exhibition">Exhibition</MenuItem>
                <MenuItem value="Sports">Sports</MenuItem>
                <MenuItem value="Symposium">Symposium</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel>College</InputLabel>
              <Select
                value={filters.college_id}
                onChange={(e) => handleFilterChange('college_id', e.target.value)}
              >
                <MenuItem value="">All Colleges</MenuItem>
                {colleges.map(college => (
                  <MenuItem key={college.id} value={college.id}>
                    {college.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Box>

      {/* Events Grid */}
      <Grid container spacing={3}>
        {events.map((event) => (
          <Grid item xs={12} md={6} lg={4} key={event.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {event.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {event.description}
                </Typography>
                <Typography variant="body2">
                  <strong>Type:</strong> {event.type}
                </Typography>
                <Typography variant="body2">
                  <strong>Date:</strong> {new Date(event.date).toLocaleDateString()}
                </Typography>
                <Typography variant="body2">
                  <strong>Capacity:</strong> {event.registrations_count}/{event.capacity}
                </Typography>
                <Typography variant="body2">
                  <strong>Status:</strong> {event.status}
                </Typography>
                <Box sx={{ mt: 2 }}>
                  <Button 
                    variant="contained" 
                    onClick={() => navigate(`/register/${event.id}`)}
                    disabled={event.status !== 'active' || event.registrations_count >= event.capacity}
                  >
                    Register
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </div>
  );
}

export default EventList;