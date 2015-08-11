"""
GwtS Utilities for calculating 9X command codes and IR timings.

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

"""

crc_9x_lookup_table = [
    0, 94, 188, 226, 97, 63, 221, 131, 194, 156, 126, 32, 163, 253, 31, 65,
    157, 195, 33, 127, 252, 162, 64, 30, 95, 1, 227, 189, 62, 96, 130, 220,
    35, 125, 159, 193, 66, 28, 254, 160, 225, 191, 93, 3, 128, 222, 60, 98,
    190, 224, 2, 92, 223, 129, 99, 61, 124, 34, 192, 158, 29, 67, 161, 255,
    70, 24, 250, 164, 39, 121, 155, 197, 132, 218, 56, 102, 229, 187, 89, 7,
    219, 133, 103, 57, 186, 228, 6, 88, 25, 71, 165, 251, 120, 38, 196, 154,
    101, 59, 217, 135, 4, 90, 184, 230, 167, 249, 27, 69, 198, 152, 122, 36,
    248, 166, 68, 26, 153, 199, 37, 123, 58, 100, 134, 216, 91, 5, 231, 185,
    140, 210, 48, 110, 237, 179, 81, 15, 78, 16, 242, 172, 47, 113, 147, 205,
    17, 79, 173, 243, 112, 46, 204, 146, 211, 141, 111, 49, 178, 236, 14, 80,
    175, 241, 19, 77, 206, 144, 114, 44, 109, 51, 209, 143, 12, 82, 176, 238,
    50, 108, 142, 208, 83, 13, 239, 177, 240, 174, 76, 18, 145, 207, 45, 115,
    202, 148, 118, 40, 171, 245, 23, 73, 8, 86, 180, 234, 105, 55, 213, 139,
    87, 9, 235, 181, 54, 104, 138, 212, 149, 203, 41, 119, 244, 170, 72, 22,
    233, 183, 85, 11, 136, 214, 52, 106, 43, 117, 151, 201, 74, 20, 246, 168,
    116, 42, 200, 150, 21, 75, 169, 247, 182, 232, 10, 84, 215, 137, 107, 53
]


delays = ("FF", "FE", "FD", "FC", "FB", "FA", "F9", "F8", "F7", "F6", "F5", "F4", "F3", "F2", "F1", "20")


def encode9x(values):
    """ Encodes a command with the appropriate 9X length code and CRC
    :param values: int[] commands in decimal format OR str[] commands in hex format OR a single str of commands
    :return: str[] Encoded command string in hex
    """
    if type(values) is str:
        values = values.split()  # Split user input into str[]
    if type(values) is list:
        if type(values[0]) is str:
            values = [int(value, 16) for value in values]  # Convert str[] with hex values to int[]
    values.insert(0, len(values) + 143)
    values.append(crc_9x(values))
    return values


def crc_9x(values):
    """ Calculate CRC for 9X commands
    :param values: int[] Commands with 9X length code written in decimal format.
    :return: int[] CRC value
    """
    crc = 0
    for value in values:
        crc = crc_9x_lookup_table[crc ^ int(value)]
    return crc


def encode_ir(values, message_width=417):
    """ Encodes a complete command into IR compatible on/off time lengths.
    :param values: int[] Command to be encoded for IR
    :param message_width: int Optional variable to change the message width.
    :return: int[] Encoded array of values for IR transmission.
    """
    return_list = []
    for value in values:
        # Commands always have initial on start bit
        high = False
        return_list.append(message_width)
        # Cycle through bits for on/off bits and add/flip as needed.
        for count in range(8):
            if value >> count & 1 == high:
                return_list[-1] += message_width
            else:
                return_list.append(message_width)
                high = not high
        # End with off bit
        if high:
            return_list[-1] += message_width
        else:
            return_list.append(message_width)
    return return_list


def int_array_to_hex_str(values):
    """ Converts int[] to hex string
    :param values: int[] Values to convert to hex string
    :return: String of converted values
    """
    return ' '.join([hex(value).upper()[2:] for value in values])


def ir_fancy_format(values):
    """ Formats IR on/off lengths nicely
    :param values: int[] of on/off IR lengths
    :return: String of nicely formatted IR lengths.
    """
    return '{'+', '.join(str(value) for value in values)+'}'
