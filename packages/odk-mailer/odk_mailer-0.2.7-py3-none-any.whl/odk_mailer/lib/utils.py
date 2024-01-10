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

# def join(answers):

#     filtered = []

#     for x in answers:
#         if answers[x] != None and answers[x] != '' and len(answers[x]) != 0:
#                 to_append = answers[x]
#                 if type(answers[x]) is list:
#                     to_append = ",".join(answers[x])

#                 filtered.append(to_append)

#     print(filtered)

#     return "::".join(filtered)

# def get_raw(source):
    
#     # read csv file from file path
#     if source.type == 'path':        
#         with open(source.path, newline='') as f:
#             reader = csv.DictReader(f, skipinitialspace=True)
#             headers = reader.fieldnames
#             rows = []
#             for row in reader:
#                 rows.append(row)

#     if source.type == 'url':
#         abort("Source type 'url' is not yet implemented" )

#     if source.type == 'api':
#         abort("Source type 'api' is not yet implemented.")    

#     else:
#         raise Exception(f"Unknown source type '{source.type}")
    
#     return { "headers": headers, "rows": rows}

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
                row.append(val)
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