command_used = []
silent = False
reversed = False
reversed_silent = False
def name_the_robot():
    """
    The function asks the user to name the robot and returns the name

    Returns:
        string: the name of the robot
    """
    name = input("What do you want to name your robot? ")
    while len(name) == 0:
        name = input("What do you want to name your robot? ")
    print(f"{name}: Hello kiddo!")
    return name


def get_command(name):
    """
    The function asks the user for command which\
    tells the robot what to do.
    Args:
        name (string): the name of the robot
    Returns:
        string: The command that instructs the robot on what to do
    """
    prompt = f'{name}: What must I do next? '
    command = input(prompt)
    while len(command) == 0:
        print(f"{name} : Sorry, I did not understand '{command}'.")
        command = input(prompt)
    return command


def valid_commands(command):
    """
    Checks if the user inputted command is in \
    the list of available commands.

    Args:
        command (string): user input that instruct \
                            the user on what to do
    Returns:
        boolean : if the command is in the list of commands
                    returns True else False
    """
    global command_used
    commands = ['help', 'off', 'right', 'left','forward', 'back', 'sprint', 'replay', 'replay silent', 'replay reversed']
    if (command[0]).lower() in commands and (len(command) == 2 and command[1].isdigit() == True):
        return True
    elif command[0] in commands:
        return True
    else:
        return False


def check_position(command, position):
    """function takes the current position \
        then returns a new position after\
        decrementing or incrementing based on\
        user input
    Args:
        command (list): a list containing the command
        position (integer): this integer tells the\
                            user what position the robot\
                            is in.
    Returns:
        integer : current position after command is\
                    executed.
    """   
    if command[0] == 'right':
        position += 1
    if command[0] == 'left':
        position -= 1
    if position == 4 or position == -4:
        position = 0
    return position


def handling_right(name,position, command):
    """This function handles the right command
    Args:
        name (string): name of the robot
        position (integer): this integer tells the\
                            user what position the robot\
                            is in
        command (list): a list containing the command.
    Returns:
        integer : current position after command is\
                    excecuted.
    """ 
    position = check_position(command, position)
    if silent == False:
        print(f" > {name} turned {command[0]}.")
    return position


def handling_left(name, position, command):
    """This function handles the left command
    Args:
        name (string): name of the robot
        position (integer): this integer tells the\
                            user what position the robot\
                            is in
        command (list): a list containing the command.
    Returns:
        integer : current position after command is\
                    excecuted.
    """ 
    position = check_position(command, position)
    if silent == False:
        print(f" > {name} turned {command[0]}.")
    return position


def checks_get_command(name):
    y_axis = 0
    x_axis = 0
    position = 0
    global silent,reversed,reversed_silent,command_used
    while True:
        silent = False
        reversed = False
        reversed_silent = False
        command = get_command(name).lower().split(" ")
        if valid_commands(command) == True:
            command_used = handling_history(command)
            if command[0] == 'off':
                print(f"{name}: Shutting down..")
                command_used = []
                silent = False
                reversed = False
                reversed_silent = False
                break
            elif command[0] == 'help':
                print(handling_help())
                continue
            elif command[0] == 'right':
                position = handling_right(name,position, command)

            elif command[0] == 'left':
                position = handling_left(name,position,command)

            elif command[0] == 'forward':
                y_axis, x_axis = handling_forward(name, y_axis, x_axis, position, command)

            elif command[0] == 'back':
                y_axis, x_axis = handling_back(name, y_axis, x_axis, position, command)

            elif command[0] == 'sprint':
                y_axis, x_axis = handling_sprint(name, y_axis, x_axis, position, command)

            elif " ".join(command) == 'replay':
                y_axis, x_axis, position = handling_replay(name, y_axis, x_axis, position,command_used)

            elif len(command) > 2 and " ".join(command) == 'replay reversed silent':
                y_axis, x_axis, position = handling_replay_reversed_silent(name, y_axis, x_axis, position)

            elif len(command) > 1 and command[0] == 'replay' and command[1] == 'reversed':
                y_axis, x_axis, position = handling_replay_reverse(name, y_axis, x_axis, position,command_used)

            elif len(command)>1 and " ".join(command) == 'replay silent':
                y_axis, x_axis, position = handling_replay_silent(name, y_axis, x_axis, position, command_used)

            elif len(command) == 2 and command[0] == 'replay' and command[1].isdigit() or len(command[1]) == 3:
                y_axis, x_axis, position = handling_replay_numbers(name, y_axis, x_axis, position, command, command_used)

            elif len(command) == 3 and command[0] == 'replay' and command[2] in ['silent','reversed'] and command[1].isdigit() or len(command[1]) == 3:
                y_axis,x_axis, position = handling_replay_silent_numbers(name, y_axis, x_axis, position, command,command_used)

            elif len(command) == 2 and command[1][0].isdigit() and not command[1].isdigit():
                print(f"{name}: Sorry, I did not understand '{command[0]} {command[1]}'.")
                continue

            elif len(command) == 2 and " ".join(command) not in  ['replay reversed','replay silent']:
                print(f"{name}: Sorry, I did not understand '{command[0]} {command[1].upper()}'.")
                continue

            elif len(command) == 2 and not command[1].isdigit():
                print(f"{name}: Sorry, I did not understand '{command}'.")
                continue

            elif len(command) == 3 and not command[2].isdigit():
                print(f"{name}: Sorry, I did not understand '{command[0].upper()} {command[1].upper()} {command[2]}'.")
                continue

            print(f" > {name} now at position ({str(x_axis)},{str(y_axis)}).")
        else:
            print(f"{name}: Sorry, I did not understand '{' '.join(command).capitalize()}'.")


