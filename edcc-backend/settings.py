import json


class Settings:
    def __init__(self):
        self.settings = {}
        self.load_settings_json_file()

    def new_commander(self, name="", inara_key="", inara_name="", edsm_key="", edsm_name=""):
        with open('settings.json', 'r') as file:
            data = json.load(file)

            cmdr = {
                "name": name,
                "inara": {
                    "api_key": inara_key,
                    "name": inara_name,
                },
                "edsm": {
                    "api_key": edsm_key,
                    "name": edsm_name,
                }
            }

            data["commanders"].append(cmdr)
            self.settings = data
            self.save_settings()

    def get_settings(self):
        self.load_settings_json_file()
        return self.settings

    def load_settings_json_file(self):
        file = open("settings.json", "r")
        file_content = file.read()
        json_data = json.loads(file_content)
        self.settings = json_data

    def save_settings(self):
        with open('settings.json', 'w') as outfile:
            json.dump(self.settings, outfile)

    def update_settings(self, new_settings):
        self.settings.update(new_settings)
        self.save_settings()


settings = Settings()
