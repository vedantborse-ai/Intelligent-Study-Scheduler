import { addTask, getSchedule, getAnalytics, completeTask } from "./api";
import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({ completion_rate: 0, pending_tasks: 0 });
  const [formData, setFormData] = useState({
    title: "",
    priority: "",
    estimated_hours: "",
    deadline: ""
  });

  // Load analytics and schedule on mount
  useEffect(() => {
    refreshData();
  }, []);

  const refreshData = async () => {
    try {
      const scheduleRes = await axios.get("http://localhost:8000/schedule");
      const analyticsRes = await axios.get("http://localhost:8000/analytics");
      setTasks(scheduleRes.data);
      setStats(analyticsRes.data);
    } catch (error) {
      console.error("Error loading data", error);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if(!formData.title || !formData.deadline) return;
    
    try {
      const formattedData = {
        ...formData,
        priority: parseInt(formData.priority) || 1,
        estimated_hours: parseInt(formData.estimated_hours) || 1,
        deadline: new Date(formData.deadline).toISOString(),
      };

      await axios.post("http://localhost:8000/tasks", formattedData);
      setFormData({ title: "", priority: "", estimated_hours: "", deadline: "" });
      refreshData(); // Reload list
    } catch (error) {
      alert("Failed to add task");
    }
  };

  const handleLogin = () => {
    window.location.href = "http://localhost:8000/oauth/login";
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
    try {
      await axios.delete("http://localhost:8000/tasks");
      refreshData();
    } catch (error) {
      console.error("Clear failed", error);
    }
  };

  return (
    <>
      <div className="game-hud-container">
        {/* --- 1. PROFILE HEADER --- */}
        <div className="profile-section">
          <div className="avatar-container">
            <div className="avatar-glow"></div>
            <img 
              src="https://images.unsplash.com/photo-1560253023-3ec5d502959f?q=80&w=200&auto=format&fit=crop" 
              className="avatar" 
              alt="User" 
            />
          </div>
          <div className="player-info">
            <h1>CYBER_SCHEDULER</h1>
            <div className="level-badge">
              {stats.pending_tasks === 0 ? "STATUS: IDLE" : "STATUS: ACTIVE"}
            </div>
          </div>
        </div>

        {/* --- 2. STATS & ANALYTICS --- */}
        <div className="stats-container">
          <div className="stat-row">
            <span className="stat-label">Mission Completion</span>
            <div className="progress-bar-track">
              <div 
                className="progress-bar-fill cyan" 
                style={{ width: `${stats.completion_rate * 100}%` }}
              ></div>
            </div>
          </div>
          <div className="stat-row">
            <span className="stat-label">System Load (Pending: {stats.pending_tasks})</span>
            <div className="progress-bar-track">
              <div 
                className="progress-bar-fill pink" 
                style={{ width: `${Math.min(stats.pending_tasks * 10, 100)}%` }}
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
            />
            <input
              type="number"
              name="estimated_hours"
              placeholder="Hrs"
              value={formData.estimated_hours}
              onChange={handleChange}
              className="cyber-input"
              style={{ width: "80px" }}
            />
            <input
              type="datetime-local"
              name="deadline"
              value={formData.deadline}
              onChange={handleChange}
              className="cyber-input"
              style={{ flex: 1 }}
            />
          </div>

          <button type="submit" className="cyber-button">
            ADD OBJECTIVE
          </button>
        </form>

        {/* --- 4. ACTION BUTTONS --- */}
        <div className="actions-container">
          <div style={{ display: 'flex', gap: '10px'}}>
             <button onClick={handleLogin} className="cyber-button secondary" style={{fontSize: '0.9rem'}}>
               SYNC GOOGLE CALENDAR
             </button>
             <button onClick={clearAllTasks} className="cyber-button danger" style={{fontSize: '0.9rem'}}>
               PURGE DATA
             </button>
          </div>
        </div>

        {/* --- 5. TASK LIST --- */}
        <div className="task-list">
          {tasks.length === 0 && (
            <div style={{textAlign: 'center', color: 'rgba(255,255,255,0.3)'}}>NO ACTIVE MISSIONS</div>
          )}
          
          {tasks.map((task) => {
            const start = new Date(task.deadline); // simplified for display
            return (
              <div key={task.id} className="task-card">
                <div className="task-info">
                  <h3>{task.title}</h3>
                  <p>Deadline: {start.toLocaleString()}</p>
                </div>
                <div className="mini-actions">
                  <button onClick={() => markCompleted(task.id)} className="icon-btn check" title="Complete">
                    ✔
                  </button>
                  <button onClick={() => handleDelete(task.id)} className="icon-btn trash" title="Delete">
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