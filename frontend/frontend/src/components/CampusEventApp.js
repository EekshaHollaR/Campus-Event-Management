import React, { useState, useEffect } from 'react';
import { Calendar, Users, Star, BarChart3, CheckCircle, Clock, MapPin } from 'lucide-react';

const API_BASE = 'http://localhost:8000';

// Mock API calls for demo purposes
// const mockAPI = {
//   getEvents: () => Promise.resolve([
//     {
//       id: 1,
//       title: "AI Workshop",
//       description: "Introduction to Artificial Intelligence and Machine Learning",
//       type: "workshop",
//       date: "2025-09-13T10:00:00",
//       capacity: 50,
//       registrations_count: 35,
//       status: "active",
//       college_id: 1
//     },
//     {
//       id: 2,
//       title: "Business Strategy Seminar",
//       description: "Modern approaches to business strategy and planning",
//       type: "seminar",
//       date: "2025-09-20T14:00:00",
//       capacity: 100,
//       registrations_count: 75,
//       status: "active",
//       college_id: 2
//     },
//     {
//       id: 3,
//       title: "Cultural Festival",
//       description: "Annual inter-college cultural festival",
//       type: "cultural",
//       date: "2025-09-27T09:00:00",
//       capacity: 200,
//       registrations_count: 150,
//       status: "active",
//       college_id: 3
//     }
//   ]),
  
//   getReports: {
//     popularity: () => Promise.resolve([
//       { event_id: 3, title: "Cultural Festival", registrations: 150 },
//       { event_id: 2, title: "Business Strategy Seminar", registrations: 75 },
//       { event_id: 1, title: "AI Workshop", registrations: 35 }
//     ]),
//     attendance: () => Promise.resolve([
//       { event_id: 3, title: "Cultural Festival", registered: 150, attended: 120, attendance_percentage: 80 },
//       { event_id: 2, title: "Business Strategy Seminar", registered: 75, attended: 65, attendance_percentage: 86.67 },
//       { event_id: 1, title: "AI Workshop", registered: 35, attended: 30, attendance_percentage: 85.71 }
//     ]),
//     feedback: () => Promise.resolve([
//       { event_id: 3, title: "Cultural Festival", average_rating: 4.5, feedback_count: 45 },
//       { event_id: 2, title: "Business Strategy Seminar", average_rating: 4.2, feedback_count: 28 },
//       { event_id: 1, title: "AI Workshop", average_rating: 4.8, feedback_count: 22 }
//     ])
//   },
  