def handling_sprint(name, y_axis, x_axis, position, command):
    """this function handles the forward movement of the robot
    Args:
        name (string): the name given to the robot
        y_axis (integer): keeps track of the robot in terms of\
                            the y axis
        x_axis (integer): keeps track of the robot in terms of\
                            the x axis
        position (integer): keeps track of direction 
        command (list): contains the command and the number\
                        that the robot should move by.
    Returns:
        tuple: containing x and y coordinates
    """
    if command[1] == '0':
        return y_axis,x_axis
    else:
        old_x_axis, old_y_axis = x_axis, y_axis
        if position == 0:
            y_axis += int(command[1])
        if position == 2 or position == -2:
            y_axis -= int(command[1])
        if position == -1 or position == 3:
            x_axis -= int(command[1])
        if position == 1 or position == -3:
            x_axis += int(command[1])
        if area_limit(y_axis,x_axis,name) == False:
            x_axis, y_axis = old_x_axis, old_y_axis
        elif silent == False:
            print(f" > {name} moved forward by {command[1]} steps.")
        command[1] = int(command[1]) - 1
        command[1] = str(command[1])
        return handling_sprint(name, y_axis, x_axis, position, [command[0],command[1]])


def handling_back(name, y_axis, x_axis, position, command):
    """this function handles the back command
    Args:
        name (string): the name given to the robot
        y_axis (integer): keeps track of the robot in terms of\
                            the y axis
        x_axis (integer): keeps track of the robot in terms of\
                            the x axis
        position (integer): keeps track of direction 
        command (list): contains the command and the number\
                        that the robot should move by.
    Returns:
        tuple: containing x and y coordinates
    """    
    old_x_axis, old_y_axis = x_axis, y_axis
    if position == 0:
        y_axis -= int(command[1])
    if position == 2 or position == -2:
        y_axis += int(command[1])
    if position == -1 or position == 3:
        x_axis += int(command[1])
    if position == 1 or position == -3:
        x_axis -= int(command[1])
    if area_limit(y_axis, x_axis, name) == False:
        x_axis, y_axis = old_x_axis, old_y_axis
    elif silent == True:
        return y_axis, x_axis
    else:
        print(f" > {name} moved back by {command[1]} steps.")
    return y_axis, x_axis


def handling_forward(name, y_axis, x_axis, position, command):
    """this function deals with the forward command
    Args:
        name (string): the name given to the robot
        y_axis (integer): keeps track of the robot in terms of\
                            the y axis
        x_axis (integer): keeps track of the robot in terms of\
                            the x axis
        position (integer): keeps track of direction 
        command (list): contains the command and the number\
                          that the robot should move by.
    Returns:
        tuple: containing x and y coordinates    
    """
    old_x_axis, old_y_axis = x_axis, y_axis
    if position == 0:
        y_axis += int(command[1])
    if position == 2 or position == -2:
        y_axis -= int(command[1])
    if position == -1 or position == 3:
        x_axis -= int(command[1])
    if position == 1 or position == -3:
        x_axis += int(command[1])
    if area_limit(y_axis,x_axis,name) == False:
        x_axis, y_axis = old_x_axis, old_y_axis
    elif silent == True:
        return y_axis, x_axis
    elif silent == False:
        print(f" > {name} moved forward by {command[1]} steps.")
    return y_axis, x_axis


