# GwtSCalc
GwtS show sequencer and command calculator

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

This script will calculate a full 9x command and IR timings given the raw commands if given no command line arguments.
For example:
Enter a 9X command: 24 64 6C <-- Raw 9x command
92 24 64 6C 4B <-- Length code and CRC generated.
{834, 417, 834, 417, 834, 834, 1251, 417, 834, 417, 834, 417, 1251, 417, 834, 834, <-- Generated IR timings
417, 417, 1251, 834, 417, 834, 417, 417, 417, 834, 417, 417, 834, 417, 417, 417} <-- Continuation of above line

Additionally, if given command line arguments, this script will generate a set of show commands with proper offsets
compatible with Jon Fether's Mouse Ear Recording Playback Tool.

The first argument is the input filename.
The second argument is optional and is the output filename. If no name is given, a default of "output.txt" will be used.
e.g. python GwtSDemo.py input.txt output.txt

Input should be formatted with the first number being the timing in milliseconds, and the following numbers being
commands, in hex, without delays or check sums.

For example:
12500 24 62 6A where 12500 represents playing the command at 12.5 seconds from the beginning that will send a command to
clear all current colors/effects and sets both ears to green.

The output will 000029CC: 93 FF 24 62 6A C8 with the first number, in hex, the time that the command is sent, followed
by a : and then followed by the command with the appropriate delay code and checksum. Following that first output, the
following lines will also be generated for the delays of FE, FD, .. F1, 20 and their appropriate time codes and
delays. Refer to the example input.txt and output.txt for an example.

By default, generated commands with the same time will be appended, one being sent right after the other.
To change this, comment out line 84 and uncomment line 85 to instead have the "newer" command replace an older command.
