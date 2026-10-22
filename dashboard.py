
from tkinter import simpledialog, messagebox
import tkinter as tk

from tkinter import ttk
import json

from test_semester import Modul, Semester

# # Studiendaten aus JSON laden
semester1 = Semester(1)
semester2 = Semester(2)
semester3 = Semester(3)

try:
    with open("module.json", "r", encoding="utf-8") as datei:
        daten = json.load(datei)

    for eintrag in daten:
        modul = Modul(
    eintrag["name"],
    eintrag["ects"],
    eintrag["note"],
    eintrag.get("semester", 1)

        )
        if modul.semester == 1:
            semester1.modul_hinzufuegen(modul)

        elif modul.semester == 2:
            semester2.modul_hinzufuegen(modul)

        elif modul.semester == 3:
            semester3.modul_hinzufuegen(modul)
    

except FileNotFoundError:
    print("Noch keine Module gespeichert.")
# Module in JSON speichern
def module_speichern():
    """Alle Module aus allen Semestern verlustfrei in JSON speichern."""
    daten = []
    for semester in [semester1, semester2, semester3]:
        for modul in semester.module:
            daten.append({
                "name": modul.name,
                "ects": modul.ects,
                "note": modul.note,
                "semester": semester.nummer
            })
    with open("module.json", "w", encoding="utf-8") as datei:
        json.dump(daten, datei, indent=4, ensure_ascii=False)

def gesamtdurchschnitt_berechnen():
    """ECTS-gewichteter Durchschnitt aller benoteten Module."""
    module = [m for s in (semester1, semester2, semester3) for m in s.module if m.note is not None]
    gewicht = sum(m.ects for m in module)
    return round(sum(m.note * m.ects for m in module) / gewicht, 2) if gewicht else None

# Ergebnisse berechnen
erworbene_ects = sum(s.erworbene_ects_berechnen() for s in [semester1, semester2, semester3])
notendurchschnitt = gesamtdurchschnitt_berechnen()
# Studienfortschritt berechnen
fortschritt = (erworbene_ects / 180) * 100


# Fenster erstellen
fenster = tk.Tk()
fenster.title("Cyber Security Dashboard")
fenster.geometry("850x650")
fenster.configure(bg="#0f172a")

# Titel anzeigen
titel = tk.Label(
    fenster,
    text="🛡 Cyber Security Dashboard",
    font=("Arial", 24, "bold"),
    bg="#0f172a",
    fg="#38bdf8"
)
titel.pack(pady=20)

# Studiengang anzeigen
studium = tk.Label(
    fenster,
    text="IU Fernstudium - 180 ECTS",
    font=("Arial", 11),
    bg="#0f172a",
    fg="white"
)
studium.pack(pady=10)

# Erworbene ECTS anzeigen
ects = tk.Label(
    fenster,
    text=f"Erworbene ECTS: {erworbene_ects} / 180",
    font=("Arial", 14),
    bg="#0f172a",
    fg="white"
)
ects.pack(pady=10)
# Notendurchschnitt anzeigen
note = tk.Label(
    fenster,
    text=f"Notendurchschnitt: {notendurchschnitt}",
    font=("Arial", 14),
    bg="#0f172a",
    fg="white"
)
note.pack(pady=10)

# Fenster starten

# Studienfortschritt anzeigen
fortschritt_text = tk.Label(
    fenster,
    text=f"Studienfortschritt: {fortschritt:.2f}%",
    font=("Arial", 14),
    bg="#0f172a",
    fg="white"
)
fortschritt_text.pack(pady=10)

# Fortschrittsbalken erstellen
balken = ttk.Progressbar(
    fenster,
    orient="horizontal",
    length=350,
    mode="determinate",
    maximum=100,
    value=fortschritt
)
balken.pack(pady=10)

# Module anzeigen
module_titel = tk.Label(
    fenster,
    text="Meine Module",
    font=("Arial", 16, "bold"),
    bg="#0f172a",
    fg="#38bdf8"
)
module_titel.pack(pady=10)


# Bereich für Module
module_frame = tk.Frame(
    fenster,
    bg="#1e293b",
    padx=20,
    pady=15
)
module_frame.pack(pady=10)

# Modulliste aktualisieren
def module_aktualisieren():
    print("Modulliste wird aktualisiert")
    for widget in module_frame.winfo_children():
        widget.destroy()

    
    

    for semester in [semester1, semester2, semester3]:
        semester_titel = tk.Label(
        module_frame,
        text=f"Semester {semester.nummer}",
        font=("Arial", 13, "bold"),
        bg="#1e293b",
        fg="#38bdf8"
        )
        semester_titel.pack(pady=10)

        for modul in semester.module:
            print("Semester:", semester.nummer, "Modul:", modul.name)
            note_anzeige = (
                "Noch offen"
                if modul.note is None
                else modul.note
            )

            if modul.note is None:
                status = "Noch offen"
                status_farbe = "#FFD700"
            elif float(modul.note) <= 4.0:
                status = "Bestanden"
                status_farbe = "#00FF7F"
            else:
                status = "Nicht bestanden"
                status_farbe = "#FF5555"


            
            # Modul-Zeile erstellen
            modul_zeile = tk.Frame(
                module_frame,
                bg="#355675"
            )
            modul_zeile.pack(pady=6, padx=10, fill="x")

            # Modul-Informationen anzeigen
            modul_text = tk.Label(
                modul_zeile,
                text=f"{modul.name} | ECTS: {modul.ects} | Note: {note_anzeige}",
                font=("Arial", 11, "bold"),
                bg="#355675",
                fg="white"
            )
            modul_text.pack(side="left", padx=10, pady=8)

            # Status anzeigen
            status_label = tk.Label(
                modul_zeile,
                text=status,
                font=("Arial", 10, "bold"),
                bg="#355675",
                fg=status_farbe
            )
            status_label.pack(side="left", padx=5)



            bearbeiten_button = tk.Button(
                modul_zeile,
                text="Bearbeiten",
                bg="#00BFFF",
                fg="white",
                command=lambda m=modul: modul_bearbeiten(m)
            )
            bearbeiten_button.pack(side="left", padx=5)

            loeschen_button = tk.Button(
                modul_zeile,
                text="Löschen",
                bg="#FF8533",
                fg="white",
                command=lambda m=modul: modul_loeschen(m)
            )
            loeschen_button.pack(side="left", padx=5)