def handling_help():
    """this function prints out information \
        detailing the commands that the robot \ 
        can respond to.
    Returns:
        string : a string detailing the above mentioned
    """
    return'I can understand these commands:\n\
OFF  - Shut down robot\nHELP - provide information about commands\n\
RIGHT - Turns right by 90 degrees\nLEFT - Turns left by 90 degrees\n\
FORWARD - Moves forward by a specified number of steps\n\
SPRINT - Sprint forward accoring to a formula\n\
BACK - Moves backwards by a specified number of steps'


def area_limit(y_axis, x_axis,name):
    """this function gives the x and y limits\
        so the robot now effectively operates in\
        a grid.
    Args:
        y_axis (integer): keeps track of the robot in terms of\
                            the y axis
        x_axis (integer): keeps track of the robot in terms of\
                            the x axis
        name (string): the name given to the robot
    Returns:
        boolean : True if within the area limit
                    False if its outside of the limit
    """    
    if x_axis in range(-100, 101) and y_axis in range(-200, 201):
        return True
    else:
        print(f"{name}: Sorry, I cannot go outside my safe zone.")
        return False


def handling_history(command):
    """This function generates a list of all the movement\
        commands.
    Args:
        command (list): command that is a user input
    Returns:
        list : list of all the movement commands
    """    
    commands_one_arg = ['right', 'left']
    commands_two_args = ['forward', 'back', 'sprint']
    if (command[0]).lower() in commands_one_arg:
        command_used.append(command[0])
    elif command[0].lower() in commands_two_args and len(command) == 2 and command[1].isnumeric() == True:
        command_used.append(" ".join(command))
    return command_used


def handling_replay(name, y_axis, x_axis, position, command_used=command_used):
    """This function handles the replay command.
    Args:
        name (string): the name given to the robot in the above mentioned function
        y_axis (integer): keeps track of the robot in terms of\
                            the y axis
        x_axis (integer): keeps track of the robot in terms of\
                            the x axis
        position (integer): keeps track of direction 
        command (list): contains the command and the number\
                          that the robot should move by.
        command_used (list, optional): a list of all commands used.\
                         Defaults to command_used.
    Returns:
        tuple: containing position, x and y coordinates 
    """    
    number = len(command_used)
    for x in command_used:
        x= x.split(" ")
        if x[0] == 'right':
            position = handling_right(name, position,x )
        if x[0] == 'left':
            position = check_position(x, position)
        if x[0] == 'forward':
            y_axis, x_axis = handling_forward(name, y_axis, x_axis, position, x)
        if x[0] == 'back':
            y_axis, x_axis = handling_back(name, y_axis, x_axis, position, x)
        if x[0] == 'sprint':
            y_axis, x_axis = handling_sprint(name, y_axis, x_axis, position, x)
        print(f" > {name} now at position ({str(x_axis)},{str(y_axis)}).")
    if reversed == False:
        print(f" > {name} replayed {number} commands.")
    else:
        print(f" > {name} replayed {number} commands in reverse.")
    return y_axis, x_axis, position


def handling_replay_numbers(name, y_axis, x_axis, position, command, command_used):
    """This function handles the replay with numbers command.
    Args:
        name (string): the name given to the robot in the above mentioned function
        y_axis (integer): keeps track of the robot in terms of\
                            the y axis
        x_axis (integer): keeps track of the robot in terms of\
                            the x axis
        position (integer): keeps track of direction 
        command (list): contains the command and the number\
                          that the robot should move by.
        command_used (list, optional): a list of all commands used.\
                         Defaults to command_used.
    Returns:
        tuple: containing x and y coordinates 
    """   
    command_used_ = command_used.copy()
    if len(command[1]) == 3:
        num1, num2 = command[1].split("-")
        command_used_ = command_used_[-(int(num1)): -(int(num2))]
    else:
        command_used_ = command_used_[-(int(command[1])):]
    y_axis, x_axis, position = handling_replay(name, y_axis, x_axis, position, command_used_)
    return y_axis, x_axis, position


