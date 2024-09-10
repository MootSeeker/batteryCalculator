"""
================================================================================
Battery Life Calculator GUI Application
--------------------------------------------------------------------------------
@file: calculator.py
@brief: This script creates a GUI application using Tkinter for calculating 
        battery runtime in different operational modes (Always ON, Log Mode, 
        and Sleep Mode) based on user inputs for power consumption, battery 
        characteristics, and other parameters. The results are displayed in 
        a sortable Treeview widget.

@author: Mootseeker
@date: 10.09.2024

@details:
    - The application allows the user to input various parameters, such as 
      battery voltage, capacity, power consumption, and self-discharge rate.
    - The runtime is calculated for multiple operation modes:
        1. Always ON Mode
        2. Log Mode
        3. Sleep Mode
    - Results are filtered and displayed in a Treeview table, where each column 
      is sortable by clicking on the column headers.
    - Input validation is performed, and any errors are shown in the result table.

@usage:
    Run the script using Python 3.x, and the Tkinter GUI will appear. Fill in 
    the required fields and click on "Calculate" to perform the battery lifetime 
    calculations. The results are shown in a dynamic table with sortable columns.

@dependencies:
    - Tkinter: For the GUI components.
    - PyInstaller (optional): To convert this script into a standalone executable 
      file if needed.

@license: MIT License
================================================================================
"""

import tkinter as tk
from tkinter import ttk

