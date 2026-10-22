
# Class fuer ein Studienmodul

class Modul:
    def __init__(self, name, ects, note, semester=1):
        self.name = name
        self.ects = ects
        self.note = note
        self.semester = semester



# Class fuer ein Semester
class Semester:
    def __init__(self, nummer):
        self.nummer = nummer
        self.module = []

    def modul_hinzufuegen(self, modul):
        self.module.append(modul)

   
    def gesamt_ects_berechnen(self):
        gesamt = 0

        for modul in self.module:
            gesamt = gesamt + modul.ects

        return gesamt

    def erworbene_ects_berechnen(self):
        erworben = 0

        for modul in self.module:
            if modul.note is not None and modul.note <= 4.0:
                erworben = erworben + modul.ects

        return erworben

    def notendurchschnitt_berechnen(self):
        noten_summe = 0
        ects_summe = 0

        for modul in self.module:
            if modul.note is not None:
                noten_summe += modul.note * modul.ects
                ects_summe += modul.ects

        if ects_summe == 0:
            return None

        return round(noten_summe / ects_summe, 2)


        

# Zwei Module erstellen
# 
# Zwei Module erstellen
if __name__ == "__main__":

    modul1 = Modul(
        "Datenschutz und IT-Sicherheit",
        5,
        2.7
    )

    modul2 = Modul(
        "Wissenschaftliches Arbeiten",
        5,
        None
    )

    # Semester erstellen
    semester1 = Semester(1)

    # Module hinzufuegen
    semester1.modul_hinzufuegen(modul1)
    semester1.modul_hinzufuegen(modul2)


    # Module anzeigen
    print("Semester:", semester1.nummer)

    for modul in semester1.module:
        print("Modul:", modul.name)
        print("ECTS:", modul.ects)
        print("Note:", modul.note)
        print("-------------------")

    # Gesamt-ECTS berechnen
    print("Gesamt ECTS:", semester1.gesamt_ects_berechnen())
    print("Erworbene ECTS:", semester1.erworbene_ects_berechnen())

    print("Notendurchschnitt:", semester1.notendurchschnitt_berechnen())

