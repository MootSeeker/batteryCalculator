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

## @brief Function to perform battery lifetime calculations and display results in the Treeview.
def berechne_akkulaufzeit():
    """Calculates battery life for various modes and displays the filtered results."""
    try:
        # Gather input values from the entry fields
        akkuspannung = float(entry_akkuspannung.get())
        akkukapazität_mah = int(entry_akkukapazität.get())
        stromverbrauch_always_on = float(entry_strom_always_on.get())
        stromverbrauch_log_sleep = float(entry_strom_log_sleep.get())
        stromverbrauch_log_on = float(entry_strom_log_on.get())
        stromverbrauch_sleep_mode = float(entry_strom_sleep_mode.get())
        verbraucher_stroeme = [float(x) for x in entry_verbraucher_stroeme.get().split(',')]
        verbraucher_spannungen = [float(x) for x in entry_verbraucher_spannungen.get().split(',')]
        booster_wirkungsgrad = float(entry_booster_wirkungsgrad.get())
        wakeup_interval_s = int(entry_wakeup_interval.get())
        verbraucher_einschaltzeit_ms = int(entry_verbraucher_einschaltzeit.get())
        verarbeitungszeit_ms = int(entry_verarbeitungszeit.get())
        selbstentladung_prozent = float(entry_selbstentladung.get())

        # Dictionary for naming the probes based on their current consumption
        verbraucher_namen = {
            1.0: 'HCD',
            4.5: 'HC2A',
            10.0: 'PCD',
            100.0: 'SF82'
        }

        ergebnisse = []  # List to store the calculation results

        ## @brief Helper function to calculate the runtime based on energy and power.
        def berechne_laufzeit(akkuenergie_wh, leistung_watt, selbstentladung_prozent):
            """Calculates the runtime of the battery in minutes, hours, and days."""
            selbstentladung_wh_pro_tag = akkuenergie_wh * (selbstentladung_prozent / 100)
            laufzeit_stunden = 0
            while akkuenergie_wh > 0:
                akkuenergie_wh -= leistung_watt
                laufzeit_stunden += 1
                if laufzeit_stunden % 24 == 0:
                    akkuenergie_wh -= selbstentladung_wh_pro_tag
            laufzeit_minuten = laufzeit_stunden * 60
            laufzeit_tage = laufzeit_stunden / 24
            return laufzeit_minuten, laufzeit_stunden, laufzeit_tage

        ## @brief Calculates battery runtime for Always ON Mode.
        #  @param akkuspannung Battery voltage.
        #  @param akkukapazität_mah Battery capacity in mAh.
        #  @param stromverbrauch_geraet Power consumption of the device.
        #  @param stromverbrauch_verbraucher Power consumption of consumers.
        #  @param verbraucher_spannung Voltage of consumers.
        #  @param booster_wirkungsgrad Booster efficiency.
        #  @param selbstentladung_prozent Self-discharge percentage.
        #  @return Runtime values in minutes, hours, and days.
        def berechne_akkulaufzeit_always_on(akkuspannung, akkukapazität_mah, stromverbrauch_geraet, stromverbrauch_verbraucher, verbraucher_spannung, booster_wirkungsgrad=1.0, selbstentladung_prozent=0.05):
            """Calculates battery runtime for Always ON Mode."""
            if verbraucher_spannung == 5.0:
                stromverbrauch_verbraucher /= booster_wirkungsgrad
            gesamtstromverbrauch_ma = stromverbrauch_geraet + 2 * stromverbrauch_verbraucher
            leistung_watt = gesamtstromverbrauch_ma / 1000 * verbraucher_spannung
            akkuenergie_wh = akkukapazität_mah / 1000 * akkuspannung
            return berechne_laufzeit(akkuenergie_wh, leistung_watt, selbstentladung_prozent)

        ## @brief Calculates battery runtime for Log Mode.
        #  @param akkuspannung Battery voltage.
        #  @param akkukapazität_mah Battery capacity in mAh.
        #  @param sleep_strom Power consumption in sleep mode.
        #  @param on_strom Power consumption in active mode.
        #  @param stromverbrauch_verbraucher Power consumption of consumers.
        #  @param verbraucher_spannung Voltage of consumers.
        #  @param wakeup_interval_s Wake-up interval in seconds.
        #  @param verbraucher_einschaltzeit_ms Activation time in milliseconds.
        #  @param verarbeitungszeit_ms Processing time in milliseconds.
        #  @param booster_wirkungsgrad Booster efficiency.
        #  @param selbstentladung_prozent Self-discharge percentage.
        #  @return Runtime values in minutes, hours, and days.
        def berechne_akkulaufzeit_log_mode(akkuspannung, akkukapazität_mah, sleep_strom, on_strom, stromverbrauch_verbraucher, verbraucher_spannung, wakeup_interval_s, verbraucher_einschaltzeit_ms=100, verarbeitungszeit_ms=50, booster_wirkungsgrad=1.0, selbstentladung_prozent=0.05):
            """Calculates battery runtime for Log Mode."""
            verbraucher_einschaltzeit_h = verbraucher_einschaltzeit_ms / 1000 / 3600
            verarbeitungszeit_h = verarbeitungszeit_ms / 1000 / 3600
            on_time_per_hour_h = 3600 / wakeup_interval_s / 3600
            if verbraucher_spannung == 5.0:
                stromverbrauch_verbraucher /= booster_wirkungsgrad
            gesamtstromverbrauch_ma = (sleep_strom * (1 - on_time_per_hour_h)) + \
                                      ((on_strom + 2 * stromverbrauch_verbraucher) * on_time_per_hour_h) + \
                                      (2 * stromverbrauch_verbraucher * verbraucher_einschaltzeit_h) + \
                                      (on_strom * verarbeitungszeit_h)
            leistung_watt = gesamtstromverbrauch_ma / 1000 * verbraucher_spannung
            akkuenergie_wh = akkukapazität_mah / 1000 * akkuspannung
            return berechne_laufzeit(akkuenergie_wh, leistung_watt, selbstentladung_prozent)

        ## @brief Calculates battery runtime for Sleep Mode.
        #  @param akkuspannung Battery voltage.
        #  @param akkukapazität_mah Battery capacity in mAh.
        #  @param sleep_strom Power consumption in sleep mode.
        #  @param verbraucher_spannung Voltage of consumers.
        #  @param selbstentladung_prozent Self-discharge percentage.
        #  @return Runtime values in minutes, hours, and days.
        def berechne_akkulaufzeit_sleep_mode(akkuspannung, akkukapazität_mah, sleep_strom, verbraucher_spannung, selbstentladung_prozent=0.05):
            """Calculates battery runtime for Sleep Mode."""
            gesamtstromverbrauch_ma = sleep_strom
            leistung_watt = gesamtstromverbrauch_ma / 1000 * verbraucher_spannung
            akkuenergie_wh = akkukapazität_mah / 1000 * akkuspannung
            return berechne_laufzeit(akkuenergie_wh, leistung_watt, selbstentladung_prozent)

        # Function to get selected values from the Modus Listbox (multiple selection)
        def get_selected_modus():
            """Gets the selected modes from the Modus Listbox."""
            selected_indices = modus_listbox.curselection()
            return [modus_listbox.get(i) for i in selected_indices]

        # Function to get selected values from the Probe Listbox (multiple selection)
        def get_selected_probe():
            """Gets the selected probes from the Probe Listbox."""
            selected_indices = probe_listbox.curselection()
            return [probe_listbox.get(i) for i in selected_indices]

        # Perform the calculations for all modes and consumers
        for verbraucher_spannung in verbraucher_spannungen:
            for stromverbrauch_verbraucher in verbraucher_stroeme:
                verbraucher_name = verbraucher_namen.get(stromverbrauch_verbraucher, 'Unbekannt')

                # Always ON Mode calculation
                laufzeit_minuten, laufzeit_stunden, laufzeit_tage = berechne_akkulaufzeit_always_on(
                    akkuspannung, akkukapazität_mah, stromverbrauch_always_on, stromverbrauch_verbraucher, verbraucher_spannung, booster_wirkungsgrad=booster_wirkungsgrad, selbstentladung_prozent=selbstentladung_prozent
                )
                ergebnisse.append({
                    'Probe': f"{verbraucher_name}",
                    'Strom_Verbraucher': f"{stromverbrauch_verbraucher:.1f} mA",
                    'Spannung': f"{verbraucher_spannung:.2f} V",
                    'Laufzeit_min': f"{laufzeit_minuten:.2f} min",
                    'Laufzeit_d': f"{laufzeit_tage:.2f} d",
                    'Modus': 'Always ON Mode'
                })

                # Log Mode calculation
                laufzeit_minuten, laufzeit_stunden, laufzeit_tage = berechne_akkulaufzeit_log_mode(
                    akkuspannung, akkukapazität_mah, stromverbrauch_log_sleep, stromverbrauch_log_on, stromverbrauch_verbraucher, verbraucher_spannung, wakeup_interval_s, verbraucher_einschaltzeit_ms=verbraucher_einschaltzeit_ms, verarbeitungszeit_ms=verarbeitungszeit_ms, booster_wirkungsgrad=booster_wirkungsgrad, selbstentladung_prozent=selbstentladung_prozent
                )
                ergebnisse.append({
                    'Probe': f"{verbraucher_name}",
                    'Strom_Verbraucher': f"{stromverbrauch_verbraucher:.1f} mA",
                    'Spannung': f"{verbraucher_spannung:.2f} V",
                    'Laufzeit_min': f"{laufzeit_minuten:.2f} min",
                    'Laufzeit_d': f"{laufzeit_tage:.2f} d",
                    'Modus': 'Log Mode'
                })

                # Sleep Mode calculation
                laufzeit_minuten, laufzeit_stunden, laufzeit_tage = berechne_akkulaufzeit_sleep_mode(
                    akkuspannung, akkukapazität_mah, stromverbrauch_sleep_mode, verbraucher_spannung, selbstentladung_prozent=selbstentladung_prozent
                )
                ergebnisse.append({
                    'Probe': f"{verbraucher_name}",
                    'Strom_Verbraucher': f"{stromverbrauch_verbraucher:.1f} mA",
                    'Spannung': f"{verbraucher_spannung:.2f} V",
                    'Laufzeit_min': f"{laufzeit_minuten:.2f} min",
                    'Laufzeit_d': f"{laufzeit_tage:.2f} d",
                    'Modus': 'Sleep Mode'
                })

        # Filter results based on the user's selection from Listbox
        modus_filter = get_selected_modus()
        probe_filter = get_selected_probe()

        gefilterte_ergebnisse = [result for result in ergebnisse if 
                                (not modus_filter or result['Modus'] in modus_filter) and 
                                (not probe_filter or result['Probe'] in probe_filter)]

        # Clear the Treeview and display the filtered results
        tree.delete(*tree.get_children())
        for result in gefilterte_ergebnisse:
            tree.insert('', 'end', values=(result['Modus'], result['Probe'], result['Strom_Verbraucher'], result['Spannung'], result['Laufzeit_min'], result['Laufzeit_d']))

    except ValueError as e:
        tree.delete(*tree.get_children())
        tree.insert('', 'end', values=("Error", "Error", "Error", "Error", "Error", str(e)))

