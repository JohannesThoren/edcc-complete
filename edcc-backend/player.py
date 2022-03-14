class Player:
    def __init__(self):
        self.__last_system = None
        self.__current_system = "Alcor"
        self.__current_ship = {}
        self.__system_data = {}

    def set_current_system(self, system_name):
        self.__current_system = system_name

    def get_current_system(self):
        return self.__current_system

    def system_change_check(self, event):
        if event["event"] == "FSDJump" or event["event"] == "Location" or event["event"] == "SupercruiseExit":
            self.__last_system = self.__current_system
            self.__current_system = event["StarSystem"]
            print("lats system: "+self.__last_system+"current system: "+self.__current_system)

    def get_last_system(self):
        return self.__last_system

    def set_system_data(self, data):
        self.__system_data = data

    def get_system_data(self):
        return self.__system_data


player = Player()
