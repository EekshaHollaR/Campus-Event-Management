// frontend/src/components/Feedback.js
import React, { useState } from "react";
import { TextField, Button, Alert, MenuItem, CircularProgress, Box, Typography, Rating } from "@mui/material";
import axios from "axios";

const API_BASE = "http://localhost:8000";

function Feedback() {
  const [form, setForm] = useState({ student_id: "", event_id: "", rating: 3, comment: "" });
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState(null);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleRatingChange = (_, value) => setForm({ ...form, rating: value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setFeedback(null);
    try {
      await axios.post(`${API_BASE}/feedback/`, form);
      setFeedback({ type: "success", msg: "Feedback submitted!" });
    } catch (error) {
      setFeedback({ type: "error", msg: error?.response?.data?.detail || "Submission failed" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box maxWidth={500} mx="auto">
      <Typography variant="h5" mb={2}>Event Feedback</Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Student ID"
          name="student_id"
          required
          fullWidth
          margin="normal"
          value={form.student_id}
          onChange={handleChange}
        />
        <TextField
          label="Event ID"
          name="event_id"
          required
          fullWidth
          margin="normal"
          value={form.event_id}
          onChange={handleChange}
        />
        <Box mt={2}>
          <Typography component="legend">Rating</Typography>
          <Rating
            name="rating"
            value={form.rating}
            onChange={handleRatingChange}
            size="large"
          />
        </Box>
        <TextField
          label="Comment"
          name="comment"
          multiline
          rows={3}
          fullWidth
          margin="normal"
          value={form.comment}
          onChange={handleChange}
        />
        {feedback && <Alert severity={feedback.type}>{feedback.msg}</Alert>}
        <Box mt={2} display="flex" alignItems="center">
          <Button variant="contained" color="primary" type="submit" disabled={loading}>{loading ? <CircularProgress size={22}/> : "Submit Feedback"}</Button>
        </Box>
      </form>
    </Box>
  );
}
export default Feedback;
