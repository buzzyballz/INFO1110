# Importing the required libraries
import sys
import os

# Setting global variable for modifiers --total and --character
total = False
character = '*'

# Checking and cycling each modifier
n_args = len(sys.argv)
# Creating empty dictionary of arguments
arguments = []
for i  in range(n_args):
    # Disregarding the first system argument as it is the filename
    if i > 0:
        modifier = sys.argv[i]
        if str(modifier) == '--total':
            total = True
        elif str(modifier[:11]) == '--character':
            character = str(modifier[12])
        # Appending everything else to the arguments list
        else:
            arguments.append(modifier)

# Verifying the files in the arguments list
# If arguments is empty, it means no file specified
if len(arguments) == 0:
    print("No score file specified.")
    sys.exit()
# If there is something in arguments, you cycle through each argument and check whether they are files
for argument in arguments:
    argument = "{}".format(argument)
    # If not a file, print that it is invalid and exit
    if not os.path.isfile(argument):
        print("Invalid path to score file.")
        sys.exit()
    # If it is valid, set that argument to be the score file
    else:
        score_file = argument

# Open the file and read the lines as score
with open(score_file, 'r') as file:
    score = file.readlines()
    # Number of lines
    n_lines = len(score)

# Updating the score lines
channels = []
temp = []
for line in score:
    line = line.rstrip()
    if line[0] != '|':
        temp = []
        channels.append(temp)
        temp.append(line)
    else:
        temp.append(line)

# Looking at the channels and convert * to 1 and - to 0
channels_updated = []
for n in range(len(channels)):
    temp = []
    for line in channels[n]:
        line = line.replace('*', '1')
        line = line.replace('-', '0')
        if line[0] == '|':
            temp.append(line[1:-1])
        else:
            temp.append(line)
    channels_updated.append(temp)
channels = channels_updated

# Getting a list of the instruments
score_instruments = []
for line in score:
    line = line.rstrip()
    if line[0] != '|':
        score_instruments.append(line)

# Creating a list of instruments
instruments = os.listdir("instruments")

# Checking if the instrument is in the instruments folder
for instrument in score_instruments:
    if instrument[0] != '|' and instrument not in instruments:
        print("Unknown source.")
        sys.exit()

# If total is true then we use this
total_values_channels = []

