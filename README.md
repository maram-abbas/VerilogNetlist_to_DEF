# VerilogNetlist_to_DEF
This project uses Verilog netlist code and LEF file in order to generate a DEF file. This project is done for the Digital Design II course at the American University in Cairo.

HOW TO USE:
- The main file to run is named mini_project.py

- When running the file, the following inputs should be provided:
	- Verilog netlist file
	- LEF file
	- pins file that contains specific information about the pins (look at examples folder)
	- core utilization
	- aspect ratio representing (core height / core width)
- You can use gen_pins_file.py by giving it the Verilog netlist file and it will generate the pins file.

DEPENDENCIES:
This project uses a LEF parser done by https://github.com/trimcao/lef-parser

ASSUMPTIONS:
- The DIEAREA's width is found by getting the total number of pins and multiplied by 400. Same thing is done for height.

- UNITS DISTANCE MICRONS is assumed to be 100.

- The DEF file generated is assumed to look as the samples send on Slack.

LIMITATIONS:
- The pins file should end with a new line
