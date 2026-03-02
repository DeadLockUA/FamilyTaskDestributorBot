import DBHandler
from globalVariables import logger
from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from supportTools import log,send_to_user,parse_deadline,get_main_menu_markup,get_support_menu_markup,get_priority_markup
from globalVariables import task_selection_states,user_states






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
    

async def message_handler(update: Update,context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

  
    user_name = DBHandler.get_user_name_by_telegram_id(user_id)
    if user_name == "Unknown user":
        # this is a new user
        await send_to_user(update, "You are here first time? Welcome! ...")
        logger.warning(f"New user detected: {user_id} ...")
        DBHandler.add_user(user_id, update.effective_user.full_name, "User")


    
    #check if user is already in a dialog state
    logger.warning("Checking user_states")
    if user_id in user_states:
        user_step = user_states[user_id]["step"]
        user_task = user_states[user_id]["task"]
        logger.warning(f"user_state: {user_step}")
        await process_user_dialog(update,user_task,user_step)

    else:
        logger.warning("user_states do not exist.Requesting for action")
        await reset_dialog (update)


async def reset_dialog(update: Update, reset_dialog_request: str = ""):
    logger.warning("resetting dialog. Sending new dialog window")
    
    # Resetting user state safely.
    user_states.pop(update.effective_user.id, None)
    
    if reset_dialog_request:
        await send_to_user(update, reset_dialog_request)    

    await update.effective_chat.send_message(text="Select option:", reply_markup=get_main_menu_markup())


async def process_user_dialog (update: Update, task: str, step: str):
    logger.warning("processing user dialog")
    if task == task_selection_states[0]:         #CREATE_TASK
        logger.warning(f"Task {task} - Processing CREATE_TASK")
        await process_task_creation_dialog (update,step)
    elif task == task_selection_states[1]:       #MY_TASKS
        logger.warning(f"Task {task} - Processing MY_TASKS")
        await process_my_tasks_dialog (update,step)
    else:
        logger.warning(f"Task {task} - is unknown. reseting dialog")
        await reset_dialog (update,"Something went wrong. Lets start from beginning.")


async def process_task_creation_dialog (update: Update, step: str):
    logger.warning("processing process_task_creation_dialog dialog")
    user_id = update.effective_user.id
    user_text = update.message.text
    
    
    if step == "WAITING_FOR_TASK_NAME":
        logger.warning(f"Step {step} - Processing WAITING_FOR_TASK_NAME")

        if len(user_text) < 5 or len(user_text) > 30:
            logger.warning(f"Improper name length, requesting again")
            await send_to_user(update,"Task name should be longer then 5 and shorter then 50 symbols")
        else:
            logger.warning(f"Updating states. Task_data.title = {user_text}")
            user_states[user_id]["task_data"]["title"] = user_text
            user_states[user_id]["step"] = "WAITING_FOR_TASK_DESCRIPTION" 
            logger.warning(f"requesting for task description")           
            await send_to_user (update, "Please, describe the task")   



    
    elif step == "WAITING_FOR_TASK_DESCRIPTION":
        logger.warning(f"Step {step} - Processing WAITING_FOR_TASK_DESCRIPTION")

        if len(user_text) > 1000:
            logger.warning(f"Improper name length, requesting again")
            await send_to_user(update,"Task descrition should be shorter then 1000 symbols")
        else:
            logger.warning(f"Updating states. Task_data.description = {user_text}")
            user_states[user_id]["task_data"]["description"] = user_text
            user_states[user_id]["step"] = "WAITING_FOR_RESPONSIBLE" 

            list_of_resposibles = [
            InlineKeyboardButton(
                user["name"],                 # button text
                callback_data="set_responsible/"+str(user["telegram_id"]) # callback must be string!
                ) for user in DBHandler.get_all_users()
            ]

            keyboard = [list_of_resposibles,*get_support_menu_markup().inline_keyboard]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Please, select responsible:", reply_markup=reply_markup)


    elif step == "WAITING_FOR_DEADLINE":         
        logger.warning(f"Step {step}")
        deadline = parse_deadline(user_text)
        logger.warning(f"User deadline is {deadline}")
        await send_to_user(update, f"Deadline: {deadline}")

        if deadline is None:
            logger.warning("Requesting again")
            await send_to_user(update,"❌ Invalid format.\n\nUse:\n1h, 2d, 3m, 4y\nor\nDD-MM-YYYY (e.g. 12-02-2029)")
        else:
            logger.warning(f"Updating states. Task_data.deadline = {deadline}")
            user_states[user_id]["task_data"]["deadline"] = deadline
            user_states[user_id]["step"] = "WAITING_FOR_PRIORITY" 
            logger.warning(f"requesting for priority")  

            reply_markup = InlineKeyboardMarkup(get_priority_markup().inline_keyboard)
            await update.message.reply_text("Please, select priority:", reply_markup=reply_markup)


    else:
        logger.warning(f"Step {step} - is unknown. reseting dialog")
        await reset_dialog (update,"Something went wrong. Lets start from beginning.")




async def process_my_tasks_dialog (update: Update, step: str):
    log ("processing process_my_tasks_dialog dialog")



    


    

    