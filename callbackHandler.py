import DBHandler,messageHandler
from globalVariables import logger
from telegram import Update
from telegram.ext import ContextTypes
from supportTools import log,send_to_user
from globalVariables import task_creation_states,task_selection_states,user_states
from DBHandler import get_tasks_by_user_id,get_user_name_by_telegram_id,get_open_tasks_by_user_id,get_task_by_task_id
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from supportTools import log,send_to_user,get_task_menu_markup,get_support_menu_markup
from commandHandler import show_help_menu



async def button_handler(update: Update,context: ContextTypes.DEFAULT_TYPE):

    logger.warning("Entering callback_handler")
    query = update.callback_query

    await query.answer()  

    data = query.data
    action = data.split(":")[0]

    logger.warning(f"Button_Pressed: {data}")


    #check if user is already in a dialog state
    logger.warning("Checking user_states")
    user_id = update.effective_user.id
    if user_id not in user_states:
        logger.warning("user_id not in user_states") 

        if action == "create_task":
            logger.warning("action create_task") 
            await create_task(update)  

        elif action == "get_my_tasks_menu":
            logger.warning("action get_my_tasks_menu") 
            await get_my_tasks_menu(update)
        
        elif action == "show_my_task_history":
            logger.warning("action show_my_task_history") 
            await show_my_task_history(update)

        elif action == "show_my_task_list":
            logger.warning("action show_my_task_list") 
            await show_my_task_list(update)

        elif action == "change_task_status":
            logger.warning("action change_task_status") 
            await change_task_status(update,data.split(":")[1])

        elif action == "complete_task":
            logger.warning("action complete_task") 
            await complete_task(update,data.split(":")[1])
        
        elif action == "review_task":
            logger.warning("action review_task") 
            await review_task(update,data.split(":")[1])

        elif action == "/help":
            await show_help_menu(update)      

        else:
            logger.warning("unknown action") 
            await messageHandler.reset_dialog (update)
    else:
        logger.warning("user_id is in user_states") 

        if action == "set_responsible":
            logger.warning("action set_responsible") 
            await set_responsible(update,data.split(":")[1])

        elif action == "set_priority":
            logger.warning("action set_priority") 
            await set_priority(update,data.split(":")[1]) 
        else:
            logger.warning("unknown action") 
            await messageHandler.reset_dialog (update)


async def create_task(update: Update):
    logger.warning("create_task")
    user_id = update.effective_user.id
    user_states[user_id] = {
        "task": task_selection_states[0],           #CREATE_TASK
        "step": task_creation_states[0],            #WAITING_FOR_TASK_NAME
        "task_data": {}
    }
    await update.callback_query.edit_message_text("Creating new task. Please enter task name:")

async def get_my_tasks_menu (update: Update):
    logger.warning("get_my_tasks_menu")

    reply_markup = InlineKeyboardMarkup(get_task_menu_markup().inline_keyboard)
    #await update.message.reply_text("Please, select priority:", reply_markup=reply_markup)
    await update.effective_chat.send_message("Please, select action:", reply_markup=reply_markup)


async def show_my_task_history(update: Update):
    logger.warning("show_my_task_history")
    user_id = update.effective_user.id
    tasks = get_tasks_by_user_id(user_id)

    if not tasks:
        await send_to_user(
            update,
            "📭 You don't have any tasks assigned to you at the moment."
        )
        return

    # Prepare message
    lines = ["📋 **Your tasks:**\n"]

    for task in tasks:
        task_id     = task['id']
        title       = task['title']
        creator_id  = task['creator_id']
        deadline    = task['deadline'] or "—"
        status      = task['status']
        priority    = task['priority']

        
        creator_name = get_user_name_by_telegram_id(creator_id)

        
        priority_emojis = ["🔴", "🟠", "🟡", "🟢", "🔵"]
        prio_emoji = priority_emojis[min(priority, 4)] if priority is not None else "⚪"

        
        status_text = {
            0: "🆕 New",
            1: "✅ Completed",
            2: "❌ Cancelled",
        }.get(status, f"Status {status}")

        
        line = (
            f"#{task_id}  {prio_emoji} **{title}**\n"
            f"   • From: {creator_name}\n"
            f"   • Deadline: {deadline}\n"
            f"   • {status_text}\n"
        )
        lines.append(line)

    # Final message
    message = "\n".join(lines).strip()

    await send_to_user(update, message)
    await messageHandler.reset_dialog (update)