def handling_replay_reverse(name, y_axis, x_axis, position,command_used):
    """This function handles the replay reverse command.
    Args:
        name (string): the name given to the robot in the above mentioned function
        y_axis (integer): keeps track of the robot in terms of\
                            the y axis
        x_axis (integer): keeps track of the robot in terms of\
                            the x axis
        position (integer): keeps track of direction 
        command (list): contains the command and the number\
                          that the robot should move by.
        command_used (list, optional): a list of all commands used.\
                         Defaults to command_used.
    Returns:
        tuple: containing x and y coordinates 
    """
    global reversed
    reversed = True
    reverse = command_used[::-1]
    return handling_replay(name, y_axis, x_axis, position, reverse)


def handling_replay_reversed_silent(name, y_axis, x_axis, position):
    """This function handles the replay reversed silent command.
    Args:
        name (string): the name given to the robot in the above mentioned function
        y_axis (integer): keeps track of the robot in terms of\
                            the y axis
        x_axis (integer): keeps track of the robot in terms of\
                            the x axis
        position (integer): keeps track of direction 
        command (list): contains the command and the number\
                          that the robot should move by.
        command_used (list, optional): a list of all commands used.\
                         Defaults to command_used.
    Returns:
        tuple: containing x and y coordinates 
    """   
    global reversed_silent
    reversed_silent = True
    reverse = command_used[::-1]
    return handling_replay_silent(name, y_axis, x_axis, position, reverse)


def handling_replay_silent(name, y_axis, x_axis, position,command_used):
    """This function handles the replay silent command.
    Args:
        name (string): the name given to the robot in the above mentioned function
        y_axis (integer): keeps track of the robot in terms of\
                            the y axis
        x_axis (integer): keeps track of the robot in terms of\
                            the x axis
        position (integer): keeps track of direction 
        command (list): contains the command and the number\
                          that the robot should move by.
        command_used (list, optional): a list of all commands used.\
                         Defaults to command_used.
    Returns:
        tuple: containing x and y coordinates 
    """   
    global silent
    silent = True
    number = len(command_used)
    for x in command_used:
        x = x.split(" ")
        if x[0] == 'right':
            position = handling_right(name, position, x)
        if x[0] == 'left':
            position = check_position(x, position)
        if x[0] == 'forward':
            y_axis, x_axis = handling_forward(name, y_axis, x_axis, position, x)
        if x[0] == 'back':
            y_axis, x_axis = handling_back(name, y_axis, x_axis, position, x)
        if x[0] == 'sprint':
            y_axis, x_axis = handling_sprint(name, y_axis, x_axis, position, x)
    if reversed_silent == False:
        print(f" > {name} replayed {str(number)} commands silently.")
    else:
        print(f" > {name} replayed {str(number)} commands in reverse silently.")
    return y_axis, x_axis, position


def handling_replay_silent_numbers(name, y_axis, x_axis,position, command, command_used):
    """This function handles the replay silent numbers command.
    Args:
        name (string): the name given to the robot in the above mentioned function
        y_axis (integer): keeps track of the robot in terms of\
                            the y axis
        x_axis (integer): keeps track of the robot in terms of\
                            the x axis
        position (integer): keeps track of direction 
        command (list): contains the command and the number\
                          that the robot should move by.
        command_used (list, optional): a list of all commands used.\
                         Defaults to command_used.
    Returns:
        tuple: containing x and y coordinates 
    """   
    command_used_ = command_used.copy()
    if command[1].isdigit():
        if command[2] == 'reversed':
            command_used_ = command_used_[:int(command[1])]
        else:
            command_used_ = command_used_[-int(command[1]):]

    elif len(command[1]) == 3:
        num1, num2 = command[1].split("-")
        command_used_ = command_used_[-int(num1):-int(num2)]

    if command[2] == 'silent':
        y_axis, x_axis, position = handling_replay_silent(name, y_axis, x_axis, position, command_used_)
    elif command[2] == 'reversed':
        y_axis,x_axis,position = handling_replay_reverse(name,y_axis,x_axis,position,command_used_)

    return y_axis, x_axis, position


def robot_start():
    """this function calls two functions which\
        effectively run the robot.
    """  
    name = name_the_robot()
    checks_get_command(name)


if __name__ == "__main__":
    robot_start()