# Running through each channel in the channels list
for channel in channels:
    x_list = []
    instrument = channel[0]
    # Finding the number of lines in the instrument
    file = open("instruments/{}".format(instrument), 'r')
    amplitude = len(file.readlines())
    file.close()
    file = open("instruments/{}".format(instrument), 'r')
    # Creating empty dictionary for coordinates and values
    coords = {}
    values = {}
    # Examining each line in the instruments file and checking if there are actual lines in the instruments file
    if amplitude > 0:
        for i in range(amplitude):
            line = file.readline().rstrip()
            # Create empty list to store the x and y values
            symbols = []
            for symbol in enumerate(line):
                symbols.append(symbol)
                for coordinate in symbols:
                    # Removing spaces and tabs - it looks at the lines and if there is something there, it will provide its enumeration (x coordinate) and its row (y coordinate)
                    # For example if it is in the 2nd row and there is something in the 10th column, it have x = 10 and y = 2
                    if coordinate[1] == ' ' or coordinate[1] == '\t':
                        symbols.remove(coordinate)
                    negative = False
                    # Checking if the row is a negative row
                if symbols[0][1] == '-':
                    negative = True
                # Get the x coordinates
                x_coord_list = []
                for coordinate in symbols:
                    # The x coordinates have shifted due to the tabs and this code shifts the x coordinates to its real x position
                    if int(coordinate[0]) > 1 and negative == True:
                        x_coord_list.append(coordinate[0] - 3)
                    elif int(coordinate[0]) > 1 and negative == False:
                        x_coord_list.append(coordinate[0] - 2)
            # Getting the y coordinates
            y_str_values = {}
            if negative == True:
                y_value = (int(symbols[1][1]) * -1)
                y_str_value = str(y_value)
                y_str_values[y_value] = y_str_value
            else:
                y_value = int(symbols[0][1])
                y_str_value = ' ' + str(y_value)
                y_str_values[y_value] = y_str_value

            # Putting the x and y coordinates together by creating a dictionary that maps them to each other
            for i in x_coord_list:
                values[i] = y_value

        # Finding the max and min of the wave (Highest row and lowest row nubmer)
        max_value = max(values.values())
        min_value = min(values.values())

        # This looks at the channel modifier and if it exceeds the length of the instrument, it will restart it - it uses a count
        for i in range(len(channel)):
            if i > 0:
                count = 0
                count_list = []
                for z in channel[i]:
                    if count == max(values.keys()):
                        count = 0
                        count_list.append(count)
                    elif z == '1':
                        count = count + 1
                        count_list.append(count)
                    else:
                        count = 0
                        count_list.append(count)
                    temp = []

                    for h in count_list:
                        if h == 0:
                            temp.append("0")
                        else:
                            temp.append("1")
                    temp = ''.join(temp)
                channel.append(temp)
                channel.remove(channel[1])

        # This looks at the channel modifier and assigns its respective x coordinate - if it detects a '0', it will reset the x coordinate count
        for h in channel:
            x = -1
            for n in range(len(h)):
                if h[n] == '1':
                    x = x + 1
                    x_list.append((n, x))
                elif h[n] == '0':
                    x = -1
                    x_list.append((n, 0))

        # Converting into a list
        values = list(values.items())

        # Flipping the x and y values
        values_flip = []
        for pair in values:
            x = pair[0]
            y = pair[1]
            values_flip.append((y, x))

        # This looks at the values and the x coordinates and maps it together
        temp = []
        for i in x_list:
            for x in values_flip:
                if i[1] == x[0]:
                    temp.append((i[1],x[1]))

        # Creating a list of rows
        # The list will contain lists - each one will have the y coordinate as the first value and the following values as the x coordinates
        # It will produce something like: [[y1, x11, x12],[y2, x21, x22]]
        rows = []
        # Making each row
        for i in range(min_value, max_value + 1):
            row_number = i
            # Begin each row with the row number as a list
            row = [row_number]
            # Running through the values and checking if it belongs in the row
            for n in values_flip:
                if n[0] == row_number:
                    row.append(n[1])
            rows.append(row)
        # Reversing rows list so that it's in descending order
        rows = rows[::-1]

        # Creating empty lists for coordinates
        # This creates a list of x-y coordinate pairs
        coordinates = []
        for coordinate in rows:
            y_value = coordinate[0]
            x_value = coordinate[1:]
            # Create a coordinate for each x coordinate and it's corresponding y value
            for n in x_value:
                coordinates.append((n, y_value))

        # Sorting values by the first number in the tuple
        values = sorted(values, key=lambda tup: tup[0])

    # From x_list, it looks at the real x coordinates and maps it to the x-y coordinates in values
    x_list_updated = []
    for coordinate in x_list:
        for x in values:
            if coordinate[1] == x[0]:
                x_list_updated.append((coordinate[0], x[1]))

    # This considers the case of two channels for one instrument
    # It starts with a dictionary and uses the x as the key and y as the value
    # If there is duplicate x coordinates, it simply adds the y values togeether in the dictionary
    x_values_dict = {}
    for coordinate in x_list_updated:
        if coordinate[0] in x_values_dict:
            x_values_dict[(coordinate[0])] += coordinate[1]
        else:
            x_values_dict[(coordinate[0])] = coordinate[1]

    # Converts the x_values_dict into a list (values_channels)
    values_channels = []
    for key, value in x_values_dict.items():
        values_channels.append((key, value))

    # Filling in the gaps - considers the case where the y difference between two consecutive x values is greater than 1 or less than -1 and fills in the empty space
    for n in range(len(values_channels)):
        if n > 0:
            difference = values_channels[n][1] - values_channels[n - 1][1]
            if difference > 1:
                for i in range(1, difference):
                    values_channels.append((n, values_channels[n][1] - i))
            elif difference < -1:
                for i in range(difference, 0):
                    values_channels.append((n, values_channels[n][1] - i - 1))

    # Flipping back the values in the form (y,x)
    values_channels_flip = []
    for pair in values_channels:
        x = pair[0]
        y = pair[1]
        values_channels_flip.append((y, x))
    # Sorting it in y descending order
    values_channels_flip = (sorted(values_channels_flip, key=lambda tup: tup[0]))[::-1]

    # Max and min y values
    y_values = []
    for coordinate in values_channels_flip:
        y_values.append(coordinate[0])
    y_max = max(y_values, default=0)
    y_min = min(y_values, default=0)

    # Make a list of x_values where the first number is the y_value
    # This is similar to before except it includes the addition of the y values with same x coordinates
    x_values = []
    for row_number in range(y_max, y_min - 1, -1):
        x = [row_number]
        for n in values_channels_flip:
            if n[0] == row_number:
                x.append(n[1])
        x_values.append(x)
    x_max = []
    for numbers in x_values:
        for number in numbers:
            x_max.append(number)
    x_max = max(x_max, default=0)

    if total == False and x_max > 0:
        print("{}:".format(instrument))
    # Creating and formatting the lines
    coords = []
    for number in x_values:
        y = number[0]
        x_values_list = number[1:]

        for x_coord in x_values_list:
            coords.append((x_coord, y))
            if y < 0:
                line = [str(y), ":", "\t"]
            else:
                line = [(" " + str(y)), ":", "\t"]

        # If the x coordinate is in the respective y coordinate row, append the character, if not append a space
        for n in range(x_max + 1):
            if n in x_values_list:
                line.append(character)
            else:
                line.append(" ")
        if total == False and x_max > 0:
            print(str(''.join(line)))
    # If total is true, add this to the total_values_channels list
    total_values_channels.append(values_channels)

