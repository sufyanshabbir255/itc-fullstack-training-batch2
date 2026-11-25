type TaskItemProps = {
  text: string;
  priority: string;
};

function TaskItem(props: TaskItemProps) {
  return (
    <li>
      {props.text} ({props.priority})
    </li>
  );
}

export default TaskItem;
