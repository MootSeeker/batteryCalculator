# Battery Life Calculator

## Overview

The **Battery Life Calculator** is a Python application built using the `tkinter` library for graphical user interface (GUI) development. This tool allows users to calculate the battery lifetime of various devices and configurations based on different modes and parameters. It provides a user-friendly interface for inputting device specifications and displays the results in a dynamic Treeview table.

## Features

- **Multiple Calculation Modes**: 
  - Always ON Mode
  - Log Mode
  - Sleep Mode
- **User Input Fields**: 
  - Battery voltage and capacity
  - Power consumption for different modes
  - Consumer currents and voltages
  - Booster efficiency and self-discharge rate
- **Dynamic Results Display**: 
  - Results are shown in a sortable Treeview table
  - Users can filter results based on selected modes and probes
- **Error Handling**: 
  - Displays error messages if input values are invalid

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/mootseeker/batteryCalculator.git
    cd batteryCalculator
    ```

2. **Install dependencies**:
   Ensure you have Python installed. This project uses `tkinter`, which is included with Python by default. No additional packages are required.

## Usage

1. **Run the application**:
    ```bash
    python main.py
    ```

2. **Input Data**:
   - Enter battery specifications in the provided fields.
   - Choose the operating modes and probes from the listboxes.
   - Click the "Calculate" button to perform the calculations.

3. **View Results**:
   - The results will be displayed in the Treeview table.
   - You can sort and filter the results by selecting different modes and probes.

4. **Exit the Application**:
   - Click the "Exit" button to close the application.

## Code Overview

### Key Functions

- `treeview_sort_column(tv, col, reverse)`: Sorts columns in the Treeview widget. Handles both numerical and text sorting.

- `berechne_akkulaufzeit()`: Calculates battery life based on user inputs and selected modes. Updates the Treeview with filtered results.

- `berechne_laufzeit(akkuenergie_wh, leistung_watt, selbstentladung_prozent)`: Helper function to calculate battery runtime in minutes, hours, and days.

- `berechne_akkulaufzeit_always_on(...)`: Calculates battery life for Always ON Mode.

- `berechne_akkulaufzeit_log_mode(...)`: Calculates battery life for Log Mode.

- `berechne_akkulaufzeit_sleep_mode(...)`: Calculates battery life for Sleep Mode.

- `get_selected_modus()`: Retrieves selected modes from the Mode Listbox.

- `get_selected_probe()`: Retrieves selected probes from the Probe Listbox.

- `beenden()`: Exits the application.

### GUI Elements

- **Input Fields**: For battery voltage, capacity, power consumption, etc.
- **Listboxes**: For selecting modes and probes with multiple selections.
- **Buttons**: For performing calculations and exiting the application.
- **Treeview**: Displays the calculation results with sortable columns.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements or bug fixes.
