from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import datetime

Base = declarative_base()


class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.datetime.today())

    def __repr__(self):
        return "<Task> " + self.task

    def __str__(self):
        return self.task

    @staticmethod
    def tasks_for_date(date: datetime, session):
        return session.query(Table).order_by(Table.deadline).filter(Table.deadline == date.date()).all()


def print_menu(items):
    for index, item in enumerate(items):
        print(f"{index+1}) {item}")
    print("0) Exit")


def print_tasks(tasks, date, is_today=False, is_all_tasks=False, new_line=True, custom_title=None):
    if custom_title is not None:
        title_string = custom_title
    else:
        title_string = date.strftime("%A %e %b").replace('  ', ' ')

        if is_today:
            title_string = "Today " + date.strftime("%e %b").replace('  ', ' ')
        elif is_all_tasks:
            title_string = "All tasks"

    print(f"{title_string}:")

    if len(tasks) > 0:
        for num, task in enumerate(tasks):
            if is_all_tasks:
                date_string = task.deadline.strftime("%e %b").lstrip()
                print(f"{num + 1}. {task}. {date_string}")
            else:
                print(f"{num + 1}. {task}")
    else:
        print("Nothing to do!")

    if new_line:
        print()


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

stage = []
while True:
    if len(stage) == 0:
        print_menu(["Today's tasks", "Week's tasks", "All tasks", "Missed tasks", "Add task", "Delete task"])
        action = input().strip()
        if action == '1':
            stage.append("tasks")
            stage.append("today")
        elif action == '2':
            stage.append("tasks")
            stage.append("week")
        elif action == '3':
            stage.append("tasks")
            stage.append("all")
        elif action == '4':
            stage.append("tasks")
            stage.append("missed")
        elif action == '5':
            stage.append("add_task")
        elif action == '6':
            stage.append("delete")
        elif action == '0':
            stage.append("exit")

    elif stage[0] == 'tasks':
        date_from = datetime.datetime.today()
        date_to = None
        base_query = session.query(Table).order_by(Table.deadline)

        if stage[1] == 'today':
            tasks = Table.tasks_for_date(date_from.date(), session)
            print_tasks(tasks, date_from, is_today=True)

        elif stage[1] == 'week':
            date_to = date_from + datetime.timedelta(days=7)
            current_date = date_from
            while current_date < date_to:
                tasks = Table.tasks_for_date(current_date.date(), session)
                print_tasks(tasks, current_date)
                current_date += datetime.timedelta(days=1)

        elif stage[1] == 'all':
            tasks = base_query.all()
            print_tasks(tasks, date_from, is_all_tasks=True)

        elif stage[1] == 'missed':
            tasks = base_query.filter(Table.deadline < date_from.date()).all()
            if len(tasks) > 0:
                print_tasks(tasks, date_from, is_all_tasks=True, custom_title="Missed tasks")
            else:
                print("Nothing is missed!")
                print()

        stage.clear()

    elif stage[0] == 'add_task':
        print("Enter task")
        task_text = input().strip()

        print("Enter deadline")
        task_deadline = datetime.datetime.strptime(input().strip(), "%Y-%m-%d")

        new_task_row = Table(task=task_text, deadline=task_deadline)
        session.add(new_task_row)
        session.commit()
        print("The task has been added!")
        print()
        stage.pop()

    elif stage[0] == 'delete':
        tasks = session.query(Table).order_by(Table.deadline).all()

        if len(tasks) > 0:
            title = "Choose the number of the task you want to delete"
            print_tasks(tasks, None, is_all_tasks=True, new_line=False, custom_title=title)
            task_num = int(input().strip())
            session.delete(tasks[task_num - 1])
            session.commit()
            print("The task has been deleted!")
        else:
            print("Nothing to delete")
        print()
        stage.pop()

    elif stage[0] == 'exit':
        print("Bye!")
        break
