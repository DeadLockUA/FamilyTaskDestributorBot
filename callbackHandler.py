import DBHandler,messageHandler
from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from supportTools import log,send_to_user
from globalVariables import task_creation_states,task_selection_states,user_states


async def button_handler(update: Update,context: ContextTypes.DEFAULT_TYPE):

    log("Entering button_handler")
    query = update.callback_query

    await query.answer()  

    data = query.data
    action = data.split("/")[0]

    log(f"Button_Pressed: {data}")

    #Here are actions for main menu buttons:
    if action == "create_task":
        log("action create_task") 
        await create_task(update)       

    elif action == "my_tasks":
        await query.edit_message_text("Here are your tasks 📋")

    #Below are actions on responsible selection during creation of task

    elif action == "set_responsible":
        log("action set_responsible") 
        await set_responsible(update,data.split("/")[1])

    elif action == "set_priority":
        log("action set_priority") 
        await set_priority(update,data.split("/")[1]) 


async def create_task(update: Update):
    log("create_task")
    user_id = update.effective_user.id
    user_states[user_id] = {
        "task": task_selection_states[0],           #CREATE_TASK
        "step": task_creation_states[0],            #WAITING_FOR_TASK_NAME
        "task_data": {}
    }
    await update.callback_query.edit_message_text("Creating new task. Please enter task name:")



async def set_responsible(update: Update,  responsible:str):
    log(f"set_responsible: {responsible}")

    user_id = update.effective_user.id
    user_states[user_id]["task_data"]["owner_id"] = responsible
    user_states[user_id]["step"] = task_creation_states[2] #setting state to WAITING_FOR_DEADLINE
    await update.callback_query.edit_message_text(f"Task is assigned to: {DBHandler.get_user_by_telegram_id(responsible)['name']}")
    await send_to_user(update,f"Please set a deadline:")

async def set_priority (update: Update,  priority:str):
    log(f"set_priority: {priority}")

    user_id = update.effective_user.id
    task_data = user_states[user_id]['task_data']

    task_data["priority"] = priority    
    await update.callback_query.edit_message_text(f"Priority is set to: {priority}")

    #Now finish creating task!
    task_data = user_states[user_id]['task_data']

    log(f"""Creating task with next parameters
    {task_data['title']}
    {task_data['owner_id']}
    {user_id}
    {task_data['deadline']}
    {task_data['priority']}
    """)

    DBHandler.add_task(
        task_data['title'],
        task_data['owner_id'],
        user_id,
        task_data['deadline'],
        task_data['priority']
    )
    user_states.pop(update.effective_user.id, None)
    await send_to_user (update,"Task created and assigned successfully 😁")