## @brief Function to exit the application.
def beenden():
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
tk.Label(root, text="Akkuspannung (V):").grid(row=0, column=0, sticky="w", padx=10, pady=5)
entry_akkuspannung = tk.Entry(root, justify='center')
entry_akkuspannung.grid(row=0, column=1, padx=10, pady=5)
entry_akkuspannung.insert(0, "3.7")

tk.Label(root, text="Akkukapazität (mAh):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_akkukapazität = tk.Entry(root, justify='center')
entry_akkukapazität.grid(row=1, column=1, padx=10, pady=5)
entry_akkukapazität.insert(0, "3500")

tk.Label(root, text="Stromverbrauch Always ON (mA):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
entry_strom_always_on = tk.Entry(root, justify='center')
entry_strom_always_on.grid(row=2, column=1, padx=10, pady=5)
entry_strom_always_on.insert(0, "40")

tk.Label(root, text="Stromverbrauch Log Sleep (mA):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
entry_strom_log_sleep = tk.Entry(root, justify='center')
entry_strom_log_sleep.grid(row=3, column=1, padx=10, pady=5)
entry_strom_log_sleep.insert(0, "0.3")

tk.Label(root, text="Stromverbrauch Log ON (mA):").grid(row=4, column=0, sticky="w", padx=10, pady=5)
entry_strom_log_on = tk.Entry(root, justify='center')
entry_strom_log_on.grid(row=4, column=1, padx=10, pady=5)
entry_strom_log_on.insert(0, "2.5")

tk.Label(root, text="Stromverbrauch Sleep Mode (mA):").grid(row=5, column=0, sticky="w", padx=10, pady=5)
entry_strom_sleep_mode = tk.Entry(root, justify='center')
entry_strom_sleep_mode.grid(row=5, column=1, padx=10, pady=5)
entry_strom_sleep_mode.insert(0, "0.25")

tk.Label(root, text="Verbraucher Ströme (mA, Kommagetrennt):").grid(row=6, column=0, sticky="w", padx=10, pady=5)
entry_verbraucher_stroeme = tk.Entry(root, justify='center')
entry_verbraucher_stroeme.grid(row=6, column=1, padx=10, pady=5)
entry_verbraucher_stroeme.insert(0, "1, 4.5, 10, 100")

tk.Label(root, text="Verbraucher Spannungen (V, Kommagetrennt):").grid(row=7, column=0, sticky="w", padx=10, pady=5)
entry_verbraucher_spannungen = tk.Entry(root, justify='center')
entry_verbraucher_spannungen.grid(row=7, column=1, padx=10, pady=5)
entry_verbraucher_spannungen.insert(0, "3.45, 5.0")

tk.Label(root, text="Booster Wirkungsgrad (%):").grid(row=8, column=0, sticky="w", padx=10, pady=5)
entry_booster_wirkungsgrad = tk.Entry(root, justify='center')
entry_booster_wirkungsgrad.grid(row=8, column=1, padx=10, pady=5)
entry_booster_wirkungsgrad.insert(0, "0.90")

tk.Label(root, text="Wakeup Intervall (s):").grid(row=9, column=0, sticky="w", padx=10, pady=5)
entry_wakeup_interval = tk.Entry(root, justify='center')
entry_wakeup_interval.grid(row=9, column=1, padx=10, pady=5)
entry_wakeup_interval.insert(0, "60")

tk.Label(root, text="Verbraucher Einschaltzeit (ms):").grid(row=10, column=0, sticky="w", padx=10, pady=5)
entry_verbraucher_einschaltzeit = tk.Entry(root, justify='center')
entry_verbraucher_einschaltzeit.grid(row=10, column=1, padx=10, pady=5)
entry_verbraucher_einschaltzeit.insert(0, "150")

tk.Label(root, text="Verarbeitungszeit (ms):").grid(row=11, column=0, sticky="w", padx=10, pady=5)
entry_verarbeitungszeit = tk.Entry(root, justify='center')
entry_verarbeitungszeit.grid(row=11, column=1, padx=10, pady=5)
entry_verarbeitungszeit.insert(0, "50")

tk.Label(root, text="Selbstentladung pro Tag (%):").grid(row=12, column=0, sticky="w", padx=10, pady=5)
entry_selbstentladung = tk.Entry(root, justify='center')
entry_selbstentladung.grid(row=12, column=1, padx=10, pady=5)
entry_selbstentladung.insert(0, "0.05")

# Mode Listbox with multiple selection
tk.Label(root, text="Select Mode:").grid(row=13, column=0, sticky="w", padx=10, pady=5)
modus_listbox = tk.Listbox(root, selectmode='multiple', height=3, exportselection=False)
modus_listbox.grid(row=13, column=1, padx=10, pady=5)
modus_listbox.insert(0, "Always ON Mode")
modus_listbox.insert(1, "Log Mode")
modus_listbox.insert(2, "Sleep Mode")

# Probe Listbox with multiple selection
tk.Label(root, text="Select Probe:").grid(row=14, column=0, sticky="w", padx=10, pady=5)
probe_listbox = tk.Listbox(root, selectmode='multiple', height=4, exportselection=False)
probe_listbox.grid(row=14, column=1, padx=10, pady=5)
probe_listbox.insert(0, "HCD")
probe_listbox.insert(1, "HC2A")
probe_listbox.insert(2, "PCD")
probe_listbox.insert(3, "SF82")

# Calculate and Exit buttons, right-aligned
berechnen_button = tk.Button(root, text="Calculate", command=berechne_akkulaufzeit)
berechnen_button.grid(row=15, column=1, sticky="e", padx=10, pady=10)

beenden_button = tk.Button(root, text="Exit", command=beenden)
beenden_button.grid(row=16, column=1, sticky="e", padx=10, pady=10)

# Treeview (similar to DataGridView) for displaying results
tree = ttk.Treeview(root, columns=('Modus', 'Probe', 'Strom Probe', 'Spannung', 'Laufzeit [min]', 'Laufzeit [d]'), show='headings')
tree.grid(row=17, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")  # Make Treeview dynamic

# Set column headers and make columns sortable
for col in tree['columns']:
    tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree, _col, False))
    tree.column(col, anchor='center', width=80)  # Set the width of each column to 80 and center-align

# Start the GUI
root.mainloop()
