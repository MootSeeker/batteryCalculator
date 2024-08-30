import pandas as pd

# Funktion für den Always ON Mode
def berechne_akkulaufzeit_always_on(akkuspannung, interne_spannung, akkukapazität_mah, stromverbrauch_geraet, stromverbrauch_verbraucher, verbraucher_spannung, selbstentladung_prozent=0.05):
    gesamtstromverbrauch_ma = stromverbrauch_geraet + 2 * stromverbrauch_verbraucher  # Zwei Verbraucher gleichzeitig
    leistung_watt = gesamtstromverbrauch_ma / 1000 * verbraucher_spannung
    akkuenergie_wh = akkukapazität_mah / 1000 * akkuspannung

    selbstentladung_wh_pro_tag = akkuenergie_wh * (selbstentladung_prozent / 100)
    
    laufzeit_stunden = 0
    while akkuenergie_wh > 0:
        akkuenergie_wh -= leistung_watt  # Energieverbrauch pro Stunde abziehen
        laufzeit_stunden += 1
        if laufzeit_stunden % 24 == 0:  # Selbstentladung nur einmal pro Tag abziehen
            akkuenergie_wh -= selbstentladung_wh_pro_tag
    
    laufzeit_minuten = laufzeit_stunden * 60
    laufzeit_tage = laufzeit_stunden / 24
    
    return laufzeit_minuten, laufzeit_stunden, laufzeit_tage, gesamtstromverbrauch_ma, leistung_watt

# Funktion für den Log Mode
def berechne_akkulaufzeit_log_mode(akkuspannung, interne_spannung, akkukapazität_mah, sleep_strom, on_strom, stromverbrauch_verbraucher, verbraucher_spannung, wakeup_interval_s, verbraucher_einschaltzeit_ms=100, verarbeitungszeit_ms=50, selbstentladung_prozent=0.05):
    # Berechnung der Einschaltdauer und Verarbeitungszeit in Stunden
    verbraucher_einschaltzeit_h = verbraucher_einschaltzeit_ms / 1000 / 3600
    verarbeitungszeit_h = verarbeitungszeit_ms / 1000 / 3600
    
    # Berechnung des Anteils der "On"-Zeit pro Stunde (in Stunden)
    on_time_per_hour_h = 3600 / wakeup_interval_s / 3600
    
    # Gesamtstromverbrauch im Log Mode:
    # - Stromverbrauch im Schlafmodus (sleep_strom * Zeit im Schlafmodus)
    # - Stromverbrauch im Wachmodus (on_strom * Zeit im Wachmodus)
    # - Stromverbrauch der beiden Verbraucher (stromverbrauch_verbraucher * Anzahl der Verbraucher * Zeit im Wachmodus)
    gesamtstromverbrauch_ma = (sleep_strom * (1 - on_time_per_hour_h)) + \
                              ((on_strom + 2 * stromverbrauch_verbraucher) * on_time_per_hour_h) + \
                              (2 * stromverbrauch_verbraucher * verbraucher_einschaltzeit_h) + \
                              (on_strom * verarbeitungszeit_h)
    
    # Ausgabe für Debugging
    print(f"Stromverbrauch (mA) bei Verbraucher: {stromverbrauch_verbraucher} mA")
    print(f"Gesamtstromverbrauch: {gesamtstromverbrauch_ma:.2f} mA\n")
    
    leistung_watt = gesamtstromverbrauch_ma / 1000 * verbraucher_spannung
    akkuenergie_wh = akkukapazität_mah / 1000 * akkuspannung

    selbstentladung_wh_pro_tag = akkuenergie_wh * (selbstentladung_prozent / 100)
    
    laufzeit_stunden = 0
    while akkuenergie_wh > 0:
        akkuenergie_wh -= leistung_watt  # Energieverbrauch pro Stunde abziehen
        laufzeit_stunden += 1
        if laufzeit_stunden % 24 == 0:  # Selbstentladung nur einmal pro Tag abziehen
            akkuenergie_wh -= selbstentladung_wh_pro_tag
    
    laufzeit_minuten = laufzeit_stunden * 60
    laufzeit_tage = laufzeit_stunden / 24
    
    return laufzeit_minuten, laufzeit_stunden, laufzeit_tage, gesamtstromverbrauch_ma, leistung_watt

# Funktion für den Sleep Mode
def berechne_akkulaufzeit_sleep_mode(akkuspannung, interne_spannung, akkukapazität_mah, sleep_strom, verbraucher_spannung, selbstentladung_prozent=0.05):
    gesamtstromverbrauch_ma = sleep_strom
    leistung_watt = gesamtstromverbrauch_ma / 1000 * verbraucher_spannung
    akkuenergie_wh = akkukapazität_mah / 1000 * akkuspannung

    selbstentladung_wh_pro_tag = akkuenergie_wh * (selbstentladung_prozent / 100)
    
    laufzeit_stunden = 0
    while akkuenergie_wh > 0:
        akkuenergie_wh -= leistung_watt  # Energieverbrauch pro Stunde abziehen
        laufzeit_stunden += 1
        if laufzeit_stunden % 24 == 0:  # Selbstentladung nur einmal pro Tag abziehen
            akkuenergie_wh -= selbstentladung_wh_pro_tag
    
    laufzeit_minuten = laufzeit_stunden * 60
    laufzeit_tage = laufzeit_stunden / 24
    
    return laufzeit_minuten, laufzeit_stunden, laufzeit_tage, gesamtstromverbrauch_ma, leistung_watt

