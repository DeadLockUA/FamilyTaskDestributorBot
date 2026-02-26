# FamilyTaskDestributorBot
This is a telegram bot to share and destribute tasks in the family. Perform some planning and track progress.

# Goals, requirements and tasks

1. [Done]Create a database to store information from users:
   
   a.[Done]Learn and install SQLite.
   
   b.[Done]Information template should contain:
     * Unique User Id
     * Task name / Timestamp / Description / Deadline / Status / Owner / Priority
  
  2. put information into the DB
  3. read out from db and send to user.
  4. manipulate existing tasks (Open -> In progress -> Done)
  5. Review status of tasks assigned by Me.
  6. Edit tasks assigned by Me
  7. Communication:
     * Send notification about new task for receiver
     * send notification for owner of the task on status update.
    
  8. Implement filtering : Overdue, today, Overdue soon.
  9. Implement sorting: Priority, overdue date
    


# Future plans
1. Greate separate user groups for different people
   * Create authentication and authorisation
2. Create statistics on complete tasks.
3. Support reccuring tasks
4. Implement task reminders






