-- Event Popularity Report
SELECT 
    e.id,
    e.title,
    e.registrations_count,
    c.name as college_name
FROM events e
JOIN colleges c ON e.college_id = c.id
ORDER BY e.registrations_count DESC;

-- Attendance Report
SELECT 
    e.id,
    e.title,
    e.registrations_count,
    COUNT(a.id) as attended_count,
    ROUND((COUNT(a.id) * 100.0 / e.registrations_count), 2) as attendance_percentage
FROM events e
LEFT JOIN registrations r ON e.id = r.event_id
LEFT JOIN attendance a ON r.id = a.registration_id
GROUP BY e.id, e.title, e.registrations_count;

-- Student Participation Report
SELECT 
    s.id,
    s.name,
    c.name as college_name,
    COUNT(a.id) as events_attended
FROM students s
JOIN colleges c ON s.college_id = c.id
LEFT JOIN registrations r ON s.id = r.student_id
LEFT JOIN attendance a ON r.id = a.registration_id
GROUP BY s.id, s.name, c.name
ORDER BY events_attended DESC;

-- Feedback Analysis
SELECT 
    e.id,
    e.title,
    COUNT(f.id) as feedback_count,
    AVG(f.rating) as average_rating,
    COUNT(CASE WHEN f.sentiment = 'positive' THEN 1 END) as positive_feedback,
    COUNT(CASE WHEN f.sentiment = 'negative' THEN 1 END) as negative_feedback,
    COUNT(CASE WHEN f.sentiment = 'neutral' THEN 1 END) as neutral_feedback
FROM events e
LEFT JOIN feedback f ON e.id = f.event_id
GROUP BY e.id, e.title;

-- Cross-College Registration Analysis
SELECT 
    e.title,
    e_college.name as event_college,
    s_college.name as student_college,
    COUNT(r.id) as registrations
FROM events e
JOIN colleges e_college ON e.college_id = e_college.id
JOIN registrations r ON e.id = r.event_id
JOIN students s ON r.student_id = s.id
JOIN colleges s_college ON s.college_id = s_college.id
GROUP BY e.title, e_college.name, s_college.name
ORDER BY e.title, registrations DESC;

-- Upcoming Events with Registration Status
SELECT 
    e.id,
    e.title,
    e.date,
    e.capacity,
    e.registrations_count,
    (e.capacity - e.registrations_count) as available_spots,
    ROUND((e.registrations_count * 100.0 / e.capacity), 2) as fill_percentage
FROM events e
WHERE e.date > datetime('now') AND e.status = 'active'
ORDER BY e.date;