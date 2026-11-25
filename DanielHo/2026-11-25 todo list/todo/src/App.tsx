import React, { useState } from "react";

type Task = {
    id: number;
    text: string;
    priority: "High" | "Medium" | "Low";
    isComplete: boolean;
};

type TaskData = {
    task: string;
    priority: "High" | "Medium" | "Low";
};

function App() {
    const currentDate = new Date().toDateString();

    const [taskData, setTaskData] = useState<TaskData>({
        task: "",
        priority: "Medium",
    });

    const [tasks, setTasks] = useState<Task[]>([
        {
            id: 1,
            text: "Scan documents",
            priority: "High",
            isComplete: true,
        },
        {
            id: 2,
            text: "Print documents",
            priority: "Medium",
            isComplete: false,
        },
        {
            id: 3,
            text: "Make Tea",
            priority: "High",
            isComplete: false,
        },
        {
            id: 4,
            text: "Spin on the office chair",
            priority: "Low",
            isComplete: true,
        },
        {
            id: 5,
            text: "Pet the dog",
            priority: "Medium",
            isComplete: false,
        },
        {
            id: 6,
            text: "Make a to-do list app",
            priority: "High",
            isComplete: false,
        },
    ]);

    const handleChange = (
        e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
    ) => {
        const { name, value } = e.target;

        setTaskData((prev) => ({
            ...prev,
            [name]: value,
        }) as TaskData);
    };

    const toggleTask = (id: number) => {
    setTasks((prev) =>
        prev.map((task) =>
            task.id === id
                ? { ...task, isComplete: !task.isComplete }
                : task
        )
    );
};

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        if (!taskData.task.trim()) {
            return;
        }

        const newTask: Task = {
            id: Date.now(),
            text: taskData.task,
            priority: taskData.priority,
            isComplete: false,
        };

        setTasks((prev) => [...prev, newTask]);

        setTaskData({
            task: "",
            priority: "Medium",
        });
    };

    const deleteTask = (id: number) => {
    setTasks((prev) =>
        prev.filter((task) => task.id !== id)
    );
};

    const totalTask = tasks.length;
    const totalCompleted = tasks.filter(
        (task) => task.isComplete
    ).length;
    const totalRemaining = totalTask - totalCompleted

    return (
        <div>
            <h2>{currentDate}</h2>
            <h1>My Tasks</h1>
            <p>
                {totalCompleted} of {totalTask} completed
            </p>      
 {/* Create a new task: */}
            <form onSubmit={handleSubmit}>
                <label>New Task</label>
                <br />

                <input
                    type="text"
                    name="task"
                    value={taskData.task}
                    onChange={handleChange}
                    placeholder="What needs to be done?"
                />
                <br />

                <label>Priority</label>
                <br />

                <select
                    name="priority"
                    value={taskData.priority}
                    onChange={handleChange}
                >
                    <option value="High">High</option>
                    <option value="Medium">Medium</option>
                    <option value="Low">Low</option>
                </select>
                <br />

                <button type="submit">
                    Add task
                </button>
            </form>
            <hr />


{/* Display all tasks: */}
            <table>
                <thead>
                    <tr>
                        <th>Done</th>
                        <th>Task</th>
                        <th>Priority</th>
                        <th>Delete</th>
                    </tr>
                </thead>
                <tbody>
                    {tasks.map(item => {
                        return (
                            <tr key={item.id}>
                                <td>
                                    <input
                                        type="checkbox"
                                        checked={item.isComplete}
                                        onChange={() => toggleTask(item.id)}
                                    />
                                </td>
                                <td>
                                    {item.isComplete ? (
                                        <s>{item.text}</s>
                                    ) : (
                                        item.text
                                    )};
                                </td>
                                <td>{item.priority}</td>
                                <td><button 
                                    type = "button" 
                                    onClick={() => deleteTask(item.id)}
                                >
                                    🗑
                                </button></td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>

            <p>
                {totalRemaining} tasks left
            </p>
        </div>
    );
}

export default App;