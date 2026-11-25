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
        }));
    };

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        if (!taskData.task.trim()) {
            return;
        }

        const newTask: Task = {
            id: tasks.length + 1,
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

    const totalTask = tasks.length;

    const totalCompleted = tasks.filter(
        (task) => task.isComplete
    ).length;

    return (
        <div>
            <h2>{currentDate}</h2>
            <h1>My Tasks</h1>

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
                <br />

                <button type="submit">
                    Add task
                </button>
            </form>

            <hr />

            <ul>
                {tasks.map((task) => (
                    <li key={task.id}>
                        {task.isComplete ? (
                            <s>
                                {task.text} | {task.priority}
                            </s>
                        ) : (
                            <>
                                {task.text} | {task.priority}
                            </>
                        )}
                    </li>
                ))}
            </ul>

            <p>
                Completed Tasks: {totalCompleted}/{totalTask}
            </p>
        </div>
    );
}

export default App;