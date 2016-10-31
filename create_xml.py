class Setting:
    'Class holding the information for each setting'

    def __init__(self, name):
        self.name = name
        self.settings_to_test = []
        self.shaking = {}

    def addShaking(self, name, values):
        self.shaking[name] = []
        for i in values:
            self.shaking[name].append(i)

    def printShaking(self):
        'Prints the shaking and its values'
        for key, values in self.shaking.items():
            for i in values:
                print("{} {}".format(key, i))

    def addEntry(self, entry):
        'Adds an entry to the settings to test'
        self.settings_to_test.append(entry)

    def printSetting(self):
        ' Prints the settings'
        for setting in self.settings_to_test:
            print("{}".format(setting))


# setting the values we want to test
synchrone = Setting("synchrone")
synchrone.addEntry(0)
synchrone.addEntry(10)
synchrone.addEntry(20)

angles = Setting("angles")
angles.addEntry(1)
angles.addEntry(2)
angles.addEntry(4)
angles.addEntry(6)
angles.addEntry(8)
angles.addEntry(10)
angles.addEntry(12)
angles.addEntry(14)
angles.addEntry(16)
angles.addEntry(18)

shaking = Setting("Shaking")
shaking.addShaking("Anarchic", [0, 5, 10, 15])
shaking.addShaking("Smooth", [0])


def print_xml():
    cpt = 1
    print('<?xml version="1.0"?>')
    print("<class>")
    for synchrone_i in synchrone.settings_to_test:
        for angles_i in angles.settings_to_test:
            for key, values in shaking.shaking.items():
                for i in values:
                    print("\t<experience id=\"{}\">".format(cpt))
                    print("\t\t<synchrone>{}</synchrone>".format(synchrone_i))
                    print("\t\t<angle>{}</angle>".format(angles_i))
                    print("\t\t<shaking>")
                    print("\t\t\t<type>{}</type>".format(key))
                    print("\t\t\t<level>{}</level>".format(i))
                    print("\t\t</shaking>")
                    print("\t</experience>")
                    cpt += 1
    print("</class>")

print_xml()
