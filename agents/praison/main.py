from praisonaiagents import Agent, Task, PraisonAIAgents
import subprocess
import os 


def run_terminal_command(command: str):
    """
    Run a terminal command and return its output
    """
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e.stderr}"

def save_to_file(file_path: str, content: str):
    """
    Save the given content to specified file path. Create the folder/file 
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as file:
        file.write(content)

    return file_path


#Create system operations agent
system_ops_agent = Agent(
    name="SystemOpsAgent",
    role="System Operations Agent",
    goal="Execute and manage complex system operations and commands",
    backstory="""You are an expert system administrador with deep knowledge of Linux systems
    You excel at running complex system operations and commands, managing processes, , and handling systems operations.
    You always validate commands before execution and ensure they are safe to run.
    .""",
    min_reflect=6,
    max_reflect=10,
    tools=[ run_terminal_command],
    llm="gpt-4o-mini"
)


## create a complex task that tests various system operations
task = Task(
    name="system_analysis_task",
    description="""
    Perform a comprehensive analysis by executing the following operations in sequence:
    1. Get system informacion(OS, kernel version)
    2. List 5 running processes and sort them by CPU Usage
    3. Check disk space usage and list directories over 10GB
    4. Display current system load and memory usage
    5. List 5 network connections
    6. Create a summary report with all findings in a text file called system_report.txt


    Do it step by step. One task at a time
    Save only the Summary report in the file.
    Use appropriate commands for each step and ensure proper error handling
    """,
    expected_output="A comprehensive system report containing all requested information saved in system_report.txt",
    agent=system_ops_agent
)


agents =  PraisonAIAgents(
    agents=[system_ops_agent],
    tasks=[task],
    process="sequential"
)


agents.start()


#Ejemplo de uso de run_terminal command
if 
# Ejemplo de uso
# output = run_terminal_command("ls -l")
# print(output)