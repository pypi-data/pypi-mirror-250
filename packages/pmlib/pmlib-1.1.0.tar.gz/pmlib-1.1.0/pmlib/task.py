from collections.abc import Sequence
from typing import List

from email_validator import validate_email, EmailNotValidError
from loguru import logger
import attrs
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import texttable

from tasklib.lazy import LazyUUIDTaskSet
from tasklib.task import TaskQuerySet
from tasklib import Task, TaskWarrior

# Set pandas display width
#     https://stackoverflow.com/a/11711637/667301
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

@attrs.define(repr=False)
class OwnedTask(Task):
    """
    A tasklib.task.Task() subclass which is owned by an email address and has a UUID.

    :param tw: A ``tasklib.TaskWarrior()`` instance
    :type tw: TaskWarrior
    :param description: The description of the task
    :type description: str
    :param due: The date due in form of 'YYYY-MM-DD'
    :type due: str
    :param start: The start date in form of 'YYYY-MM-DD'
    :type start: str
    :param priority: Character representing the priority: H, M, or L
    :type priority: str
    :param owner: The email address of the person who owns the task; this is stored as a Task() tag.
    :type owner: str
    :return: An OwnedTask(), which is an instance of ``tasklib.task.Task()`` with a string ``owner``
    :rtype: OwnedTask
    """
    tw: TaskWarrior = None
    due: str = None
    start: str = None
    priority: str = None
    owner: str = None
    project: str = None
    description: str = None
    status: str = None

    @logger.catch(reraise=True)
    def __init__(self,
                 tw: TaskWarrior = None,
                 due: str = None,
                 start: str = None,
                 priority: str = 'M',
                 owner: str = None,
                 project: str = None,
                 description: str = None,
                 status: str = "pending"):

        super(OwnedTask, self).__init__(
            tw,
            description=description,
            project=project,
            due=due,
            start=start,
            status=status,
            priority=priority)

        # Ensure that the task has a project defined...
        if not isinstance(project, str):
            error = f"Cannot create task -->{description}<-- due {due} without a valid project string"
            logger.critical(error)
            raise NotImplementedError(error)

        # The original tasklib.Task() instances do not have a self.tw attribute
        self.tw = tw
        self['due'] = due
        self['start'] = start
        self['status'] = status
        self['priority'] = priority

        self['description'] = description
        self.owner = self.set_owner(owner)

    def __repr__(self):
        return f"""<OwnedTask '{self['description']}' due: {self['due']} owner: {self.owner}>"""

    def __str__(self):
        return self.__repr__()

    @logger.catch(reraise=True)
    def __hash__(self):
        total = 0
        for value in self.__dict__.values():
            if isinstance(value, dict):
                for other in value.values():
                    if isinstance(other, set):
                        for item in other:
                            total += hash(item)
                    else:
                        total += hash(other)
            else:
                total += hash(value)
        return total

    @logger.catch(reraise=True)
    def get_depends(self):
        return self['depends']

    @logger.catch(reraise=True)
    def set_depends(self, value: List[Task]) -> LazyUUIDTaskSet:
        """
        Set the dependencies for this task
        """
        if isinstance(value, Sequence):
            for task in value:
                if not isinstance(task, Task):
                    error = f"{task} {type(task)} must be an instance of tasklib.Task()"
                    logger.critical(error)
                    raise ValueError(error)
            self['depends'] = LazyUUIDTaskSet(self.tw, [ii['uuid'] for ii in value])
            return self['depends']
        else:
            error = f"OwnedTaskWarrior().set_depends() requires a list of task instances, but got {type(value)}"
            logger.critical(error)
            raise NotImplementedError(error)

    @logger.catch(reraise=True)
    def get_owner(self) -> str:
        """
        :return: The value of the owner email from tags
        :rtype: str
        """
        for tag in self['tags']:
            if tag[0:7] == "owner=":
                return tag.split("=", 1)[1]

        # We could not find the owner tag...
        error = f"OwnedTask['uuid'] {self['uuid']} does not have an owner tag"
        logger.critical(error)
        raise NotImplementedError(error)

    @logger.catch(reraise=True)
    def set_owner(self, email_value: str) -> str:
        """
        Validate the owner's email address in ``email_value``, set an owner tag

        :return: The string owner email address
        :rtype: str
        """
        if isinstance(email_value, str):
            try:
                validate_email(email_value)
            except EmailNotValidError:
                error = f"{email_value} is not a valid email address"
                logger.critical(error)
                raise EmailNotValidError(error)
            except BaseException:
                error = f"{email_value} has some unexpected problem"
                logger.critical(error)
                raise NotImplementedError(error)
        else:
            error = "Email addresses must be a string"
            logger.critical(error)
            raise NotImplementedError(error)

        correct_owner_tag = f"owner={email_value}"
        for tag in self['tags']:
            if tag[0:7] == 'owner=':
                if tag == correct_owner_tag:
                    return correct_owner_tag
                else:
                    self['tags'].remove(tag)

        self['tags'].add(correct_owner_tag)
        return correct_owner_tag.split("=", 1)[1]