//   registerStudent: (data) => Promise.resolve({ id: Date.now(), ...data, timestamp: new Date().toISOString() }),
//   submitFeedback: (data) => Promise.resolve({ id: Date.now(), ...data, sentiment: "positive" })
// };
const mockAPI = {
  getEvents: async () => {
    const response = await fetch('http://localhost:8000/events');
    return response.json();
  },
  
  registerStudent: async (data) => {
    const response = await fetch('http://localhost:8000/students/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }
}
const CampusEventApp = () => {
  const [currentView, setCurrentView] = useState('events');
  const [events, setEvents] = useState([]);
  const [reports, setReports] = useState({ popularity: [], attendance: [], feedback: [] });
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [registrationSuccess, setRegistrationSuccess] = useState(false);
  const [feedbackSuccess, setFeedbackSuccess] = useState(false);

  useEffect(() => {
    loadEvents();
    loadReports();
  }, []);

  const loadEvents = async () => {
    try {
      const data = await mockAPI.getEvents();
      setEvents(data);
    } catch (error) {
      console.error('Error loading events:', error);
    }
  };

  const loadReports = async () => {
    try {
      const [popularity, attendance, feedback] = await Promise.all([
        mockAPI.getReports.popularity(),
        mockAPI.getReports.attendance(),
        mockAPI.getReports.feedback()
      ]);
      setReports({ popularity, attendance, feedback });
    } catch (error) {
      console.error('Error loading reports:', error);
    }
  };

  const handleRegistration = async (eventId) => {
    try {
      await mockAPI.registerStudent({ 
        student_id: 1, // Mock student ID
        event_id: eventId 
      });
      setRegistrationSuccess(true);
      setTimeout(() => setRegistrationSuccess(false), 3000);
      loadEvents(); // Refresh events
    } catch (error) {
      console.error('Registration error:', error);
    }
  };

  const handleFeedback = async (eventId, rating, comment) => {
    try {
      await mockAPI.submitFeedback({
        student_id: 1, // Mock student ID
        event_id: eventId,
        rating,
        comment
      });
      setFeedbackSuccess(true);
      setTimeout(() => setFeedbackSuccess(false), 3000);
    } catch (error) {
      console.error('Feedback error:', error);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getEventTypeColor = (type) => {
    const colors = {
      workshop: 'bg-blue-100 text-blue-800',
      seminar: 'bg-green-100 text-green-800',
      cultural: 'bg-purple-100 text-purple-800',
      conference: 'bg-orange-100 text-orange-800',
      sports: 'bg-red-100 text-red-800'
    };
    return colors[type] || 'bg-gray-100 text-gray-800';
  };

  const EventsView = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Campus Events</h2>
        <div className="flex space-x-2">
          <select className="px-4 py-2 border border-gray-300 rounded-lg">
            <option>All Types</option>
            <option>Workshop</option>
            <option>Seminar</option>
            <option>Cultural</option>
          </select>
        </div>
      </div>

      {registrationSuccess && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
          Successfully registered for event!
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {events.map(event => (
          <div key={event.id} className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-semibold text-gray-900">{event.title}</h3>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getEventTypeColor(event.type)}`}>
                  {event.type}
                </span>
              </div>
              
              <p className="text-gray-600 mb-4">{event.description}</p>
              
              <div className="space-y-2 mb-4">
                <div className="flex items-center text-sm text-gray-500">
                  <Calendar className="w-4 h-4 mr-2" />
                  {formatDate(event.date)}
                </div>
                <div className="flex items-center text-sm text-gray-500">
                  <Users className="w-4 h-4 mr-2" />
                  {event.registrations_count} / {event.capacity} registered
                </div>
              </div>
              
              <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
                <div 
                  className="bg-blue-600 h-2 rounded-full" 
                  style={{ width: `${(event.registrations_count / event.capacity) * 100}%` }}
                ></div>
              </div>
              
              <button 
                onClick={() => handleRegistration(event.id)}
                disabled={event.registrations_count >= event.capacity}
                className={`w-full py-2 px-4 rounded-lg font-medium ${
                  event.registrations_count >= event.capacity 
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed' 
                    : 'bg-blue-600 text-white hover:bg-blue-700'
                }`}
              >
                {event.registrations_count >= event.capacity ? 'Event Full' : 'Register Now'}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const CheckInView = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Event Check-In</h2>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="text-center">
          <div className="w-32 h-32 mx-auto mb-6 border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center">
            <div className="text-gray-400">
              <div className="w-16 h-16 bg-gray-200 rounded"></div>
              <p className="text-sm mt-2">QR Code Scanner</p>
            </div>
          </div>
          <p className="text-gray-600 mb-4">Scan student QR code to check them in</p>
          <button className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700">
            <CheckCircle className="w-5 h-5 inline mr-2" />
            Manual Check-In
          </button>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4">Recent Check-ins</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between py-2 px-4 bg-gray-50 rounded">
            <div>
              <p className="font-medium">Alice Cooper</p>
              <p className="text-sm text-gray-500">AI Workshop</p>
            </div>
            <div className="flex items-center text-green-600">
              <Clock className="w-4 h-4 mr-1" />
              <span className="text-sm">On time</span>
            </div>
          </div>
          <div className="flex items-center justify-between py-2 px-4 bg-gray-50 rounded">
            <div>
              <p className="font-medium">Bob Smith</p>
              <p className="text-sm text-gray-500">AI Workshop</p>
            </div>
            <div className="flex items-center text-yellow-600">
              <Clock className="w-4 h-4 mr-1" />
              <span className="text-sm">Late (5 min)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const FeedbackView = () => {
    const [rating, setRating] = useState(0);
    const [comment, setComment] = useState('');

    const submitFeedback = (e) => {
      e.preventDefault();
      handleFeedback(1, rating, comment); // Mock event ID
      setRating(0);
      setComment('');
    };

    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-gray-900">Event Feedback</h2>
        
        {feedbackSuccess && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
            Thank you for your feedback!
          </div>
        )}
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-4">Rate Your Experience</h3>
          <form onSubmit={submitFeedback} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Event: AI Workshop
              </label>
              <div className="flex space-x-1 mb-4">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setRating(star)}
                    className={`text-2xl ${star <= rating ? 'text-yellow-400' : 'text-gray-300'}`}
                  >
                    <Star className="w-6 h-6 fill-current" />
                  </button>
                ))}
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Comments (Optional)
              </label>
              <textarea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                placeholder="Share your thoughts about the event..."
              />
            </div>
            
            <button
              type="submit"
              disabled={rating === 0}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              Submit Feedback
            </button>
          </form>
        </div>
      </div>
    );
  };

  const DashboardView = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Dashboard & Reports</h2>
      
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <Calendar className="w-8 h-8 text-blue-600 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-600">Total Events</p>
              <p className="text-2xl font-semibold text-gray-900">{events.length}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <Users className="w-8 h-8 text-green-600 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-600">Total Registrations</p>
              <p className="text-2xl font-semibold text-gray-900">
                {events.reduce((sum, event) => sum + event.registrations_count, 0)}
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <Star className="w-8 h-8 text-yellow-600 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-600">Avg Rating</p>
              <p className="text-2xl font-semibold text-gray-900">4.5</p>
            </div>
          </div>
        </div>
      </div>
      
      {/* Reports */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-4">Event Popularity</h3>
          <div className="space-y-3">
            {reports.popularity.map((item, index) => (
              <div key={index} className="flex justify-between items-center">
                <span className="text-sm text-gray-600">{item.title}</span>
                <span className="font-medium">{item.registrations}</span>
              </div>
            ))}
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-4">Attendance Rate</h3>
          <div className="space-y-3">
            {reports.attendance.map((item, index) => (
              <div key={index} className="space-y-1">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">{item.title}</span>
                  <span className="font-medium">{item.attendance_percentage}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full" 
                    style={{ width: `${item.attendance_percentage}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-4">Feedback Ratings</h3>
          <div className="space-y-3">
            {reports.feedback.map((item, index) => (
              <div key={index} className="flex justify-between items-center">
                <span className="text-sm text-gray-600">{item.title}</span>
                <div className="flex items-center">
                  <Star className="w-4 h-4 text-yellow-400 fill-current mr-1" />
                  <span className="font-medium">{item.average_rating}</span>
                  <span className="text-xs text-gray-500 ml-2">({item.feedback_count})</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const renderView = () => {
    switch (currentView) {
      case 'events':
        return <EventsView />;
      case 'checkin':
        return <CheckInView />;
      case 'feedback':
        return <FeedbackView />;
      case 'dashboard':
        return <DashboardView />;
      default:
        return <EventsView />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">Campus Events</h1>
            </div>
            <div className="flex space-x-8">
              <button
                onClick={() => setCurrentView('events')}
                className={`inline-flex items-center px-1 pt-1 text-sm font-medium ${
                  currentView === 'events' 
                    ? 'text-blue-600 border-b-2 border-blue-600' 
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <Calendar className="w-4 h-4 mr-1" />
                Events
              </button>
              <button
                onClick={() => setCurrentView('checkin')}
                className={`inline-flex items-center px-1 pt-1 text-sm font-medium ${
                  currentView === 'checkin' 
                    ? 'text-blue-600 border-b-2 border-blue-600' 
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <CheckCircle className="w-4 h-4 mr-1" />
                Check-In
              </button>
              <button
                onClick={() => setCurrentView('feedback')}
                className={`inline-flex items-center px-1 pt-1 text-sm font-medium ${
                  currentView === 'feedback' 
                    ? 'text-blue-600 border-b-2 border-blue-600' 
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <Star className="w-4 h-4 mr-1" />
                Feedback
              </button>
              <button
                onClick={() => setCurrentView('dashboard')}
                className={`inline-flex items-center px-1 pt-1 text-sm font-medium ${
                  currentView === 'dashboard' 
                    ? 'text-blue-600 border-b-2 border-blue-600' 
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <BarChart3 className="w-4 h-4 mr-1" />
                Dashboard
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {renderView()}
        </div>
      </main>
    </div>
  );
};

export default CampusEventApp;