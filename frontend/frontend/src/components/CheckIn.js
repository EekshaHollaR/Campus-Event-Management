// frontend/src/components/CheckIn.js
import React, { useState } from "react";
import { TextField, Button, Alert, CircularProgress, Box, Typography } from "@mui/material";
import axios from "axios";

const API_BASE = "http://localhost:8000";

function CheckIn() {
  const [registrationId, setRegistrationId] = useState("");
  const [status, setStatus] = useState("present");
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setFeedback(null);
    try {
      await axios.post(`${API_BASE}/attendance/checkin/`, { registration_id: registrationId, status });
      setFeedback({ type: "success", msg: "Check-in successful!" });
    } catch (error) {
      setFeedback({ type: "error", msg: error?.response?.data?.detail || "Check-in failed" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box maxWidth={400} mx="auto">
      <Typography variant="h5" mb={2}>Event Check-In</Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Registration ID"
          value={registrationId}
          required
          fullWidth
          type="number"
          margin="normal"
          onChange={e => setRegistrationId(e.target.value)}
        />
        {feedback && <Alert severity={feedback.type}>{feedback.msg}</Alert>}
        <Box mt={2} display="flex" alignItems="center">
          <Button variant="contained" color="primary" type="submit" disabled={loading}>{loading ? <CircularProgress size={22}/> : "Check In"}</Button>
        </Box>
      </form>
    </Box>
  );
}
export default CheckIn;
