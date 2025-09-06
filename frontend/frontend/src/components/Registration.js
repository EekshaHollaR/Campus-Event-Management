// frontend/src/components/Registration.js
import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { TextField, Button, Alert, CircularProgress, Box, Typography } from "@mui/material";
import axios from "axios";

const API_BASE = "http://localhost:8000";

function Registration() {
  const { eventId } = useParams();
  const [form, setForm] = useState({ student_id: "", event_id: eventId });
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setFeedback(null);
    try {
      await axios.post(`${API_BASE}/students/register/`, form);
      setFeedback({ type: "success", msg: "Registration successful!" });
      setTimeout(() => navigate("/"), 1200);
    } catch (error) {
      setFeedback({ type: "error", msg: error?.response?.data?.detail || "Failed to register" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box maxWidth={400} mx="auto">
      <Typography variant="h5" mb={2}>Register for Event</Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Student ID"
          name="student_id"
          value={form.student_id}
          onChange={handleChange}
          type="number"
          required
          fullWidth
          margin="normal"
        />
        {feedback && <Alert severity={feedback.type}>{feedback.msg}</Alert>}
        <Box mt={2} display="flex" alignItems="center">
          <Button variant="contained" color="primary" type="submit" disabled={loading}>{loading ? <CircularProgress size={22}/> : "Register"}</Button>
        </Box>
      </form>
    </Box>
  );
}
export default Registration;
