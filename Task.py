import math

class Task:
    def __init__(self, task_id: int, deadline: int, duration: int, perfect_benefit: float) -> None:
        """
        Creates a new task with the corresponding task_id,
        deadline, duration, and perfect_benefit

        Args: 
        - task_id (int): task id of the Task
        - deadline (int): deadline of the Task
        - duration (int): duration of the Task
        - perfect_benefit (float): the benefit recieved from
        completing the Task anytime before (or on) the deadline

        Output:
        - Task object: corresponding Task object

        Sample usage:
        >>> import Task
        >>> task0 = Task.Task(0, 1, 2, 3.0)
        >>> print(task0)
        Task 0 has deadline 1, duration 2, and max benefit 3
        """
        self.task_id = task_id
        self.deadline = deadline
        self.duration = duration
        self.perfect_benefit = perfect_benefit
        
    def get_task_id(self) -> int:
        """ 
        Returns the task id of this Task 

        Sample usage:
        >>> task0.get_task_id()
        0
        """
        return self.task_id

    def get_deadline(self) -> int:
        """ 
        Returns the start time of this Task 

        Sample usage:
        >>> task0.get_deadline()
        1
        """
        return self.deadline

    def get_duration(self) -> int:
        """ 
        Returns the duration of this task 
    
        Sample usage:
        >>> task0.get_duration()
        2
        """
        return self.duration
    
    def get_max_benefit(self) -> int:
        """ 
        Returns the max possible benefit recievable from this task 
        which is equal to the benefit recieved from completing 
        this task any time before (or on) the deadline

        Sample usage:
        >>> task0.get_max_benefit()
        3
        """
        return self.perfect_benefit

    def get_late_benefit(self, minutes_late: int) -> int:
        """
        Returns the benefit recieved from completing this task
        minutes_late minutes late

        Sample usage:
        >>> task0.get_late_benefit(0)
        3.0
        >>> task0.get_late_benefit(5)
        2.7555368532043722
        >>> task0.get_late_benefit(30)
        1.8014867364367977
        """
        minutes_late = max(0, minutes_late)
        return self.get_max_benefit() * math.exp(-0.0170 * minutes_late)
    
    def hypothetical_gain(self, time):
        """[summary]

        Args:
            time (int): Current time of the day.

        Returns:
            The hypothetical gain of doing this specific task at the given time of the day.
        """
        return self.get_late_benefit(time + self.get_duration() - self.get_deadline())
    
    def calculate_weight_1(self, time):
        """[summary]
        Divide by duration of task to prioritize tasks that take shorter time
        """
        return self.hypothetical_gain(time)/self.get_duration()
    
    def calculate_weight_2(self, time):
        """[summary]
        Divide by duration of task to prioritize tasks that take shorter time and take in account of deadline closeness as well as efficiency
        """
        return self.weight_gain(time) * self.weight_efficiency() * self.weight_urgency(time)
    
    def weight_gain(self, time):
        return self.hypothetical_gain(time) / 100

    def weight_urgency(self, time):
        return max(0, 0.1/(0.1 + self.get_deadline() - self.get_duration() - time))
    
    def weight_efficiency(self):
        return self.get_max_benefit() / self.get_duration()
    
    def heuristic(self, time, c1, c2, c3):
        return self.weight_gain(time) * c1 + self.weight_urgency(time) * c2 + self.weight_efficiency() * c3

    def __str__(self):
        """
        Generates a readable string representation of a task

        Sample usage:
        >>> str(task0)
        Task 0 has deadline 1, duration 2, and max benefit 3.0
        """
        return "Task {} has deadline {}, duration {}, and max benefit {}".format(self.get_task_id(), self.get_deadline(), self.get_duration(), self.get_max_benefit())
