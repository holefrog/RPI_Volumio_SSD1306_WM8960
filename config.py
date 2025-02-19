import configparser
import os
import logging

CONFIG_FILE = "config.ini"

def load_config():
    config = configparser.ConfigParser()
    # Check if the config file exists
    if not os.path.exists(CONFIG_FILE):
        logging.error("Error: No config.ini found. Creating default config.ini...")
        create_default_config()
        exit(1)

    config.read(CONFIG_FILE)

    try:
        host_ip = config.get("SERVER", "HOST_IP")
        host_port = config.get("SERVER", "HOST_Port")
        player_id = config.get("PLAYER", "Player_ID")
        return host_ip, host_port, player_id

    except (configparser.NoSectionError, configparser.NoOptionError):
        logging.error("Error: Invalid config.ini format. Please check your configuration.")
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

    logging.info("Default config.ini created. Please edit it and restart the script.")

