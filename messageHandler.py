import DBHandler
from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from supportTools import log,send_to_user,parse_deadline,get_main_menu_markup
from globalVariables import task_creation_states,task_selection_states,user_states




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

    #register new user if not in DB
    if not DBHandler.get_user_by_telegram_id(user_id):                          
        await send_to_user(update, "You are here first time? Welcome! For more details type /Start")                    
        log(f"New user detected. Registering new user: {user_id}, {update.effective_user.full_name} as regular user")
        DBHandler.add_user(user_id, update.effective_user.full_name, "User")
    
    #check if user is already in a dialog state
    log("Checking user_states")
    if user_id in user_states:
        user_step = user_states[user_id]["step"]
        user_task = user_states[user_id]["task"]
        log(f"user_state: {user_step}")
        await process_user_dialog(update,user_task,user_step)

    else:
        log("user_states do not exist.Requesting for action")
        await reset_dialog (update)


async def reset_dialog(update: Update, reset_dialog_request: str = ""):
    log("resetting dialog. Sending new dialog window")
    
    # Resetting user state safely.
    user_states.pop(update.effective_user.id, None)
    
    if reset_dialog_request:
        #FUTURE IMPROVEMENT: send_to_user have to support effective_chat / effective_user
        await send_to_user(update, reset_dialog_request)    

    await update.effective_chat.send_message(text="Select option:", reply_markup=get_main_menu_markup())


async def process_user_dialog (update: Update, task: str, step: str):
    log ("processing user dialog")
    if task == task_selection_states[0]:         #CREATE_TASK
        log(f"Task {task} - Processing CREATE_TASK")
        await process_task_creation_dialog (update,step)
    elif task == task_selection_states[1]:       #MY_TASKS
        log(f"Task {task} - Processing MY_TASKS")
        await process_my_tasks_dialog (update,step)
    else:
        log(f"Task {task} - is unknown. reseting dialog")
        await reset_dialog (update,"Something went wrong. Lets start from beginning.")


async def process_task_creation_dialog (update: Update, step: str):
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
            user_states[user_id]["step"] = task_creation_states[1] #setting state to WAITING_FOR_RESPONSIBLE
            log(f"requesting for responsible")         

            list_of_resposibles = [
            InlineKeyboardButton(
                user["name"],                 # button text
                callback_data="set_responsible/"+str(user["telegram_id"]) # callback must be string!
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


    elif step == task_creation_states[1]:         #WAITING_FOR_RESPONSIBLE - This state should not be reachable. Something wrong, just for debug purposes
        log(f"Step {step}")
        log(f"!!!!!!!!!!!!!! This step shoul be skipped as it is handled in button callback!!!!!!!!!")

    elif step == task_creation_states[2]:         #WAITING_FOR_DEADLINE
        log(f"Step {step}")
        deadline = parse_deadline(user_text)
        log(f"User deadline is {deadline}")
        await send_to_user(update, f"Deadline: {deadline}")

        if deadline is None:
            log("Requesting again")
            await send_to_user(update,"❌ Invalid format.\n\nUse:\n1h, 2d, 3m, 4y\nor\nDD-MM-YYYY (e.g. 12-02-2029)")
        else:
            log(f"Updating states. Task_data.deadline = {deadline}")
            user_states[user_id]["task_data"]["deadline"] = deadline
            user_states[user_id]["step"] = task_creation_states[3] #setting state to WAITING_FOR_PRIORITY
            log(f"requesting for priority")  


            keyboard = [
                [
                    InlineKeyboardButton("🔴 0 - Super Urgent", callback_data="set_priority/0"),
                ],
                [
                    InlineKeyboardButton("🟠 1 - High", callback_data="set_priority/1"),
                ],
                [
                    InlineKeyboardButton("🟡 2 - Medium", callback_data="set_priority/2"),
                ],
                [
                    InlineKeyboardButton("🟢 3 - Low", callback_data="set_priority/3"),
                ],
                [
                    InlineKeyboardButton("🔵 4 - Relaxed", callback_data="set_priority/4")
                ],
                [
                    InlineKeyboardButton("❓ Help", callback_data="/help"),
                    InlineKeyboardButton("📋 return to Menu", callback_data="/start")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Please, select priority:", reply_markup=reply_markup)




    elif step == task_creation_states[3]:         #WAITING_FOR_PRIORITY - This state should not be reachable. Something wrong, just for debug purposes
        log(f"Step {step}")
        log(f"!!!!!!!!!!!!!! This step shoul be skipped as it is handled in button callback!!!!!!!!!")



    else:
        log(f"Step {step} - is unknown. reseting dialog")
        await reset_dialog (update,"Something went wrong. Lets start from beginning.")




async def process_my_tasks_dialog (update: Update, step: str):
    log ("processing process_my_tasks_dialog dialog")



    


    

    