async def show_my_task_list (update: Update):
    logger.warning("show_my_task_list")

    user_id = update.effective_user.id
    tasks = get_open_tasks_by_user_id(user_id)

    if not tasks:
        await send_to_user(
            update,
            "📭 You don't have any tasks assigned to you at the moment."
        )
        return
      

    keyboard = []
    for task in tasks:
        title = task["title"]
        callback_data="change_task_status:"+str(task["id"])
        button = InlineKeyboardButton (text= title, callback_data= callback_data)
        keyboard.append([button])

    keyboard.append(*get_support_menu_markup().inline_keyboard)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await send_to_user(update, "Please, select task to review:", reply_markup=reply_markup)
    
    
async def change_task_status(update: Update,  taskId:str):
    logger.warning(f"change_task_status: {taskId}")
    task = get_task_by_task_id (taskId)
    #deadline = task.get("deadline")
    owner = task["owner_id"]    

    message_text = (
        f"Title: {task['title']}\n"
        f"Owner: {owner}\n\n"
        f"Select action:"
    )

    keyboard = [
        [
            InlineKeyboardButton("🔍 Review task", callback_data="review_task:"+taskId),
            InlineKeyboardButton("✅ Finish task", callback_data="complete_task:"+taskId)
        ],
        *get_support_menu_markup().inline_keyboard 
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await send_to_user(update, message_text, reply_markup=reply_markup)

async def review_task(update: Update,  taskId:str):
    logger.warning(f"review_task: {taskId}")
    task = get_task_by_task_id (taskId)
    title = task["title"]    
    description = task["description"]
    owner_id = task["owner_id"]
    owner_name = get_user_name_by_telegram_id(owner_id) 
    creator_id = task["creator_id"]
    creator_name = get_user_name_by_telegram_id(creator_id)
    deadline = task["deadline"]
    status = task["status"]
    status_text = {
            0: "🆕 New",
            1: "✅ Completed",
            2: "❌ Cancelled",
        }.get(status, f"Status {status}")
    
    priority = task["priority"]

    message = f"Task: {title}\n\nCreator: {creator_name}\n\nDeadline: {deadline}\n\n\n\nDescripton: \n\n{description}"

    keyboard = [
        [
            InlineKeyboardButton("⬅️ Back", callback_data="show_my_task_list"),
            InlineKeyboardButton("✅ Finish task", callback_data="complete_task:"+taskId)
        ],
        # Reuse the support row upacked
        *get_support_menu_markup().inline_keyboard 

    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await send_to_user (update, message, reply_markup=reply_markup)
    



async def complete_task(update: Update,  taskId:str):
    logger.warning(f"complete_task: {taskId}")
    DBHandler.update_task_status(taskId,1)
    await messageHandler.reset_dialog(update, "Task successfully closed 👍\n\nWhat would you like to do next?")
    
    


async def set_responsible(update: Update,  responsible:str):
    logger.warning(f"set_responsible: {responsible}")

    user_id = update.effective_user.id
    user_states[user_id]["task_data"]["owner_id"] = responsible
    user_states[user_id]["step"] = task_creation_states[2] #setting state to WAITING_FOR_DEADLINE
    await update.callback_query.edit_message_text(f"Task is assigned to: {DBHandler.get_user_name_by_telegram_id(responsible)}")
    await send_to_user(update,f"Please set a deadline:")

async def set_priority (update: Update,  priority:str):
    logger.warning(f"set_priority: {priority}")

    user_id = update.effective_user.id
    task_data = user_states[user_id]['task_data']

    task_data["priority"] = priority    
    await update.callback_query.edit_message_text(f"Priority is set to: {priority}")

    #Now finish creating task!
    task_data = user_states[user_id]['task_data']


    logger.warning(", ".join(f"{key}: {value}" for key, value in task_data.items()))    

    DBHandler.add_task(
        task_data['title'],
        task_data['description'],
        task_data['owner_id'],
        user_id,
        task_data['deadline'],
        task_data['priority']
    )
    user_states.pop(update.effective_user.id, None)

    task_summary=f"""Task summary
    📋Task title: " {task_data['title']}
    👥For whom: {DBHandler.get_user_name_by_telegram_id(task_data['owner_id'])}
    ⌛Deadline: {str(task_data['deadline']).split('.')[0]}
    🏃‍♂️‍➡️Priority: {task_data['priority']}
    
    Task created and assigned successfully 😁
    """
    await send_to_user (update,task_summary)
    await messageHandler.reset_dialog(update, "What would you like to do next?")