@attrs.define(repr=False)
class OwnedTaskWarrior(TaskWarrior):
    """
    A TaskWarrior() subclass that implements owned tasks.

    :param data_location: Directory where task data should be stored (required)
    :type data_location: str
    :param create: Whether the directory should be created, default to True.
    :type create: bool
    :param taskrc_location: Location where the taskrc is
    :type taskrc_location: str
    :param task_command: Name of the TaskWarrior command, default to 'task'
    :type task_command: str
    :param version_override: 
    :type version_override: bool
    :param purge_existing:  Whether to purge all existing tasks in the database, default to False
    :type purge_existing: bool
    """

    @logger.catch(reraise=True)
    def __init__(self, data_location=None, create=True,
                 taskrc_location=None, task_command='task',
                 version_override=None, purge_existing=False):
        TaskWarrior.__init__(self,
                             data_location=data_location,
                             create=create,
                             taskrc_location=taskrc_location,
                             task_command=task_command,
                             version_override=version_override)

        if not isinstance(self.tasks, TaskQuerySet):
            error = f"{self.tasks} {type(self.tasks)} must be a tasklib TaskQuerySet() instance"
            logger.critical(error)
            raise NotImplementedError(error)

        # Purge all existing tasks
        if purge_existing:
            for task in self.tasks:
                self.purge_task(task)
            self.reload_tasks()

    @logger.catch(reraise=True)
    def __hash__(self) -> int:
        """
        :return: An hash value that uniquely represents this ``OwnedTaskWarrior()`` collection
        :rtype: int
        """
        total = 0
        if self.tasks:
            for task in self.tasks:
                total += hash(task)
        return total

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self.tasks is not None:
            return f"""<OwnedTaskWarrior with {len(self.tasks)} OwnedTask() instances>"""
        else:
            return """<OwnedTaskWarrior with 0 OwnedTask() instances>"""

    def reload_tasks(self) -> None:
        """Reload tasks from disk"""
        self.tasks = TaskQuerySet(self)

    def delete_project(self, task: Task, project: str) -> None:
        """
        Delete all ``task`` instances associated with ``project`` (case-insensitive) from TaskWarrior().

        This method is an addition to the original ``tasklib`` API.
        """
        if self.tasks:
            for task in self.tasks:
                if task['project'].lower() == project.lower():
                    self.execute_command([task['uuid'], 'delete'])

    def purge_project(self, project: str) -> None:
        """
        Permanently remove all ``task`` instances associated with ``project`` (case-insensitive) from TaskWarrior().  This causes data loss.

        This method is an addition to the original ``tasklib`` API.
        """
        self.reload_tasks()
        if self.tasks:
            for task in self.tasks:
                if task['project'] == project:
                    self.execute_command([task['uuid'], 'delete'])
                    self.execute_command([task['uuid'], 'purge'])

    def purge_task(self, task):
        """
        Permanently remove the task from TaskWarrior().  This causes data loss.

        The task will not be completely purged until OwnedTaskWarrior() is re-loaded from disk.

        This method is an addition to the original ``tasklib`` API; it was submitted
        as ``tasklib`` github PR number 130.
        """
        self.execute_command([task['uuid'], 'delete'])
        self.execute_command([task['uuid'], 'purge'])

    def get_project(self, project: str) -> List[OwnedTask]:
        """
        :param project: Name of the project tasks to retrieve
        :type project: str
        :return: List of OwnedTask instances for the project
        :rtype: List[OwnedTask]
        """
        self.reload_tasks()

        retval = list()
        # sort tasks by start date
        tasks = sorted(self.tasks, key=lambda ii: ii['start'])
        for task in tasks:
            if task['project'] == project:
                owner = "__Unknown__"
                for tag in task['tags']:
                    if tag[0:6] == "owner=":
                        owner = tag.split("=", 1)[1]
                _task = OwnedTask(
                        description=task['description'],
                        project=task['project'],
                        owner=owner,
                        due=task['due'],
                        start=task['start'],)
                # Ensure all task attributes are copied over...
                _task.__dict__ = task.__dict__
                retval.append(_task)
        return retval

    @logger.catch(reraise=True)
    def get_task(self, uuid_value: str) -> OwnedTask:
        """
        :return: Walk the task database and return an OwnedTask() instance representing the UUID in ``uuid_value``, default to None
        :rtype: OwnedTask
        """

        for task in self.tasks:
            if task['uuid'] == uuid_value:

                # Ensure that the task has a project defined...
                if not isinstance(task['project'], str):
                    error = f"Cannot manage task {task['uuid']} without a valid project string"
                    logger.critical(error)
                    raise NotImplementedError(error)

                # Find the owner in the Task() tags and copy into
                # the new OwnedTask() instance
                for tag in task['tags']:
                    if tag[0:6] == "owner=":
                        owner = tag.split("=", 1)[1]
                        break

                owned_task = OwnedTask(tw=None,
                                       description=task['description'],
                                       project=task['project'],
                                       due=task['due'],
                                       owner=owner)
                # Take all the attributes of the Task instance and copy
                # into the new OwnedTask() instance.
                owned_task.__dict__ = task.__dict__
                return owned_task
        return None

    @logger.catch(reraise=True)
    def get_project_df(self, project: str) -> pd.DataFrame:
        """
        Get a project Gantt pandas DataFrame

        :return: A pandas DataFrame containing the tasks
        :rtype: pd.DataFrame
        """
        self.reload_tasks()

        # ref:
        #     https://www.datacamp.com/tutorial/how-to-make-gantt-chart-in-python-matplotlib
        #     (with customizations, below, required by TaskWarrior)

        tasks = self.get_project(project=project)
        if False:
            owners = [ii.owner for ii in tasks]

        # Build completion fractions based on task status...
        #     either pending or completed
        comp_fracs = []
        for task in tasks:
            if task['status'] == "pending":
                comp_fracs.append(0)
            else:
                comp_fracs.append(1)

        data = {
            "task": [ii['description'] for ii in tasks],
            "owner": [self.get_task(ii['uuid']).owner for ii in tasks],
            "start": [pd.to_datetime(ii['start']) for ii in tasks],
            "end": [pd.to_datetime(ii['due']) for ii in tasks],
            "status": [ii['status'] for ii in tasks],
            "completion_frac": comp_fracs,
        }
        df = pd.DataFrame(data)
        # Number of days from the project start to the start date
        # of each task
        df['days_to_start'] = (df['start'] - df['start'].min()).dt.days
        # Number of days from the project start to the end date
        # of each task
        df['days_to_end'] = (df['end'] - df['start'].min()).dt.days
        # Task duration in days
        df['task_duration'] = df['days_to_end'] - df['days_to_start'] + 1
        # The status of completion of each task translated from a
        # fraction into a portion of days allocated to that task
        df['completion_days'] = df['completion_frac'] * df['task_duration']

        return df

    def save_project_gantt_chart(self,
                                 project: str,
                                 filename: str = 'gantt.png') -> None:
        """
        Save the project Gantt chart as a file
        """
        ######################################################################
        # Consider using the unmaintained:
        #     https://xael.org/pages/python-gantt-en.html
        ######################################################################
        self.reload_tasks()

        tasks = self.get_project(project=project)
        owners = [ii.owner for ii in tasks]

        df = self.get_project_df(project)
        ######################################################################
        # Build a matplotlib gantt chart
        ######################################################################

        # There are hundreds of xkcd colors in the palette...
        # this is a small sample of the XKCD colors...
        all_colors = ["xkcd:red", "xkcd:orange", "xkcd:cyan", "xkcd:light purple", "xkcd:yellow", "xkcd:silver", "xkcd:tan", "xkcd:royal blue",]
        owner_colors = dict()

        # Assign a color for each owner...
        owners = sorted(set(owners))
        for idx, owner in enumerate(owners):
            color = all_colors[idx]
            owner_colors[owner] = color

        legend = list()
        # Assign colors to owners
        for owner in owner_colors.keys():
            legend.append(matplotlib.patches.Patch(color=owner_colors[owner]))

        # Access matplotlib subplots
        fig, ax = plt.subplots()
        # Get x-axis ticks for every Monday
        xticks = np.arange(5, df['days_to_end'].max() + 2, 7)
        # Apply each Monday tick labels (different than the axis tick itself)
        xticklabels = pd.date_range(
            start=df['start'].min() + dt.timedelta(days=4),
            end=df['end'].max()
        ).strftime("%Y-%m-%d")

        #####################################################################
        # Add a task bar for each task
        #####################################################################

        # Get a list of all DataFrame() row indexes
        df.sort_values(by='start')
        all_row_idxs = [idx for idx in df.index.values]
        # ensure longer tasks are sorted before shorter tasks...
        for idx, old_index in enumerate(all_row_idxs):
            if idx == len(all_row_idxs) - 1:
                continue
            index = df.iloc[old_index]
            old_dfrow = df.iloc[old_index]
            new_dfrow = df.iloc[old_index + 1]
            if old_dfrow['task_duration'] > new_dfrow['task_duration']:
                all_row_idxs[idx], all_row_idxs[idx + 1] = all_row_idxs[idx + 1], all_row_idxs[idx]

        # Move the last dfrow to the first (after the buggy sort, above)
        last_idx = all_row_idxs[-1]
        del all_row_idxs[-1]
        all_row_idxs.insert(0, last_idx)

        for idx in all_row_idxs:
            dfrow = df.iloc[idx]
            if dfrow['status'] != "completed":
                plt.barh(y=dfrow['task'], width=dfrow['task_duration'],
                         left=dfrow['days_to_start'] + 1,
                         color=owner_colors[dfrow['owner']],
                         edgecolor="none")
            else:
                plt.barh(y=dfrow['task'], width=dfrow['task_duration'],
                         left=dfrow['days_to_start'] + 1,
                         color=owner_colors[dfrow['owner']],
                         edgecolor="xkcd:black",
                         hatch="//",)

        # Put a vertical line on the chart for today
        if False:
            # This is broken, it squashes all tasks
            ax.axvline(dt.datetime.now(), linestyle="dashed")

        # Put tasks in chronological order
        plt.gca().invert_yaxis()
        plt.title(f'Schedule for the {project} Project', fontsize=16)

        # Apply the x-axis ticks, defined above...
        ax.set_xticks(xticks)
        # Set weekly tick intervals
        ax.set_xticklabels(xticklabels[::7])
        # Show vertical lines for each week
        ax.xaxis.grid(True, alpha=0.5)
        # Set x-axis label font size
        #       https://stackoverflow.com/a/29074915/667301
        ax.tick_params(labelsize=10)
        ax.set_xlabel("Mondays [YYYY-MM-DD] (shading: Task completed)")
        # Rotate x-tick labels to 90 degrees to avoid overlap
        #       https://stackoverflow.com/a/37708190/667301
        plt.xticks(rotation=90)


        # Add a legend of task owners
        ax.legend(handles=legend, labels=owner_colors.keys(), fontsize=11)

        # https://stackoverflow.com/a/9890599/667301
        plt.savefig(filename, bbox_inches='tight')


    @logger.catch(reraise=True)
    def get_table(self, max_width=80) -> str:
        """
        :param max_width: The maximum table width without wrapping cells
        :type max_width: int
        :return: A string task table rendering
        :rtype: str
        """
        # Reload tasks from disk
        self.reload_tasks()

        all_tasks = list()
        table = texttable.Texttable(max_width=max_width)
        table.set_deco(texttable.Texttable.HEADER)
        table.set_cols_dtype(["t", "t", "i", "t", "t", "t"])
        table.set_cols_align(["l", "l", "l", "l", "l", "l"])

        # Append a list of titles
        all_tasks.append(["uuid", "due", "depends", "owner", "project", "description"])
        if self.tasks:
            for task in self.tasks:
                owner = None
                for tag in task['tags']:
                    if tag[0:6] == "owner=":
                        owner = tag.split("=", 1)[1]
                all_tasks.append([task['uuid'], task['due'], len(task['depends']), owner, task['project'], task['description']])
        table.add_rows(all_tasks)
        return table.draw()
