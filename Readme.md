# Battery Life Calculator 🔋

[![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

## Overview 🌐

The **Battery Life Calculator** is a Python application designed to help users calculate the battery life of various devices and configurations. Built with the `tkinter` library for a graphical user interface (GUI), this tool provides a user-friendly way to input device specifications and view results in a dynamic Treeview table. It supports multiple calculation modes and offers a robust error handling system to ensure accurate calculations.

## Features ✨

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
  - Displays error messages for invalid input values

## Getting Started 🚀

### Prerequisites 📋

- Python (3.x recommended)
- Basic knowledge of Python and GUI programming.

### Installation 💻

1. Clone the repository:
    ```bash
    git clone https://github.com/mootseeker/batteryCalculator.git
    cd batteryCalculator
    ```
2. Ensure Python is installed. This project uses `tkinter`, which is included with most Python installations by default.

### Running the Application 🚀

1. Start the application:
    ```bash
    python calculator.py
    ```
2. **Input Data**:
   - Enter battery specifications in the provided fields.
   - Choose operating modes and probes from the listboxes.
   - Click the "Calculate" button to perform the calculations.

3. **View Results**:
   - Results are displayed in the Treeview table.
   - Sort and filter results by selecting different modes and probes.

4. **Exit the Application**:
   - Click the "Exit" button to close the application.

## ToDo ✅

- [ ] [Add additional calculation modes](https://github.com/MootSeeker/batteryCalculator/issues/1)
- [ ] [Enhance error handling for edge cases](https://github.com/MootSeeker/batteryCalculator/issues/2)
- [ ] [Improve user interface design](https://github.com/MootSeeker/batteryCalculator/issues/3)
- [ ] [Implement data export features (e.g., CSV, PDF)](https://github.com/MootSeeker/batteryCalculator/issues/4)

## Code Overview 🧩

### Key Functions

- `treeview_sort_column(tv, col, reverse)`: Sorts columns in the Treeview widget.
- `berechne_akkulaufzeit()`: Calculates battery life based on user inputs.
- `berechne_laufzeit(akkuenergie_wh, leistung_watt, selbstentladung_prozent)`: Helper function for runtime calculation.
- `berechne_akkulaufzeit_always_on(...)`: Computes battery life for Always ON Mode.
- `berechne_akkulaufzeit_log_mode(...)`: Computes battery life for Log Mode.
- `berechne_akkulaufzeit_sleep_mode(...)`: Computes battery life for Sleep Mode.
- `get_selected_modus()`: Retrieves selected modes from the Mode Listbox.
- `get_selected_probe()`: Retrieves selected probes from the Probe Listbox.
- `beenden()`: Exits the application.

### GUI Elements

- **Input Fields**: For entering specifications and power details.
- **Listboxes**: For selecting modes and probes.
- **Buttons**: For calculating and exiting the application.
- **Treeview**: Displays results with sortable columns.

## Statistics 📊

- **Commits**: ![Commits](https://img.shields.io/github/commit-activity/m/MootSeeker/batteryCalculator)
- **Open Issues**: ![Open Issues](https://img.shields.io/github/issues-raw/MootSeeker/batteryCalculator)
- **Pull Requests**: ![Pull Requests](https://img.shields.io/github/issues-pr-raw/MootSeeker/batteryCalculator)
- **Stars**: ![Stars](https://img.shields.io/github/stars/MootSeeker/batteryCalculator)
- **Forks**: ![Forks](https://img.shields.io/github/forks/MootSeeker/batteryCalculator)

### Languages Used in This Repository

- ![Top Langs](https://img.shields.io/github/languages/top/MootSeeker/batteryCalculator)
- ![Languages](https://img.shields.io/github/languages/count/MootSeeker/batteryCalculator)

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing 🤝

Contributions are welcome! Please fork the repository, create a feature branch, commit your changes, and submit a pull request.

## Contact 📧

For questions or feedback, please open an issue on the repository or contact [MootSeeker](https://github.com/MootSeeker).

Happy coding!
