"""
GwtS show sequencer and command calculator

MousieMagic.tumblr.com
MousieMagic@gmail.com


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

--

This script will calculate a full 9x command given the raw commands.

Additionally, if given command line arguments, this script will generate a set of show commands with proper offsets
compatible with Jon Fether's Mouse Ear Recording Playback Tool.
The first argument is the input filename.
The second argument is optional and is the output filename. If no name is given, a default of "output.txt" will be used.
e.g. python GwtSDemo input_file_name.txt output_file_name.txt

"""

import GwtSUtils
import sys

# Regular command calculator
def main():
    print("Enter 0 to exit")
    while True:
        try:
            user_input = input("Enter a 9X command: ")
            if user_input == '0':
                return
            encoded = GwtSUtils.encode9x(user_input)
            print(GwtSUtils.int_array_to_hex_str(encoded))  # Displays 9x computed command
            print(GwtSUtils.ir_fancy_format(GwtSUtils.encode_ir(encoded)))  # Displays IR on/off timings
        except ValueError:
            print("Bad input")

# Show Sequencer
if len(sys.argv) > 1:
    input_commands, output_commands = list(), list()
    with open(sys.argv[1], 'r') as input_file:
        for line in input_file:
            input_commands.append(line.replace(':', '').split())
    for line in input_commands:
        for index, delay in enumerate(GwtSUtils.delays):  # Delays from FF to 20
            if (int(line[0])-(16-index)*100) < 0:  # If the modified time goes before 0 (start of show) omit it.
                continue
            output_line = (str(int(line[0])-(16-index)*100)).zfill(8) + " "  # Begin with the time code in milliseconds
            temp_command = line[1:]  # Extract the actual command from the line and omit the time
            temp_command.insert(0, delay)  # Prepend the delay code to the command e.g. F2
            temp_command = [int(value, 16) for value in temp_command]  # Convert from hex to decimal
            temp_command = GwtSUtils.encode9x(temp_command)  # Encode for 9x using length code and CRC
            output_line += (' '.join([hex(value).upper()[2:].zfill(2) for value in temp_command]))  # Convert back from decimal to hex and append to time code.
            output_commands.append(output_line)  # Append time code + command to output command list.
    # Sort list of commands and removes commands with overlapping times.
    # Earlier commands are overwritten with "newer" commands.
    command_dict = dict()
    for line in sorted(output_commands):
        command_dict[line[:8]] = line[8:]
    # Write to file
    try:
        output = open(sys.argv[2], 'w')
    except IndexError:
        output = open("output.txt", 'w')
    for key, content in sorted(command_dict.items()):
        output.write(hex(int(key))[2:].upper().zfill(8) + ':' + content + '\n')
    output.close()


if __name__ == "__main__" and len(sys.argv) == 1:
    main()