# If total is true, it repeats the process with a new update channel - total_values_channels
if total == True:
    print("Total:")
    total_values_channels_updated = []
    for channel in total_values_channels:
        for coord in channel:
            total_values_channels_updated.append(coord)
    total_values_channels = total_values_channels_updated
    total_values_dict = {}
    for coordinate in total_values_channels:
        if coordinate[0] in total_values_dict:
            total_values_dict[(coordinate[0])] += coordinate[1]
        else:
            total_values_dict[(coordinate[0])] = coordinate[1]

    total_values_channels = []
    # Converting dictionary back to list
    for key, value in total_values_dict.items():
        total_values_channels.append((key, value))

    # Filling in the gaps
    for n in range(len(total_values_channels)):
        if n > 1:
            difference = total_values_channels[n][1] - total_values_channels[n - 1][1]
            if difference > 1:
                for i in range(1, difference):
                    total_values_channels.append((n, total_values_channels[n][1] - i))
            elif difference < -1:
                for i in range(difference, 0):
                    total_values_channels.append((n, total_values_channels[n][1] - i - 1))

    # Flipping the values
    total_values_channels_flip = []
    for pair in total_values_channels:
        x = pair[0]
        y = pair[1]
        total_values_channels_flip.append((y, x))

    # Sorting it out
    total_values_channels_flip = (sorted(total_values_channels_flip, key=lambda tup: tup[0]))[::-1]

    # Max and min y values
    y_values = []
    for coordinate in total_values_channels_flip:
        y = coordinate[0]
        y_values.append(y)
    y_max = max(y_values, default=0)
    y_min = min(y_values, default=0)

    # Make a list of x_values where the first number is the y_value
    x_values = []
    for row_number in range(y_max, y_min - 1, -1):
        x = [row_number]
        for n in total_values_channels_flip:
            if n[0] == row_number:
                x.append(n[1])
        x_values.append(x)
    coords = []
    for number in x_values:
        y = number[0]
        x_values_list = number[1:]

        for x_coord in x_values_list:
            coords.append((x_coord, y))

        if y < 0:
            line = [str(y), ":", "\t"]
        else:
            line = [(" " + str(y)), ":", "\t"]

        # Finding maximum value in x
        x_max = []
        for coord in total_values_channels_flip:
            x_max.append(coord[1])
        x_max = max(x_max, default=0)

        for n in range(x_max + 1):
            if n in x_values_list:
                line.append(character)
            else:
                line.append(" ")
        if x_max > 0:
            print(str(''.join(line)))