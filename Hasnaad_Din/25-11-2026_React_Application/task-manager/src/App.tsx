import { useState } from "react"; //used to create hooks
import TaskItem from "./TaskItem.tsx";

// describe what a task looks like
type Task = {
  id: number;
  text: string;
  priority: string;
};

function App() {
  const [tasks, setTasks] = useState<Task[]>([]); //list of tasks, default is empty
  const [text, setText] = useState<string>("");
  const [priority, setPriority] = useState<string>("Low");
  const today: string = new Date().toLocaleDateString("en-GB", {
    month: "long",
    year: "numeric",
  });

  function addTask() {
    if (text === "") return;
    const newTask: Task = { id: Date.now(), text: text, priority: priority };
    setTasks([...tasks, newTask]);
    setText("");
    setPriority("Low");
  }

  return (
    <div>
      <p>{today}</p>
      <h1>My Tasks</h1>
      <p>New task</p> <p>0 of {tasks.length} completed</p>
      <div
        style={{
          border: "1px solid grey",
          borderRadius: "8px",
          padding: "10px",
          backgroundColor: "white",
        }}
      >
        <input
          type="text"
          placeholder="What needs to be done?"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <select value={priority} onChange={(e) => setPriority(e.target.value)}>
          <option>High</option>
          <option>Medium</option>
          <option>Low</option>
        </select>
        <button onClick={addTask}>+ Add task</button>
        <ul>
          {tasks.map((task) => (
            <TaskItem key={task.id} text={task.text} priority={task.priority} />
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
