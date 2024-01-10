import typer
import csv 
import time
from rich import print
from rich.console import Console
from rich.columns import Columns
from rich.table import Table
from rich.panel import Panel
import json
from datetime import datetime

def abort(msg):
    print("[bold red]Error:[/bold red] "+msg)
    raise typer.Abort()

def now():
    return int(time.time())

def ts_to_str(ts):
    dt = datetime.fromtimestamp(ts)
    return dt.strftime("%c")

def render_state(state):
    match state:
        case 0:
            return "pending"
        case 1: 
            return "success"
        case _:
            return "failure"

def print_jobs(jobs):
    console = Console()
    header = ["Job Id", "Scheduled", "Recipients", "State"]
    table = Table(*header, expand=False, highlight=True, box=None, title_justify="left", show_lines="True")
    console.print()
    for job in jobs:
        row = []
        for key,val in job.items():
            if key == 'hash':
                row.append(val[:20])
            if key in ['created','scheduled']:
                row.append((ts_to_str(val)))
            if key== 'recipients':
                row.append(str(val))
            if key == 'state':
                row.append(render_state(val))
        table.add_row(*row)
    console.print(table)
    console.print()


# def render_table(header, body):
#     console = Console()

#     if header:
#         table = Table(*header)

#     for row in body:
#         table.add_row(*row)
    
#     console.print(table)