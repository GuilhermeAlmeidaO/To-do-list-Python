import sqlite3

class Task:
    def __init__(self, name):
        self.name = name
        self.done = 0
    
    def __str__(self):
        return f"{self.name}, {self.done}"

messages = {
    'hello': "Hello, welcome to your To-do List",
    'mainMenu': 
"""
    [1] Create a new task
    [2] View all your tasks
    [3] Edit some task
    [4] Delete all completed tasks
    [5] Close the app
""",
    'editMenu': 
"""
What do you want to change in this task?

    [1] Check this done
    [2] Delete this task
""",
    'errorWrongNumberType': "ERROR: You must write a number. \n",
    'errorDontExistInList': "ERROR: This number isn't in the list \n",
    'errorDontExistThisIdInDB': "This id doesn't exits in the database. \n",
    'errorEmptyTaskName': "ERROR: You can't create a task with a empty name. \n",
    'errorDontHaveTasks': "You don't have tasks. \n",
    'errorDontHaveTasksToEdit': "You don't have tasks to edit. \n",
    '-=-': "-=-" * 10,
    '---': "---" * 10,
    '-': "-" * 5
}

def configDB():
    conn = sqlite3.connect("./task.db")
    cursor = conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    done INTERGER NOT NULL DEFAULT 0
)
""")
    conn.commit()
    conn.close()

def getTaskDB(id=None):
    if not id:
        conn = sqlite3.connect("./task.db")
        cursor = conn.cursor()
        cursor.execute("""
SELECT * FROM tasks
""")
        tasks = cursor.fetchall()
        conn.close()
        return tasks
    else:
        conn = sqlite3.connect("./task.db")
        cursor = conn.cursor()
        cursor.execute("""
SELECT * FROM tasks WHERE id = ?
""", (id, ))
        task = cursor.fetchall()
        conn.close()
        return task

def postTaskDB(taskName, taskState):
    conn = sqlite3.connect("./task.db")
    cursor = conn.cursor()
    cursor.execute("""
INSERT INTO tasks (name, done)
VALUES (?, ?)
""", (taskName, taskState))
    conn.commit()
    conn.close()

def putDoneTaskDB(taskID):
    conn = sqlite3.connect("./task.db")
    cursor = conn.cursor()
    cursor.execute("""
UPDATE tasks
SET done = 1
WHERE id = ?
""", (taskID,))
    conn.commit()
    conn.close()

def deleteTaskDB(taskID):
    conn = sqlite3.connect("./task.db")
    cursor = conn.cursor()
    cursor.execute("""
DELETE FROM tasks
WHERE id = ?
""", (taskID, ))
    conn.commit()
    conn.close()

def app():
    print(messages["hello"])
    print(messages["-=-"])
    while True:
        print("Menu: ")
        try:
            userAction = int(input(messages["mainMenu"]))
            match userAction:
                case 1:
                    print(messages["-=-"])
                    while True:
                        taskName = input("Write the task's name: ")
                        if not taskName == "":
                            newTask = Task(taskName)
                            postTaskDB(newTask.name, newTask.done)
                            print("Task created!")
                            break
                        else:
                            print(messages["errorEmptyTaskName"])
                case 2: 
                    print(messages["-=-"])
                    tasks = getTaskDB()
                    if len(tasks) == 0:
                        print(messages["errorDontHaveTasks"])
                    else:
                        print("Your tasks:")
                        print(messages["---"])
                        for task in tasks:
                            print(f"Task: {task[1]} \nId: {task[0]} \nState: {"Done" if task[2] == 1 else "Not done"} \n{"-" * 5}")
                case 3:
                    print(messages["-=-"])
                    tasks = getTaskDB()
                    if len(tasks) == 0:
                        print(messages["errorDontHaveTasksToEdit"])
                    else:
                        while True:
                            try:
                                taskId = int(input("Write the task's id: "))
                                print(messages["-"])
                                taskToEdit = getTaskDB(taskId)
                                if not len(taskToEdit) == 0:
                                    print(f"Task: {taskToEdit[0][1]} \nState: {"Done" if taskToEdit[0][2] == 1 else "Not done"}")
                                    print(messages["-"])
                                    while True:
                                        try:
                                            action = int(input(messages["editMenu"]))
                                            match action:
                                                case 1:
                                                    putDoneTaskDB(taskToEdit[0][0])
                                                    print("The task was checked!")
                                                    break
                                                case 2: 
                                                    deleteTaskDB(taskToEdit[0][0])
                                                    print("The task was deleted!")
                                                    break
                                                case _:
                                                    print(messages["errorDontExistInList"])
                                        except ValueError:
                                            print(messages["errorWrongNumberType"])
                                    break
                                else:
                                    print(messages["errorDontExistThisIdInDB"])
                            except ValueError:
                                print(messages["errorWrongNumberType"])
                    print(messages["-"])
                case 4:
                    print(messages["-=-"])
                    tasks = getTaskDB()
                    if not len(tasks) == 0:
                        for task in tasks:
                            if task[2] == 1:
                                deleteTaskDB(task[0])
                        print("All completed tasks have been deleted!")
                    else: 
                        print(messages["errorDontHaveTasks"])
                case 5:
                    break
                case _:
                    print(messages["errorDontExistInList"])
        except ValueError:
            print(messages["errorWrongNumberType"])


if __name__ == "__main__":
    try:
        configDB()
        app()
    except Exception as e:
        print("error " + e)