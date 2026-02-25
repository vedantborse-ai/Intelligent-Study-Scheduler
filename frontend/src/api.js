const BASE_URL = "http://localhost:8000";

export const addTask = async (task) => {
  const formattedTask = {
    ...task,
    deadline: new Date(task.deadline).toISOString()
  };

  const response = await fetch(`${BASE_URL}/tasks`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formattedTask),
  });

  return response.json();
};

export const getSchedule = async () => {
  const res = await fetch(`${BASE_URL}/schedule`);
  return res.json();
};

export const getAnalytics = async () => {
  const res = await fetch(`${BASE_URL}/analytics`);
  return res.json();
};

export const completeTask = async (id) => {
  const res = await fetch(`${BASE_URL}/tasks/${id}/complete`, {
    method: "PUT",
  });
  return res.json();
};
