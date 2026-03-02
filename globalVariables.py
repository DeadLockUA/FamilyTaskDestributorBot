
import logging

# One-time configuration 
logging.basicConfig(
    level=logging.WARNING,                     
    #format='%(asctime)s  %(levelname)-7s  %(name)s  %(filename)s:%(lineno)d  %(funcName)s()  →  %(message)s',
    format='%(asctime)s %(filename)s:%(lineno)d  →  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

task_selection_states = (                                                   #Task in progress
    "CREATE_TASK",
    "MY_TASKS"
)

task_creation_states = (                                                    #Steps in sequence to create tasks
    "WAITING_FOR_TASK_NAME",
    "WAITING_FOR_TASK_DESCRIPTION"
    "WAITING_FOR_RESPONSIBLE",
    "WAITING_FOR_DEADLINE",
    "WAITING_FOR_PRIORITY"
)

user_states = {                                                             #Store information about current user state and information he provided
    12345: {
        "task": "CREATE_TASK",
        "step": "WAITING_FOR_TASK_NAME",
        "task_data": {
            "title":"TemplateTask",
            "owner_id": 22222,
            "creator_id" : 12345,
            "deadline":"01.01.2027",
            "status" : 0,
            "priority" : 5,

        }
    }
}