import React, { useState, useEffect } from 'react';
// import ReactDOM from 'react-dom/client';

function App() {
    // Date
    const [currentDate] = useState(new Date().toDateString());

    // New Task
    const [taskData, setTaskData] = useState({
        task        : ''
        ,priority   : 'Medium'
    });

    const handleChange = (e) => {
        const { name, value } = e.target;

        setTaskData((prev) => ({ 
            ...prev
            ,[name]: value 
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(taskData);
    };

    // Example tasks
    const tasks =[
        {
            id          : 1
            ,text       : "Scan documents"
            ,priority   : "High"
            ,isComplete : true
        }
        ,{
            id          : 2
            ,text       : "Print documents"
            ,priority   : "Medium"
            ,isComplete : false
        }
        ,{
            id          : 3
            ,text       : "Make Tea"
            ,priority   : "High"
            ,isComplete : false
        }
        ,{
            id          : 4
            ,text       : "Spin on the office chair"
            ,priority   : "Low"
            ,isComplete : true
        }
        ,{
            id          : 5
            ,text       : "Pet the dog"
            ,priority   : "Medium"
            ,isComplete : false
        }
        ,{
            id          : 6
            ,text       : "Make a to-do list app"
            ,priority   : "High"
            ,isComplete : false
        }


    ];

    return (
        <div>
            <h2>{currentDate}</h2>
            <h1>My Tasks</h1>
            
            <form onSubmit={handleSubmit}>
                <label>New task</label>
                <input name ="task"     value={taskData.task}       onChange={handleChange} placeholder="What needs to be done"/>
                <label>Priority</label>
                <select name="priority" value={taskData.priority}   onChange={handleChange}>
                    <option value="High">Top</option>
                    <option value="Medium">Medium</option>
                    <option value="Low">Low</option>
                </select>
                <button type="submit">Add task</button>
            </form>
        
            <ul>
                {tasks.map((task) => (
                    task.isComplete ==! true ? (                    
                        <li key={task.id}>
                            {task.text} || {task.priority}
                        </li>
                    ) : (
                        <li key={task.id}>
                            <s>{task.text} || {task.priority}</s>
                        </li>
                    )
                ))}
            </ul>

        </div>
    );
}

export default App;