# Module beim Start anzeigen
# Statistiken aktualisieren
def statistiken_aktualisieren():
    """Kennzahlen über alle drei Semester neu berechnen."""
    neue_ects = sum(s.erworbene_ects_berechnen() for s in (semester1, semester2, semester3))
    neuer_durchschnitt = gesamtdurchschnitt_berechnen()
    neuer_fortschritt = neue_ects / 180 * 100
    ects.config(text=f"Erworbene ECTS: {neue_ects} / 180")
    note.config(text=f"Notendurchschnitt: {neuer_durchschnitt}")
    fortschritt_text.config(text=f"Studienfortschritt: {neuer_fortschritt:.2f}%")
    balken["value"] = neuer_fortschritt

# Fenster zum Hinzufügen eines Moduls
def modul_bearbeiten(modul):
    neue_note = simpledialog.askstring(
        "Modul bearbeiten",
        f"Neue Note für {modul.name}:",
        initialvalue="" if modul.note is None else str(modul.note),
        parent=fenster
    )

    if neue_note is None:
        return

    try:
        note_wert = float(neue_note.replace(",", "."))

        if not 1.0 <= note_wert <= 5.0:
            print("Ungültige Note!")
            return

        modul.note = note_wert

        module_aktualisieren()
        statistiken_aktualisieren()
        module_speichern()

    except ValueError:
        print("Bitte gültige Note eingeben!")

def modul_loeschen(modul):
    bestaetigung = messagebox.askyesno(
        "Modul löschen",
        f"Möchtest du {modul.name} wirklich löschen?"
    )

    if not bestaetigung:
        return

    for semester in (semester1, semester2, semester3):
        if modul in semester.module:
            semester.module.remove(modul)
            break

    module_aktualisieren()
    statistiken_aktualisieren()
    module_speichern()

def modul_hinzufuegen():
    neues_fenster = tk.Toplevel(fenster)
    neues_fenster.title("Neues Modul")
    neues_fenster.geometry("400x520")

    tk.Label(
        neues_fenster,
        text="Modulname:",
        font=("Arial", 12)
    ).pack(pady=10)

    name_entry = tk.Entry(
        neues_fenster,
        width=30
    )
    name_entry.pack(pady=5) 
      
    # ECTS eingeben
    tk.Label(
        neues_fenster,
        text="ECTS:",
        font=("Arial", 12)
    ).pack(pady=10)

    ects_entry = tk.Entry(
        neues_fenster,
        width=30
    )
    ects_entry.pack(pady=5)
    
    # Note eingeben
    tk.Label(
        neues_fenster,
        text="Note:",
        font=("Arial", 12)
    ).pack(pady=10)


    note_entry = tk.Entry(
        neues_fenster,
        width=30
    )
    note_entry.pack(pady=5)

    # Semester auswählen
    tk.Label(
        neues_fenster,
        text="Semester:",
        font=("Arial", 12)
    ).pack(pady=5)

    semester_var = tk.IntVar(value=1)

    semester_auswahl = tk.OptionMenu(
        neues_fenster,
        semester_var,
        1, 2, 3
    )
    semester_auswahl.pack(pady=5)

    
    # Neues Modul speichern
    def modul_speichern():
        semester_nummer = semester_var.get()
        name = name_entry.get().strip()
        ects_text = ects_entry.get().strip()
        note_text = note_entry.get().strip()

        if not name or not ects_text:
            print("Bitte Modulname und ECTS eingeben!")
            return

        try:
            ects = int(ects_text)
            note = float(note_text.replace(",", ".")) if note_text else None
        except ValueError:
            print("Bitte gültige Zahlen eingeben!")
            return

        if ects <= 0 or (note is not None and not 1.0 <= note <= 5.0):
            print("Ungültige ECTS oder Note!")
            return

        neues_modul = Modul(name, ects, note, semester_nummer)
        (semester1, semester2, semester3)[semester_nummer - 1].modul_hinzufuegen(neues_modul)
        module_aktualisieren()
        statistiken_aktualisieren()
        module_speichern()


        print("Modul gespeichert:", name)
        neues_fenster.destroy()
    
    # Speichern Button
    speichern_button = tk.Button(
        neues_fenster,
        text="Speichern",
        font=("Arial", 12),
        width=20,
    command=modul_speichern
    )
    speichern_button.pack(pady=20)
# Button zum Hinzufügen eines Moduls

hinzufuegen_button = tk.Button(
    fenster,
    text="+ Modul hinzufügen",
    command=modul_hinzufuegen,
    font=("Arial", 12, "bold"),
    bg="#00BFFF",
    fg="white",
    activebackground="#009ACD",
    activeforeground="white",
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2"
)

hinzufuegen_button.pack(pady=15)

module_aktualisieren()
fenster.mainloop()
