import React, { useState, useEffect } from 'react';
import { 
  Typography, Grid, Card, CardContent, Box,
  Table, TableBody, TableCell, TableContainer, 
  TableHead, TableRow, Paper 
} from '@mui/material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

function Dashboard() {
  const [reports, setReports] = useState({
    eventPopularity: [],
    attendance: [],
    feedback: [],
    topStudents: [],
    upcomingEvents: []
  });

  useEffect(() => {
    fetchAllReports();
  }, []);

  const fetchAllReports = async () => {
    try {
      const [popularity, attendance, feedback, topStudents, upcoming] = await Promise.all([
        axios.get(`${API_BASE}/reports/event-popularity`),
        axios.get(`${API_BASE}/reports/attendance`),
        axios.get(`${API_BASE}/reports/feedback`),
        axios.get(`${API_BASE}/reports/top-students?limit=5`),
        axios.get(`${API_BASE}/reports/upcoming-events`)
      ]);

      setReports({
        eventPopularity: popularity.data,
        attendance: attendance.data,
        feedback: feedback.data,
        topStudents: topStudents.data,
        upcomingEvents: upcoming.data
      });
    } catch (error) {
      console.error('Error fetching reports:', error);
    }
  };

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Admin Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* Event Popularity Chart */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Event Popularity
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={reports.eventPopularity.slice(0, 5)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="title" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="registrations" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Attendance Chart */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Attendance Rates
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={reports.attendance.slice(0, 5)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="title" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="attendance_percentage" fill="#82ca9d" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Top Students */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Top Active Students
              </Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Student Name</TableCell>
                      <TableCell align="right">Events Attended</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {reports.topStudents.map((student) => (
                      <TableRow key={student.student_id}>
                        <TableCell>{student.name}</TableCell>
                        <TableCell align="right">{student.events_attended}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Upcoming Events */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Upcoming Events
              </Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Event Title</TableCell>
                      <TableCell>Date</TableCell>
                      <TableCell>Type</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {reports.upcomingEvents.slice(0, 5).map((event) => (
                      <TableRow key={event.event_id}>
                        <TableCell>{event.title}</TableCell>
                        <TableCell>{new Date(event.date).toLocaleDateString()}</TableCell>
                        <TableCell>{event.type}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
}

export default Dashboard;