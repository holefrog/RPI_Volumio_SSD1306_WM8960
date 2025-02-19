import configparser
import os

CONFIG_FILE = "config.ini"

def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        print("Error: No config.ini found. Creating default config.ini...")
        create_default_config()
        exit(1)

    config.read(CONFIG_FILE)

    try:
        host_ip = config.get("SERVER", "HOST_IP")
        host_port = config.get("SERVER", "HOST_Port")
        player_id = config.get("PLAYER", "Player_ID")
        return host_ip, host_port, player_id

    except (configparser.NoSectionError, configparser.NoOptionError):
        print("Error: Invalid config.ini format. Please check your configuration.")
        exit(1)

def create_default_config():
    config = configparser.ConfigParser()
    config["SERVER"] = {
        "HOST_IP": "LMS IP",
        "HOST_Port": "LMS Port"
    }
    config["PLAYER"] = {
        "Player_ID": "Your Player's MAC address"
    }
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)

    print("Default config.ini created. Please edit it and restart the script.")

