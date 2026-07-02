import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({ completion_rate: 0, pending_tasks: 0, weekly_streak: 0, total_tasks: 0, completed_tasks: 0 });
  const [isCalendarConnected, setIsCalendarConnected] = useState(false);
  const [connectedEmail, setConnectedEmail] = useState("");
  const [formData, setFormData] = useState({
    title: "",
    priority: "",
    estimated_hours: "",
    deadline: ""
  });

  // Load analytics, calendar status, and schedule on mount
  useEffect(() => {
    refreshData();
  }, []);

  const refreshData = async () => {
    try {
      const scheduleRes = await axios.get("http://localhost:8000/schedule");
      const analyticsRes = await axios.get("http://localhost:8000/analytics");
      const statusRes = await axios.get("http://localhost:8000/calendar/status");
      
      setTasks(scheduleRes.data);
      setStats(analyticsRes.data);
      setIsCalendarConnected(statusRes.data.connected);
      setConnectedEmail(statusRes.data.email || "");
    } catch (error) {
      console.error("Error loading data", error);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.title || !formData.deadline) {
      alert("Mission Objective and Deadline are required!");
      return;
    }
    
    try {
      const formattedData = {
        title: formData.title,
        priority: parseInt(formData.priority) || 1,
        estimated_hours: parseInt(formData.estimated_hours) || 1,
        deadline: new Date(formData.deadline).toISOString(),
      };

      await axios.post("http://localhost:8000/tasks", formattedData);
      setFormData({ title: "", priority: "", estimated_hours: "", deadline: "" });
      refreshData();
    } catch (error) {
      alert("Failed to add task");
    }
  };

  const handleLogin = () => {
    window.location.href = "http://localhost:8000/oauth/login";
  };

  const handleSyncCalendar = async () => {
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/calendar/sync");
      alert(res.data.message || "Synced successfully!");
      refreshData();
    } catch (error) {
      console.error("Sync failed", error);
      alert(error.response?.data?.error || "Sync failed. Please ensure you are logged in to Google Calendar.");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/tasks/${id}`);
      refreshData();
    } catch (error) {
      console.error("Delete failed", error);
    }
  };

  const markCompleted = async (id) => {
    try {
      await axios.patch(`http://localhost:8000/tasks/${id}/complete`);
      refreshData();
    } catch (error) {
      console.error("Completion failed", error);
    }
  };

  const clearAllTasks = async () => {
    if (!window.confirm("Are you sure you want to PURGE all tasks? This cannot be undone.")) return;
    try {
      await axios.delete("http://localhost:8000/tasks");
      refreshData();
    } catch (error) {
      console.error("Clear failed", error);
    }
  };

  return (
    <>
      {/* --- TOP PROFILE HEADER NAVBAR --- */}
      <header className="navbar">
        <div className="nav-brand">
          <span className="logo-icon">🧠</span> SmartSchedule <span className="logo-accent">AI</span>
        </div>
        <div className="nav-profile">
          <div className="profile-details">
            <span className="profile-name">CYBER_SCHEDULER</span>
            <span className="profile-email">
              {isCalendarConnected ? (
                <span className="email-status connected">🟢 {connectedEmail || "Google Connected"}</span>
              ) : (
                <span className="email-status disconnected">🔴 Offline Calendar</span>
              )}
            </span>
          </div>
          <div className="nav-avatar-container">
            <img 
              src="https://images.unsplash.com/photo-1560253023-3ec5d502959f?q=80&w=200&auto=format&fit=crop" 
              className="nav-avatar" 
              alt="User Profile" 
            />
            <span className="status-indicator"></span>
          </div>
        </div>
      </header>

      <div className="game-hud-container">
        {/* --- 1. PROFILE HEADER --- */}
        <div className="profile-section">
          <div className="player-info" style={{ width: '100%' }}>
            <h1>MISSION CONTROL</h1>
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginTop: '5px' }}>
              <div className="level-badge">
                {stats.pending_tasks === 0 ? "STATUS: IDLE" : "STATUS: ACTIVE"}
              </div>
              <div className="level-badge streak">
                🔥 STREAK: {stats.weekly_streak || 0} DAYS
              </div>
            </div>
          </div>
        </div>

        {/* --- 2. STATS & ANALYTICS --- */}
        <div className="stats-container">
          <div className="stat-row">
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span className="stat-label">Mission Completion</span>
              <span className="stat-val" style={{ color: 'var(--neon-cyan)', fontSize: '0.85rem' }}>{Math.round((stats.completion_rate || 0) * 100)}%</span>
            </div>
            <div className="progress-bar-track">
              <div 
                className="progress-bar-fill cyan" 
                style={{ width: `${(stats.completion_rate || 0) * 100}%` }}
              ></div>
            </div>
          </div>
          <div className="stat-row">
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span className="stat-label">System Load (Pending: {stats.pending_tasks || 0})</span>
              <span className="stat-val" style={{ color: 'var(--neon-pink)', fontSize: '0.85rem' }}>{Math.min((stats.pending_tasks || 0) * 10, 100)}%</span>
            </div>
            <div className="progress-bar-track">
              <div 
                className="progress-bar-fill pink" 
                style={{ width: `${Math.min((stats.pending_tasks || 0) * 10, 100)}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* --- 3. INPUT FORM --- */}
        <form onSubmit={handleSubmit} className="task-form">
          <input
            name="title"
            placeholder="Enter Mission Objective..."
            value={formData.title}
            onChange={handleChange}
            className="cyber-input"
            autoComplete="off"
            required
          />
          <div style={{ display: "flex", gap: "10px" }}>
            <input
              type="number"
              name="priority"
              placeholder="Pri (1-5)"
              min="1" max="5"
              value={formData.priority}
              onChange={handleChange}
              className="cyber-input"
              style={{ width: "80px" }}
              required
            />
            <input
              type="number"
              name="estimated_hours"
              placeholder="Hrs"
              min="1"
              value={formData.estimated_hours}
              onChange={handleChange}
              className="cyber-input"
              style={{ width: "80px" }}
              required
            />
            <input
              type="datetime-local"
              name="deadline"
              value={formData.deadline}
              onChange={handleChange}
              className="cyber-input"
              style={{ flex: 1 }}
              required
            />
          </div>

          <button type="submit" className="cyber-button">
            ADD OBJECTIVE
          </button>
        </form>

        {/* --- 4. ACTION BUTTONS --- */}
        <div className="actions-container">
          <div style={{ display: 'flex', gap: '10px', flexDirection: 'column'}}>
             {isCalendarConnected ? (
               <div style={{ display: 'flex', gap: '10px' }}>
                 <button 
                   onClick={handleSyncCalendar} 
                   className="cyber-button" 
                   disabled={loading} 
                   style={{ flex: 2 }}
                 >
                   {loading ? "SYNCING..." : "SYNC TO GOOGLE CALENDAR"}
                 </button>
                 <button 
                   onClick={handleLogin} 
                   className="cyber-button secondary" 
                   style={{ flex: 1, fontSize: '0.85rem' }}
                 >
                   RECONNECT
                 </button>
               </div>
             ) : (
               <button onClick={handleLogin} className="cyber-button secondary">
                 LINK GOOGLE CALENDAR
               </button>
             )}
             <button onClick={clearAllTasks} className="cyber-button danger">
               PURGE DATA
             </button>
          </div>
        </div>

        {/* --- 5. TASK LIST --- */}
        <div className="task-list">
          {tasks.length === 0 && (
            <div style={{textAlign: 'center', color: 'rgba(255,255,255,0.3)', padding: '20px'}}>NO ACTIVE MISSIONS</div>
          )}
          
          {tasks.map((task) => {
            const start = task.start_time ? new Date(task.start_time) : null;
            const end = task.end_time ? new Date(task.end_time) : null;
            const deadline = new Date(task.deadline);
            
            return (
              <div key={task.id} className={`task-card ${task.conflict ? 'conflict-card' : ''}`}>
                <div className="task-info">
                  <h3>{task.title}</h3>
                  {start && end && (
                    <p className="schedule-time">
                      📅 Schedule: {start.toLocaleString([], {month: 'short', day: 'numeric', hour: '2-digit', minute:'2-digit'})} - {end.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})} ({task.estimated_hours}h)
                    </p>
                  )}
                  <p className="deadline-time">Deadline: {deadline.toLocaleString([], {month: 'short', day: 'numeric', hour: '2-digit', minute:'2-digit'})}</p>
                  {task.conflict && (
                    <span className="conflict-badge">⚠️ Overlaps Deadline!</span>
                  )}
                </div>
                <div className="mini-actions">
                  <button onClick={() => markCompleted(task.id)} className="icon-btn check" title="Complete Objective">
                    ✔
                  </button>
                  <button onClick={() => handleDelete(task.id)} className="icon-btn trash" title="Delete Objective">
                    ✖
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Background Mesh */}
      <div className="bg-grid"></div>
    </>
  );
}

export default App;