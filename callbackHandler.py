import DBHandler,messageHandler
from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from supportTools import log,send_to_user
from globalVariables import task_creation_states,task_selection_states,user_states
from DBHandler import get_tasks_by_user_id,get_user_name_by_telegram_id


async def button_handler(update: Update,context: ContextTypes.DEFAULT_TYPE):

    log("Entering callback_handler")
    query = update.callback_query

    await query.answer()  

    data = query.data
    action = data.split("/")[0]

    log(f"Button_Pressed: {data}")


    #check if user is already in a dialog state
    log("Checking user_states")
    user_id = update.effective_user.id
    if user_id not in user_states:
        log("user_id not in user_states") 

        if action == "create_task":
            log("action create_task") 
            await create_task(update)  
        elif action == "my_tasks":
            log("action my_tasks") 
            await get_my_tasks(update)
        else:
            log("unknown action") 
            await messageHandler.reset_dialog (update)
    else:
        log("user_id is in user_states") 

        if action == "set_responsible":
            log("action set_responsible") 
            await set_responsible(update,data.split("/")[1])

        elif action == "set_priority":
            log("action set_priority") 
            await set_priority(update,data.split("/")[1]) 
        else:
            log("unknown action") 
            await messageHandler.reset_dialog (update)


async def create_task(update: Update):
    log("create_task")
    user_id = update.effective_user.id
    user_states[user_id] = {
        "task": task_selection_states[0],           #CREATE_TASK
        "step": task_creation_states[0],            #WAITING_FOR_TASK_NAME
        "task_data": {}
    }
    await update.callback_query.edit_message_text("Creating new task. Please enter task name:")

#async def get_my_tasks (update: Update):

async def get_my_tasks(update: Update):
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

        # Get creator's name (using your existing helper)
        creator_name = get_user_name_by_telegram_id(creator_id)

        # Priority emoji
        priority_emojis = ["🔴", "🟠", "🟡", "🟢", "🔵"]
        prio_emoji = priority_emojis[min(priority, 4)] if priority is not None else "⚪"

        # Simple status text – customize as you wish
        status_text = {
            0: "🆕 New",
            1: "🔄 In progress",
            2: "✅ Completed",
            3: "❌ Cancelled",
        }.get(status, f"Status {status}")

        # One task line
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




async def set_responsible(update: Update,  responsible:str):
    log(f"set_responsible: {responsible}")

    user_id = update.effective_user.id
    user_states[user_id]["task_data"]["owner_id"] = responsible
    user_states[user_id]["step"] = task_creation_states[2] #setting state to WAITING_FOR_DEADLINE
    await update.callback_query.edit_message_text(f"Task is assigned to: {DBHandler.get_user_name_by_telegram_id(responsible)}")
    await send_to_user(update,f"Please set a deadline:")

async def set_priority (update: Update,  priority:str):
    log(f"set_priority: {priority}")

    user_id = update.effective_user.id
    task_data = user_states[user_id]['task_data']

    task_data["priority"] = priority    
    await update.callback_query.edit_message_text(f"Priority is set to: {priority}")

    #Now finish creating task!
    task_data = user_states[user_id]['task_data']

    #log(f"""Creating task with next parameters
    #{task_data['title']}, {task_data['owner_id']}, {user_id},{task_data['deadline']},{task_data['priority']}""")

    log(", ".join(f"{key}: {value}" for key, value in task_data.items()))    

    DBHandler.add_task(
        task_data['title'],
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
