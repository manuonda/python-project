import os 
from dotenv import load_dotenv
_ = load_dotenv()

profile = {
    "name":"Jhon",
    "full_name":"Jhon Doe",
    "user_profile_background":"Senior software engineer"
}


prompt_instructions = {
    "triage_rules": {
        "ignore": "Marketing newsletters, spam emails, mass company announcements",
        "notify": "Team member out sick, build system notifications, project status updates",
        "respond": "Direct questions from team members, meeting requests, critical bug reports",
    },
    "agent_instructions": "Use these tools when appropriate to help manage John's tasks efficiently."
}