# Konstanten
akkuspannung = 7.2
interne_spannung = 3.3
akkukapazität_mah = 2700
stromverbrauch_always_on = 40
stromverbrauch_log_sleep = 0.1
stromverbrauch_log_on = 5.0
stromverbrauch_sleep_mode = 0.05
verbraucher_stroeme = [1, 4.5, 10, 100]
wakeup_interval_s = 60
verbraucher_einschaltzeit_ms = 100  # Einschaltzeit des Verbrauchers in Millisekunden
verarbeitungszeit_ms = 50  # Verarbeitungszeit des Geräts in Millisekunden
selbstentladung_prozent = 0.05  # 0.05% Selbstentladung pro Tag

# Ergebnisse speichern
ergebnisse = {
    'Always ON Mode': [],
    'Log Mode': [],
    'Sleep Mode': []
}

# Berechnungen für beide Spannungsvarianten
spannungen = {'Variante 1 (3.4V)': 3.4, 'Variante 2 (5V)': 5.0}

# Für die Konsolenausgabe: Wir nehmen die Variante 1 (3.4V) und den niedrigsten Verbraucher (10 mA)
spannung_name = 'Variante 1 (3.4V)'
verbraucher_spannung = spannungen[spannung_name]
stromverbrauch_verbraucher = verbraucher_stroeme[0]

# Berechnung für Log Mode für den niedrigsten Verbraucher
laufzeit_minuten, laufzeit_stunden, laufzeit_tage, gesamtstromverbrauch, leistung_watt = berechne_akkulaufzeit_log_mode(
    akkuspannung, interne_spannung, akkukapazität_mah, stromverbrauch_log_sleep, stromverbrauch_log_on, stromverbrauch_verbraucher, verbraucher_spannung, wakeup_interval_s, verbraucher_einschaltzeit_ms=verbraucher_einschaltzeit_ms, verarbeitungszeit_ms=verarbeitungszeit_ms, selbstentladung_prozent=selbstentladung_prozent
)

# Ausgabe in der Konsole
print(f"Variante 1 (3.4V) - Log Mode mit niedrigstem Verbrauch:")
print(f"Verbraucherstrom: {stromverbrauch_verbraucher} mA")
print(f"Gesamtstromverbrauch: {gesamtstromverbrauch} mA")
print(f"Benötigte Leistung: {leistung_watt:.2f} Watt")
print(f"Akkulaufzeit: {laufzeit_minuten:.2f} Minuten, {laufzeit_stunden:.2f} Stunden, {laufzeit_tage:.2f} Tage\n")

# Restliche Berechnungen für Excel
for spannung_name, verbraucher_spannung in spannungen.items():
    # Always ON Mode
    for stromverbrauch_verbraucher in verbraucher_stroeme:
        laufzeit_minuten, laufzeit_stunden, laufzeit_tage, gesamtstromverbrauch, leistung_watt = berechne_akkulaufzeit_always_on(
            akkuspannung, interne_spannung, akkukapazität_mah, stromverbrauch_always_on, stromverbrauch_verbraucher, verbraucher_spannung, selbstentladung_prozent=selbstentladung_prozent
        )
        ergebnisse['Always ON Mode'].append([spannung_name, stromverbrauch_verbraucher, gesamtstromverbrauch, leistung_watt, '', '', laufzeit_minuten, laufzeit_stunden, laufzeit_tage])
    
    # Log Mode
    for stromverbrauch_verbraucher in verbraucher_stroeme:
        laufzeit_minuten, laufzeit_stunden, laufzeit_tage, gesamtstromverbrauch, leistung_watt = berechne_akkulaufzeit_log_mode(
            akkuspannung, interne_spannung, akkukapazität_mah, stromverbrauch_log_sleep, stromverbrauch_log_on, stromverbrauch_verbraucher, verbraucher_spannung, wakeup_interval_s, verbraucher_einschaltzeit_ms=verbraucher_einschaltzeit_ms, verarbeitungszeit_ms=verarbeitungszeit_ms, selbstentladung_prozent=selbstentladung_prozent
        )
        ergebnisse['Log Mode'].append([spannung_name, stromverbrauch_verbraucher, gesamtstromverbrauch, leistung_watt, wakeup_interval_s, verbraucher_einschaltzeit_ms, laufzeit_minuten, laufzeit_stunden, laufzeit_tage])
    
    # Sleep Mode
    for stromverbrauch_verbraucher in verbraucher_stroeme:
        laufzeit_minuten, laufzeit_stunden, laufzeit_tage, gesamtstromverbrauch, leistung_watt = berechne_akkulaufzeit_sleep_mode(
            akkuspannung, interne_spannung, akkukapazität_mah, stromverbrauch_sleep_mode, verbraucher_spannung, selbstentladung_prozent=selbstentladung_prozent
        )
        ergebnisse['Sleep Mode'].append([spannung_name, 0, gesamtstromverbrauch, leistung_watt, '', '', laufzeit_minuten, laufzeit_stunden, laufzeit_tage])

# Ergebnisse in Excel speichern
with pd.ExcelWriter('Batterielaufzeit_Berechnungen.xlsx') as writer:
    for mode, data in ergebnisse.items():
        df = pd.DataFrame(data, columns=['Spannungsvariante', 'Verbraucherstrom (mA)', 'Gesamtstromverbrauch (mA)', 'Benötigte Leistung (Watt)', 'Messintervall (s)', 'Verbraucher-Einschaltzeit (ms)', 'Akkulaufzeit (Minuten)', 'Akkulaufzeit (Stunden)', 'Akkulaufzeit (Tage)'])
        df.to_excel(writer, sheet_name=mode, index=False)

print("Die Berechnungen wurden erfolgreich in 'Batterielaufzeit_Berechnungen.xlsx' gespeichert.")
