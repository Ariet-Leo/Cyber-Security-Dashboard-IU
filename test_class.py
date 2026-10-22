
class Modul:
    def __init__(self, name, ects, semester, note):
        self.name = name
        self.ects = ects
        self.semester = semester
        self.note = note


modul1 = Modul(
    "Datenschutz und IT-Sicherheit",
    5,
    1,
    2.7
)

modul2 = Modul(
    "Wissenschaftliches Arbeiten",
    5,
    1,
    None
)

print("Modul 1:", modul1.name)
print("Note:", modul1.note)

print("-------------------")

print("Modul 2:", modul2.name)
print("Note:", modul2.note)
