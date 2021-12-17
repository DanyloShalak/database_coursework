from controller import Controller
from repository import Repository



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
    except Exception as e:
        print(e)

