import DBHandler
from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from communication_handler import log,send_to_user

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


#Task should contain:
#unique id
#Title - text
#OwnerID - int
#CreatorID - int
#Deadline - text
#Status - int
#Priority -int

async def reset_user_states (user_id: int):
    del user_states[user_id]
    


task_selection_states = (                                                   #Task in progress
    "CREATE_TASK",
    "MY_TASKS"
)

task_creation_states = (                                                    #Steps in sequence to create tasks
    "WAITING_FOR_TASK_NAME",
    "WAITING_FOR_RESPONSIBLE",
    "WAITING_FOR_DEADLINE",
    "WAITING_FOR_PRIORITY"
)


async def message_handler_default(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not DBHandler.get_user_by_telegram_id(user_id):                          #If user is unknown - register gim into DB
        await send_to_user(update, "You are here first time? Welcome! For more details type /Start")                    
        log(f"New user detected. Registering new user: {user_id}, {update.effective_user.full_name} as regular user")
        DBHandler.add_user(user_id, update.effective_user.full_name, "User")
    
    log("Checking user_states")
    if user_id in user_states:
        user_step = user_states[user_id]["step"]
        user_task = user_states[user_id]["task"]
        log(f"user_state: {user_step}")
        await process_user_dialog(update,context,user_task,user_step)

    else:
        log("user_states do not exist.Requesting for action")
        await reset_dialog (update,context,"Please, select desired action")



async def reset_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE, reset_dialog_request:str):
    log("resetting dialog")
    await send_to_user(update,reset_dialog_request)
    log("sending dialog window")
    await show_menu (update,context)


async def process_user_dialog (update: Update, context: ContextTypes.DEFAULT_TYPE,task: str , step: str):
    log ("processing user dialog")
    if task == task_selection_states[0]:         #CREATE_TASK
        log(f"Task {task} - Processing CREATE_TASK")
        await process_task_creation_dialog (update,context,step)
    elif task == task_selection_states[1]:       #MY_TASKS
        log(f"Task {task} - Processing MY_TASKS")
        await process_my_tasks_dialog (update,context,step)
    else:
        log(f"Task {task} - is unknown. reseting dialog")
        await reset_dialog (update,context,"Something went wrong. Lets start from beginning.")


async def process_task_creation_dialog (update: Update, context: ContextTypes.DEFAULT_TYPE, step: str):
    log ("processing process_task_creation_dialog dialog")
    user_id = update.effective_user.id
    user_text = update.message.text
    
    
    if step == task_creation_states[0]:           #WAITING_FOR_TASK_NAME
        log(f"Step {step} - Processing WAITING_FOR_TASK_NAME")

        if len(user_text) < 5 or len(user_text) > 30:
            log(f"Improper name length, requesting again")
            await send_to_user(update,"Task name should be longer then 5 and shorter then 50 symbols")
        else:
            log(f"Updating states. Task_data.title = {user_text}")
            user_states[user_id]["task_data"]["title"] = user_text
            user_states[user_id]["step"] = task_creation_states[1]
            log(f"requesting for responsible")         

            list_of_resposibles = [
            InlineKeyboardButton(
                user["name"],                 # button text
                callback_data="select_responsible/"+str(user["telegram_id"]) # callback must be string!
                ) for user in DBHandler.get_all_users()
            ]

            keyboard = [
                list_of_resposibles,
                [
                    InlineKeyboardButton("❓ Help", callback_data="/help"),
                    InlineKeyboardButton("📋 return to Menu", callback_data="/start")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Please, select responsible:", reply_markup=reply_markup)


    elif step == task_creation_states[1]:         #WAITING_FOR_RESPONSIBLE
        log(f"Step {step} - Processing WAITING_FOR_RESPONSIBLE")
        log(f"Assigned responsible = {user_text}")
    elif step == task_creation_states[2]:         #WAITING_FOR_DEADLINE
        log(f"Step {step} - Processing WAITING_FOR_DEADLINE")
    elif step == task_creation_states[3]:         #WAITING_FOR_PRIORITY
        log(f"Step {step} - Processing WAITING_FOR_PRIORITY")
    else:
        log(f"Step {step} - is unknown. reseting dialog")
        await reset_dialog (update,context,"Something went wrong. Lets start from beginning.")




async def process_my_tasks_dialog (update: Update, context: ContextTypes.DEFAULT_TYPE, step: str):
    log ("processing process_my_tasks_dialog dialog")





async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("👥 Assign new task", callback_data="create_task"),
            InlineKeyboardButton("📋 My Tasks", callback_data="my_tasks")
        ],
        [
            InlineKeyboardButton("❓ Help", callback_data="help")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    log("Entering button_handler")
    query = update.callback_query

    await query.answer()  

    data = query.data

    log(f"Button_Pressed: {data}")
    if data == "create_task":
        log("Starting to handle create_task button")
        user_id = update.effective_user.id
        user_states[user_id] = {
            "task": task_selection_states[0],           #CREATE_TASK
            "step": task_creation_states[0],            #WAITING_FOR_TASK_NAME
            "task_data": {}
        }
        await query.edit_message_text("Please enter task name:")

        # log("checking if there was previous state")
        # if step in task_creation_states:
        #      log(f"Previous state was{task_creation_states(position)}")
        #      position = task_creation_states.index(step)
        #      position+=1
        #      log(f"Next state will be{task_creation_states(position)}")
        # else:
        #      log(f"Previous state was absent")
        #      position = 0
        #      log(f"Next state will be{task_creation_states(position)}")



        
        
        

    elif data == "my_tasks":
        await query.edit_message_text("Here are your tasks 📋")

    elif data == "help":
        await query.edit_message_text("Help section ❓")

    

    