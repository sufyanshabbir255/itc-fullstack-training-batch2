from itertools import count

tasks_db: dict [
    int
    ,dict
] = {}

_task_id_counter = count(start=1)


def next_task_id() -> int:
    return next(_task_id_counter)


def seed_data() -> None:
    if tasks_db:
        return
    
    for text, priority, isComplete in [
        (
            "Scan documents"
            ,"High"
            ,True
        ),(
            "Print documents",
            "Medium",
            False,
        ),(
            "Make Tea",
            "High",
            False,
        ),(
            "Spin on the office chair",
            "Low",
            True,
        ),(
            "Pet the dog",
            "Medium",
            False,
        ),(
            "Make a to-do list app",
            "High",
            False,
        )
    ] :
        task_id = next_task_id()
        
        tasks_db[task_id] = {
            "id"            : task_id
            ,"text"         : text
            ,"priority"     : priority
            ,"isComplete"   : isComplete
        }