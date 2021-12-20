from controller import Controller
from repository import Repository
from psycopg2 import OperationalError
import psycopg2


try:
    repo = Repository()
except Exception:
    print('Can not connect to servers')
    exit()

repo = Repository()
contr = Controller(repo)

while(True):
    command_line = input('Enter command\n')

    if command_line == 'exit':
        break
    
    try:
         contr.perform_command(command_line)
    except  IndexError:
        print('Incorrect entered command parameters')
    except OperationalError:
        repo.connect()
    except Exception as e:
        print(e)