## @brief Function to sort the columns of the Treeview.
#  @param tv The Treeview widget.
#  @param col The column to sort.
#  @param reverse Boolean to indicate if sorting should be reversed.
def treeview_sort_column(tv, col, reverse):
    """Sorts Treeview columns based on their values."""
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    
    try:
        l.sort(key=lambda t: float(t[0]), reverse=reverse)
    except ValueError:
        l.sort(key=lambda t: t[0], reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

## @brief Function to copy the results to the clipboard.
def copy_to_clipboard():
    """Copies the Treeview results to the clipboard."""
    clipboard_content = ""
    # Get all rows in the Treeview
    for row in tree.get_children():
        values = tree.item(row)["values"]
        row_text = "\t".join([str(value) for value in values]) + "\n"
        clipboard_content += row_text

    # Copy to clipboard
    root.clipboard_clear()
    root.clipboard_append(clipboard_content)
    root.update()  # now it stays on the clipboard after the window is closed

## @brief Function to perform battery lifetime calculations and display results in the Treeview.
def calculate_battery_life():
    """Calculates battery life for various modes and displays the filtered results."""
    try:
        # Gather input values from the entry fields
        battery_voltage = float(entry_battery_voltage.get())
        battery_capacity_mah = int(entry_battery_capacity.get())
        power_consumption_always_on = float(entry_power_consumption_always_on.get())
        power_consumption_log_sleep = float(entry_power_consumption_log_sleep.get())
        power_consumption_log_on = float(entry_power_consumption_log_on.get())
        power_consumption_sleep_mode = float(entry_power_consumption_sleep_mode.get())
        consumer_currents = [float(x) for x in entry_consumer_currents.get().split(',')]
        consumer_voltages = [float(x) for x in entry_consumer_voltages.get().split(',')]
        booster_efficiency = float(entry_booster_efficiency.get())
        wakeup_interval_s = int(entry_wakeup_interval.get())
        consumer_activation_time_ms = int(entry_consumer_activation_time.get())
        processing_time_ms = int(entry_processing_time.get())
        self_discharge_percent = float(entry_self_discharge.get())

        # Dictionary for naming the probes based on their current consumption
        consumer_names = {
            1.0: 'Low Current Sensor',
            4.5: 'Medium Current Sensor A',
            10.0: 'Medium Current Sensor B',
            100.0: 'High Current Sensor'
        }

        results = []  # List to store the calculation results

        ## @brief Helper function to calculate the runtime based on energy and power.
        def calculate_runtime(battery_energy_wh, power_watt, self_discharge_percent):
            """Calculates the runtime of the battery in minutes, hours, and days."""
            self_discharge_wh_per_day = battery_energy_wh * (self_discharge_percent / 100)
            runtime_hours = 0
            while battery_energy_wh > 0:
                battery_energy_wh -= power_watt
                runtime_hours += 1
                if runtime_hours % 24 == 0:
                    battery_energy_wh -= self_discharge_wh_per_day
            runtime_minutes = runtime_hours * 60
            runtime_days = runtime_hours / 24
            return runtime_minutes, runtime_hours, runtime_days

        ## @brief Calculates battery runtime for Always ON Mode.
        #  @param battery_voltage Battery voltage.
        #  @param battery_capacity_mah Battery capacity in mAh.
        #  @param power_consumption_device Power consumption of the device.
        #  @param power_consumption_consumer Power consumption of consumers.
        #  @param consumer_voltage Voltage of consumers.
        #  @param booster_efficiency Booster efficiency.
        #  @param self_discharge_percent Self-discharge percentage.
        #  @return Runtime values in minutes, hours, and days.
        def calculate_battery_life_always_on(battery_voltage, battery_capacity_mah, power_consumption_device, power_consumption_consumer, consumer_voltage, booster_efficiency=1.0, self_discharge_percent=0.05):
            """Calculates battery runtime for Always ON Mode."""
            if consumer_voltage == 5.0:
                power_consumption_consumer /= booster_efficiency
            total_current_consumption_ma = power_consumption_device + 2 * power_consumption_consumer
            power_watt = total_current_consumption_ma / 1000 * consumer_voltage
            battery_energy_wh = battery_capacity_mah / 1000 * battery_voltage
            return calculate_runtime(battery_energy_wh, power_watt, self_discharge_percent)

        ## @brief Calculates battery runtime for Log Mode.
        #  @param battery_voltage Battery voltage.
        #  @param battery_capacity_mah Battery capacity in mAh.
        #  @param sleep_power Power consumption in sleep mode.
        #  @param on_power Power consumption in active mode.
        #  @param power_consumption_consumer Power consumption of consumers.
        #  @param consumer_voltage Voltage of consumers.
        #  @param wakeup_interval_s Wake-up interval in seconds.
        #  @param consumer_activation_time_ms Activation time in milliseconds.
        #  @param processing_time_ms Processing time in milliseconds.
        #  @param booster_efficiency Booster efficiency.
        #  @param self_discharge_percent Self-discharge percentage.
        #  @return Runtime values in minutes, hours, and days.
        def calculate_battery_life_log_mode(battery_voltage, battery_capacity_mah, sleep_power, on_power, power_consumption_consumer, consumer_voltage, wakeup_interval_s, consumer_activation_time_ms=100, processing_time_ms=50, booster_efficiency=1.0, self_discharge_percent=0.05):
            """Calculates battery runtime for Log Mode."""
            consumer_activation_time_h = consumer_activation_time_ms / 1000 / 3600
            processing_time_h = processing_time_ms / 1000 / 3600
            on_time_per_hour_h = 3600 / wakeup_interval_s / 3600
            if consumer_voltage == 5.0:
                power_consumption_consumer /= booster_efficiency
            total_current_consumption_ma = (sleep_power * (1 - on_time_per_hour_h)) + \
                                          ((on_power + 2 * power_consumption_consumer) * on_time_per_hour_h) + \
                                          (2 * power_consumption_consumer * consumer_activation_time_h) + \
                                          (on_power * processing_time_h)
            power_watt = total_current_consumption_ma / 1000 * consumer_voltage
            battery_energy_wh = battery_capacity_mah / 1000 * battery_voltage
            return calculate_runtime(battery_energy_wh, power_watt, self_discharge_percent)

        ## @brief Calculates battery runtime for Sleep Mode.
        #  @param battery_voltage Battery voltage.
        #  @param battery_capacity_mah Battery capacity in mAh.
        #  @param sleep_power Power consumption in sleep mode.
        #  @param consumer_voltage Voltage of consumers.
        #  @param self_discharge_percent Self-discharge percentage.
        #  @return Runtime values in minutes, hours, and days.
        def calculate_battery_life_sleep_mode(battery_voltage, battery_capacity_mah, sleep_power, consumer_voltage, self_discharge_percent=0.05):
            """Calculates battery runtime for Sleep Mode."""
            total_current_consumption_ma = sleep_power
            power_watt = total_current_consumption_ma / 1000 * consumer_voltage
            battery_energy_wh = battery_capacity_mah / 1000 * battery_voltage
            return calculate_runtime(battery_energy_wh, power_watt, self_discharge_percent)

        # Function to get selected values from the Mode Listbox (multiple selection)
        def get_selected_mode():
            """Gets the selected modes from the Mode Listbox."""
            selected_indices = mode_listbox.curselection()
            return [mode_listbox.get(i) for i in selected_indices]

        # Function to get selected values from the Probe Listbox (multiple selection)
        def get_selected_probe():
            """Gets the selected probes from the Probe Listbox."""
            selected_indices = probe_listbox.curselection()
            return [probe_listbox.get(i) for i in selected_indices]

        # Perform the calculations for all modes and consumers
        for consumer_voltage in consumer_voltages:
            for power_consumption_consumer in consumer_currents:
                consumer_name = consumer_names.get(power_consumption_consumer, 'Unknown')

                # Always ON Mode calculation
                runtime_minutes, runtime_hours, runtime_days = calculate_battery_life_always_on(
                    battery_voltage, battery_capacity_mah, power_consumption_always_on, power_consumption_consumer, consumer_voltage, booster_efficiency=booster_efficiency, self_discharge_percent=self_discharge_percent
                )
                results.append({
                    'Probe': f"{consumer_name}",
                    'Power_Consumption': f"{power_consumption_consumer:.1f} mA",
                    'Voltage': f"{consumer_voltage:.2f} V",
                    'Runtime_min': f"{runtime_minutes:.2f} min",
                    'Runtime_d': f"{runtime_days:.2f} d",
                    'Mode': 'Always ON Mode'
                })

                # Log Mode calculation
                runtime_minutes, runtime_hours, runtime_days = calculate_battery_life_log_mode(
                    battery_voltage, battery_capacity_mah, power_consumption_log_sleep, power_consumption_log_on, power_consumption_consumer, consumer_voltage, wakeup_interval_s, consumer_activation_time_ms=consumer_activation_time_ms, processing_time_ms=processing_time_ms, booster_efficiency=booster_efficiency, self_discharge_percent=self_discharge_percent
                )
                results.append({
                    'Probe': f"{consumer_name}",
                    'Power_Consumption': f"{power_consumption_consumer:.1f} mA",
                    'Voltage': f"{consumer_voltage:.2f} V",
                    'Runtime_min': f"{runtime_minutes:.2f} min",
                    'Runtime_d': f"{runtime_days:.2f} d",
                    'Mode': 'Log Mode'
                })

                # Sleep Mode calculation
                runtime_minutes, runtime_hours, runtime_days = calculate_battery_life_sleep_mode(
                    battery_voltage, battery_capacity_mah, power_consumption_sleep_mode, consumer_voltage, self_discharge_percent=self_discharge_percent
                )
                results.append({
                    'Probe': f"{consumer_name}",
                    'Power_Consumption': f"{power_consumption_consumer:.1f} mA",
                    'Voltage': f"{consumer_voltage:.2f} V",
                    'Runtime_min': f"{runtime_minutes:.2f} min",
                    'Runtime_d': f"{runtime_days:.2f} d",
                    'Mode': 'Sleep Mode'
                })

        # Filter results based on the user's selection from Listbox
        mode_filter = get_selected_mode()
        probe_filter = get_selected_probe()

        filtered_results = [result for result in results if 
                            (not mode_filter or result['Mode'] in mode_filter) and 
                            (not probe_filter or result['Probe'] in probe_filter)]

        # Clear the Treeview and display the filtered results
        tree.delete(*tree.get_children())
        for result in filtered_results:
            tree.insert('', 'end', values=(result['Mode'], result['Probe'], result['Power_Consumption'], result['Voltage'], result['Runtime_min'], result['Runtime_d']))

    except ValueError as e:
        tree.delete(*tree.get_children())
        tree.insert('', 'end', values=("Error", "Error", "Error", "Error", "Error", str(e)))

## @brief Function to exit the application.
def exit_app():
    """Exits the application."""
    root.quit()

# GUI window creation
root = tk.Tk()
root.title("Battery Life Calculator")

# Dynamic window resizing
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(17, weight=1)

# Input fields with labels and entry boxes
tk.Label(root, text="Battery Voltage (V):").grid(row=0, column=0, sticky="w", padx=10, pady=5)
entry_battery_voltage = tk.Entry(root, justify='center')
entry_battery_voltage.grid(row=0, column=1, padx=10, pady=5)
entry_battery_voltage.insert(0, "3.7")

tk.Label(root, text="Battery Capacity (mAh):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_battery_capacity = tk.Entry(root, justify='center')
entry_battery_capacity.grid(row=1, column=1, padx=10, pady=5)
entry_battery_capacity.insert(0, "3500")

tk.Label(root, text="Power Consumption Always ON (mA):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
entry_power_consumption_always_on = tk.Entry(root, justify='center')
entry_power_consumption_always_on.grid(row=2, column=1, padx=10, pady=5)
entry_power_consumption_always_on.insert(0, "40")

tk.Label(root, text="Power Consumption Log Sleep (mA):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
entry_power_consumption_log_sleep = tk.Entry(root, justify='center')
entry_power_consumption_log_sleep.grid(row=3, column=1, padx=10, pady=5)
entry_power_consumption_log_sleep.insert(0, "0.3")

tk.Label(root, text="Power Consumption Log ON (mA):").grid(row=4, column=0, sticky="w", padx=10, pady=5)
entry_power_consumption_log_on = tk.Entry(root, justify='center')
entry_power_consumption_log_on.grid(row=4, column=1, padx=10, pady=5)
entry_power_consumption_log_on.insert(0, "2.5")

tk.Label(root, text="Power Consumption Sleep Mode (mA):").grid(row=5, column=0, sticky="w", padx=10, pady=5)
entry_power_consumption_sleep_mode = tk.Entry(root, justify='center')
entry_power_consumption_sleep_mode.grid(row=5, column=1, padx=10, pady=5)
entry_power_consumption_sleep_mode.insert(0, "0.25")

tk.Label(root, text="Consumer Currents (mA, comma-separated):").grid(row=6, column=0, sticky="w", padx=10, pady=5)
entry_consumer_currents = tk.Entry(root, justify='center')
entry_consumer_currents.grid(row=6, column=1, padx=10, pady=5)
entry_consumer_currents.insert(0, "1, 4.5, 10, 100")

tk.Label(root, text="Consumer Voltages (V, comma-separated):").grid(row=7, column=0, sticky="w", padx=10, pady=5)
entry_consumer_voltages = tk.Entry(root, justify='center')
entry_consumer_voltages.grid(row=7, column=1, padx=10, pady=5)
entry_consumer_voltages.insert(0, "3.45, 5.0")

tk.Label(root, text="Booster Efficiency (%):").grid(row=8, column=0, sticky="w", padx=10, pady=5)
entry_booster_efficiency = tk.Entry(root, justify='center')
entry_booster_efficiency.grid(row=8, column=1, padx=10, pady=5)
entry_booster_efficiency.insert(0, "0.90")

tk.Label(root, text="Wakeup Interval (s):").grid(row=9, column=0, sticky="w", padx=10, pady=5)
entry_wakeup_interval = tk.Entry(root, justify='center')
entry_wakeup_interval.grid(row=9, column=1, padx=10, pady=5)
entry_wakeup_interval.insert(0, "60")

tk.Label(root, text="Consumer Activation Time (ms):").grid(row=10, column=0, sticky="w", padx=10, pady=5)
entry_consumer_activation_time = tk.Entry(root, justify='center')
entry_consumer_activation_time.grid(row=10, column=1, padx=10, pady=5)
entry_consumer_activation_time.insert(0, "150")

tk.Label(root, text="Processing Time (ms):").grid(row=11, column=0, sticky="w", padx=10, pady=5)
entry_processing_time = tk.Entry(root, justify='center')
entry_processing_time.grid(row=11, column=1, padx=10, pady=5)
entry_processing_time.insert(0, "50")

tk.Label(root, text="Self Discharge per Day (%):").grid(row=12, column=0, sticky="w", padx=10, pady=5)
entry_self_discharge = tk.Entry(root, justify='center')
entry_self_discharge.grid(row=12, column=1, padx=10, pady=5)
entry_self_discharge.insert(0, "0.05")

# Mode Listbox with scrollbar and multiple selection
tk.Label(root, text="Select Mode:").grid(row=13, column=0, sticky="w", padx=10, pady=5)

# Frame to contain the Listbox and Scrollbar
frame_mode = tk.Frame(root)
frame_mode.grid(row=13, column=1, padx=10, pady=5, sticky="nsew")

# Create the Listbox
mode_listbox = tk.Listbox(frame_mode, selectmode='multiple', height=3, exportselection=False)
mode_listbox.pack(side="left", fill="both", expand=True)

# Add items to the Listbox
mode_listbox.insert(0, "Always ON Mode")
mode_listbox.insert(1, "Log Mode")
mode_listbox.insert(2, "Sleep Mode")

# Create and configure the Scrollbar
scrollbar_mode = tk.Scrollbar(frame_mode, orient="vertical", command=mode_listbox.yview)
scrollbar_mode.pack(side="right", fill="y")

# Link the Listbox and Scrollbar
mode_listbox.config(yscrollcommand=scrollbar_mode.set)

# Update grid configuration to allow resizing
root.grid_rowconfigure(13, weight=1)
root.grid_columnconfigure(1, weight=1)


# Probe Listbox with scrollbar and multiple selection
tk.Label(root, text="Select Probe:").grid(row=14, column=0, sticky="w", padx=10, pady=5)

# Frame to contain the Listbox and Scrollbar
frame_probe = tk.Frame(root)
frame_probe.grid(row=14, column=1, padx=10, pady=5, sticky="nsew")

# Create the Listbox
probe_listbox = tk.Listbox(frame_probe, selectmode='multiple', height=4, exportselection=False)
probe_listbox.pack(side="left", fill="both", expand=True)

# Add items to the Listbox
probe_listbox.insert(0, "Low Current Sensor")
probe_listbox.insert(1, "Medium Current Sensor A")
probe_listbox.insert(2, "Medium Current Sensor B")
probe_listbox.insert(3, "High Current Sensor")

# Create and configure the Scrollbar
scrollbar_probe = tk.Scrollbar(frame_probe, orient="vertical", command=probe_listbox.yview)
scrollbar_probe.pack(side="right", fill="y")

# Link the Listbox and Scrollbar
probe_listbox.config(yscrollcommand=scrollbar_probe.set)

# Update grid configuration to allow resizing
root.grid_rowconfigure(14, weight=1)
root.grid_columnconfigure(1, weight=1)


# Buttons Frame
frame_buttons = tk.Frame(root)
frame_buttons.grid(row=15, column=1, sticky="e", padx=10, pady=10)

# Calculate button
calculate_button = tk.Button(frame_buttons, text="Calculate", command=calculate_battery_life)
calculate_button.grid(row=0, column=0, padx=5)

# Exit button
exit_button = tk.Button(frame_buttons, text="Exit", command=exit_app)
exit_button.grid(row=0, column=1, padx=5)

# Copy to Clipboard button
copy_button = tk.Button(frame_buttons, text="Export to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=0, column=2, padx=5)

# Frame to contain the Treeview and Scrollbars
frame_tree = tk.Frame(root)
frame_tree.grid(row=17, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Create the Treeview
tree = ttk.Treeview(frame_tree, columns=('Mode', 'Probe', 'Power Consumption', 'Voltage', 'Runtime [min]', 'Runtime [d]'), show='headings')
tree.grid(row=0, column=0, sticky="nsew")

# Set column headers and make columns sortable
for col in tree['columns']:
    tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree, _col, False))
    tree.column(col, anchor='center', width=80)  # Set the width of each column to 80 and center-align

# Create and configure vertical scrollbar
vsb = tk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
vsb.grid(row=0, column=1, sticky='ns')

# Create and configure horizontal scrollbar
hsb = tk.Scrollbar(frame_tree, orient="horizontal", command=tree.xview)
hsb.grid(row=1, column=0, sticky='ew')

# Link the Treeview and scrollbars
tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

# Update grid configuration to allow resizing
frame_tree.grid_rowconfigure(0, weight=1)
frame_tree.grid_columnconfigure(0, weight=1)

# Start the GUI
root.mainloop()
