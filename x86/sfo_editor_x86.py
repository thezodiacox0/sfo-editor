import os
import platform
import json
import random
import subprocess
import requests
import base64
from colorama import Fore, Style, init

init(autoreset=True)

translations_cache = {}

TRANSLATIONS_FILE = "translations.json"
SETTINGS_FILE = "settings/settings.json"
BACKUP_DIR = "backup"

# Clear Screen 
def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')  
    else:
        os.system('clear') 

# Main Title (SFO Editor)
def main_title(title="", is_menu=False):
    print("=" * 50)
    print(Fore.RED + Style.BRIGHT + f"{title}".center(50))
    print("=" * 50 + "\n")
    if is_menu:
        print("=" * 50)

# Main Menu
def main_menu(translations):
    clear_screen()
    main_title(translations["app_title"], is_menu=False) 
    print(Fore.WHITE + Style.BRIGHT + translations["select_option"].center(50))
    menu_items = {
        "modify_sfo": translations["modify_sfo"],
        "auto_configuration": translations["auto_configuration"],
        "help_menu": translations["help_menu"],
		"settings_menu": translations["settings_menu"],
		"exit": translations["exit"],
    }
    print("=" * 50)
	
    for index, (key, value) in enumerate(menu_items.items()):
        if key == "exit":
            print(f"{Fore.WHITE}[0] ►{Style.RESET_ALL} {value}")
        else:
            print(f"{Fore.WHITE}[{index + 1}] ►{Style.RESET_ALL} {value}")
    print("=" * 50) 

# Configurations Menu
def auto_configuration(sfo_command, translations):
    while True:
        clear_screen()
        main_title(translations["app_title"])
        print(Fore.WHITE + Style.BRIGHT + f"{translations['title_configurations_menu']}".center(50))

        menu_items = {
            "load_configuration": translations["load_configuration"],
            "download_configuration": translations["download_configuration"],
            "exit_menu": translations["exit_menu"]
        }	
        
        print("=" * 50)
        
        for index, (key, value) in enumerate(menu_items.items()):
            if key == "exit_menu":
                print(f"{Fore.WHITE}[0] ►{Style.RESET_ALL} {value}")
            else:
                print(f"{Fore.WHITE}[{index + 1}] ►{Style.RESET_ALL} {value}")
        
        print("=" * 50) 
		
        choice = input(translations["select"]).strip()
        # Load Configuration Menu
        if choice == "1":
            load_configuration(sfo_command, translations)
				
        elif choice == "2":
            github_online_database(translations)
            break

        elif choice == "0":
            print("*" * 50)
            print(Fore.WHITE + Style.BRIGHT + f"{translations['exiting_settings']}".center(50))
            print("*" * 50)
            break
        else:
            print_invalid_choice(translations)
            input(translations["press_enter"])
            continue
	
# Settings Menu
def settings_menu(translations):
    while True:
        clear_screen()
        main_title(translations["app_title"])
        print(Fore.WHITE + Style.BRIGHT + f"{translations['settings_title']}".center(50))

        menu_items = {
            "backup": translations["backup"],
            "default_language": translations["default_language"],
            "exit_menu": translations["exit_menu"]
        }
        	
        print("=" * 50)
        
        for index, (key, value) in enumerate(menu_items.items()):
            if key == "exit_menu":
                print(f"{Fore.WHITE}[0] ►{Style.RESET_ALL} {value}")
            else:
                print(f"{Fore.WHITE}[{index + 1}] ►{Style.RESET_ALL} {value}")
        
        print("=" * 50) 
        
        choice = input(translations["select"]).strip()
        # Backup Menu
        if choice == "1":
            settings = load_settings()

            while True:
                print("=" * 50)
                print(Fore.WHITE + Style.BRIGHT + translations["backup_option_title"].center(50))
                print("=" * 50)
                print(Fore.WHITE + f"{Fore.WHITE}[1] ►{Style.RESET_ALL} {translations['enable_option']}")
                print(Fore.WHITE + f"{Fore.WHITE}[2] ►{Style.RESET_ALL} {translations['disable_option']}")
                print("=" * 50)
                
                backup_choice = input(translations["select"]).strip()
                
                if backup_choice == "1":
                    # Enable Backup
                    print("=" * 50)
                    print(Fore.WHITE + Style.BRIGHT + translations["enabled"].center(50))
                    print("=" * 50)
                    settings["backup_configsfo"] = True
                    settings["backup_paramsfo"] = True
                    save_settings(settings)
                    input(translations["press_enter"])
                    break	
                elif backup_choice == "2":
                    # Disable Backup
                    print("*" * 50)
                    print(Fore.WHITE + Style.BRIGHT + translations["disabled"].center(50))
                    print("*" * 50)
                    settings["backup_configsfo"] = False
                    settings["backup_paramsfo"] = False
                    save_settings(settings)
                    input(translations["press_enter"])
                    break
                else:
                    print_invalid_choice(translations)
                    input(translations["press_enter"])
                    break

        # Change Language Default Menu
        elif choice == "2":
            print("=" * 50)
            print(Fore.WHITE + Style.BRIGHT + translations["select_language"].center(50))
            print("=" * 50)
            print(Fore.WHITE + f"{Fore.WHITE}[1] ►{Style.RESET_ALL} {translations['spanish_language']}")
            print(Fore.WHITE + f"{Fore.WHITE}[2] ►{Style.RESET_ALL} {translations['english_language']}")
            print("=" * 50)

            language_choice = input(translations["select"]).strip()

            translations = load_translations() 
            if language_choice == "1": 
                save_language("es")
                print("=" * 50)
                print(Fore.GREEN + Style.BRIGHT + f'{translations["changed_language"]}'.center(50))
                print("=" * 50)
                break
            elif language_choice == "2":
                save_language("en")
                print("=" * 50)
                print(Fore.GREEN + Style.BRIGHT + f'{translations["changed_language"]}'.center(50))
                print("=" * 50)
                break
            else:
                print_invalid_choice(translations)
                input(translations["press_enter"])
                continue
              
					
        elif choice == "0":
            print("*" * 50)
            print(Fore.WHITE + Style.BRIGHT + f"{translations['exiting_settings']}".center(50))
            print("*" * 50)
            break
        else:
            print_invalid_choice(translations)
            input(translations["press_enter"])
            continue
		
		
# GitHub Database
def github_online_database(translations):
    clear_screen()
    main_title(translations["app_title"])
    global selected_config
    selected_config = None
    base_url = "https://api.github.com/repos/thezodiacox0/sfo-db/contents/Config"
    config_list_file = "config_pack_list.json"

    try:	
        print(Fore.WHITE + Style.BRIGHT + f"{translations['select_config_file']}".center(50))
        print("=" * 50)
        
        response = requests.get(base_url)
        response.raise_for_status()
        items = response.json()

        config_url = f"{base_url}/{config_list_file}"
        config_response = requests.get(config_url)
        config_response.raise_for_status()
        config_data = config_response.json()

        if 'content' in config_data:
            decoded_content = base64.b64decode(config_data['content']).decode('utf-8')
            
            try:
                config_json = json.loads(decoded_content)
                
                if "config_pack" in config_json and isinstance(config_json["config_pack"], list):
                    options = {}
                    
                    for idx, pack in enumerate(config_json["config_pack"], start=1):
                        name = pack.get("name", "❌ Unknown Config Pack Name")
                        author = pack.get("author")  
                        options[str(idx)] = pack["id"]
                        print(f"[{idx}] ► 🛠 {name}")
                        print(f"       └── ⚙︎ {author}")
                    
                    print("=" * 50)
                    
                    choice = input(translations["select"]).strip()
                    if choice in options:
                        selected_config = options[choice]
                        print(Fore.WHITE + f"✔ {translations['sfo_config_selected']}: {Fore.WHITE}{Style.BRIGHT}{selected_config}")

                        github_preview(translations, selected_config)
                        os.makedirs("config", exist_ok=True)
                    else:
                        print_invalid_choice(translations)
            except json.JSONDecodeError:
                pass

    except requests.exceptions.RequestException as e:
        pass

def github_preview(translations, config_id):
    base_url = f"https://api.github.com/repos/thezodiacox0/sfo-db/contents/Config/{config_id}/config_list.json"
    
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            preview_data = response.json()
            if 'content' in preview_data:
                decoded_content = base64.b64decode(preview_data['content']).decode('utf-8')
                config_data = json.loads(decoded_content)

                print("*" * 50)
                print(Fore.RED + f"{Style.BRIGHT}{('🛠️ ' + translations['github_config_preview'] + ': ' + config_id + ' 🛠️').center(50)}")
                print("*" * 50)

            if "json_config" in config_data:
                options = {}

                for idx, pack in enumerate(config_data["json_config"], start=1):
                    name = pack.get("config_name", "❌ Unknown Config Name")
                    json_file = pack.get("json_file", "❌ No json file found")
                    options[str(idx)] = json_file
                    print(f"[{idx}] ► 🛠 {name}")
                    print(f"       └── ⚙︎ {json_file}")

            select_config(translations, config_id)
        else:
            print("*" * 50)
            print(Fore.RED + f"{translations['no_config_files']}: {config_id}")
            print("*" * 50)
    except requests.exceptions.RequestException:
        pass

def select_config(translations, config_id):
    base_url = f"https://api.github.com/repos/thezodiacox0/sfo-db/contents/Config/{config_id}"
    
    try:
        response = requests.get(base_url)
        if response.status_code != 200:
            print(f"❌ Error HTTP {config_id}")
            return
        
        files = response.json()
        files = [file for file in files if file["name"] not in ["config_list.json", "README.md"]]
        options = {}

        print("*" * 50)
        print(Fore.WHITE + f"{Fore.WHITE}[0] ►{Style.RESET_ALL} {translations['download_all']}")
        print("*" * 50)
		
        choice = input(translations["select_download"]).strip().lower()
		
        for index, file in enumerate(files, start=1):
            options[str(index)] = file["name"]

        selected_files = []
        if choice == "0":
            download_config(translations, config_id, None)
        else:
            selected = choice.split(",")
            for sel in selected:
                sel = sel.strip()
                if sel in options:
                    selected_files.append(options[sel])

            if selected_files:
                download_config(translations, config_id, selected_files)
            else:
                print("\n" + "*" * 50)
                print(Fore.RED + Style.BRIGHT + translations["no_valid_files"].center(50))
                print("*" * 50 + "\n")
    
    except requests.exceptions.RequestException:
        pass

def download_config(translations, config_id, files=None):
    base_url = f"https://api.github.com/repos/thezodiacox0/sfo-db/contents/Config/{config_id}"
    response = requests.get(base_url)

    if response.status_code == 200:
        file_list = response.json()
        
        for file in file_list:
            if file["type"] == "file" and file["name"] not in ["config_list.json", "README.md"]:
                if files is None or file["name"] in files:
                    file_url = file["download_url"]
                    file_path = os.path.join("config", file["name"])
                    
                    file_response = requests.get(file_url)
                    if file_response.status_code == 200:
                        with open(file_path, "wb") as f:
                            f.write(file_response.content)
                        print("=" * 50)
                        print("\t" + (Fore.WHITE + Style.BRIGHT + translations["json_downloaded"] + f" {file['name']}" + Style.RESET_ALL).center(48))
                        print("=" * 50)
                    else:
                        print("*" * 50)
                        print("\t" + (Fore.RED + Style.BRIGHT + translations["json_error_download"] + f" {file['name']}" + Style.RESET_ALL).center(48))
                        print("*" * 50)

						
        print("=" * 50)
        print(Fore.GREEN + Style.BRIGHT + f"{translations['json_all_downloaded']}".center(50))
        print("=" * 50)
    else:
        print("*" * 50)
        print(Fore.RED + Style.BRIGHT + "❌ Error fetching files.".center(50))
        print("*" * 50)

# Settings
def load_settings():

    directory = os.path.dirname(SETTINGS_FILE)
    if not os.path.exists(directory):
        os.makedirs(directory)  

    if not os.path.exists(SETTINGS_FILE):
        default_settings = {
            "sfo_settings": "json"
        }
        save_settings(default_settings) 
        return default_settings  
    
    with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
        settings = json.load(file)
    
    return settings

def save_settings(settings):

    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, ensure_ascii=False, indent=4)
		
# Backup PARAM.SFO
def backup_sfo():
    sfo_command = get_sfo_command()
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    try:
        result = subprocess.check_output([sfo_command, '-q', 'title_id', 'param.sfo'], stderr=subprocess.STDOUT).decode().strip()
        title_id_list = [
        "CUSA", "PPSA", "SLES", "SCES", "SLUS", "SCUS", "SLPS", "SLJS", "SCPS", 
        "SCPM", "SLPM", "SLED", "PAPX", "PBPX", "PCPX"
    ]
		
        if any(result.startswith(prefix) for prefix in title_id_list):
            title_id = result[4:]
        else:
            return 

        title_id_prefix = ''.join(filter(str.isdigit, title_id))[:5]
        backup_count = len([name for name in os.listdir(BACKUP_DIR) if name.startswith(f"BACKUP-SFO{title_id_prefix}")])
        random_part = random.randint(1000, 9999)
        backup_name = f"BACKUP-SFO{title_id_prefix}-{random_part}{backup_count:02d}.sfo"
        backup_path = os.path.join(BACKUP_DIR, backup_name)

        if os.path.exists("param.sfo"):
            os.system(f'copy "param.sfo" "{backup_path}"' if platform.system() == "Windows" else f'cp param.sfo "{backup_path}"')

    except subprocess.CalledProcessError as e:
        pass
    except Exception as e:
        pass
		
def backup_config_sfo():
    sfo_command = get_sfo_command()
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    try:
        result = subprocess.check_output([sfo_command, '-q', 'title_id', 'param.sfo'], stderr=subprocess.STDOUT).decode().strip()
        title_id_list = [
        "CUSA", "PPSA", "SLES", "SCES", "SLUS", "SCUS", "SLPS", "SLJS", "SCPS", 
        "SCPM", "SLPM", "SLED", "PAPX", "PBPX", "PCPX"
    ]
		
        if any(result.startswith(prefix) for prefix in title_id_list):
            title_id = result[4:]
        else:
            return 

        title_id_prefix = ''.join(filter(str.isdigit, title_id))[:5]
        backup_count = len([name for name in os.listdir(BACKUP_DIR) if name.startswith(f"BACKUP-CONFIG{title_id_prefix}")])
        random_part = random.randint(1000, 9999)
        backup_name = f"BACKUP-CONFIG{title_id_prefix}-{random_part}{backup_count:02d}.sfo"
        backup_path = os.path.join(BACKUP_DIR, backup_name)

        if os.path.exists("param.sfo"):
            os.system(f'copy "param.sfo" "{backup_path}"' if platform.system() == "Windows" else f'cp param.sfo "{backup_path}"')

    except subprocess.CalledProcessError as e:
        pass
    except Exception as e:
        pass

# Any Error
def print_invalid_choice(translations):
    print("\n" + "*" * 50)
    print(Fore.RED + Style.BRIGHT + translations["print_invalid_choice"].center(50))
    print("*" * 50 + "\n")

# SFO Command Linux/Windows
def get_sfo_command():
    if platform.system() == "Linux":
        return "./sfo_32"
    elif platform.system() == "Windows":
        return "sfo_32"

# Load translations from JSON
def get_saved_language():
    try:
        with open(TRANSLATIONS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("saved_language")
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_language(language):
    try:
        with open(TRANSLATIONS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data["saved_language"] = language  
    with open(TRANSLATIONS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_translations():
    global translations_cache
    if not translations_cache:
        try:
            with open(TRANSLATIONS_FILE, "r", encoding="utf-8") as file:
                translations_cache = json.load(file)
        except FileNotFoundError:
            print(Fore.WHITE + "❌ Translation file not found.")
            return {}

    language = get_saved_language()
    if not language:
        language = input("❓ Select the language (Spanish / English): ").strip().lower()
        save_language(language)

    return translations_cache.get(language, translations_cache.get("en", {}))

# Modify SFO Parameters
def modify_sfo(sfo_command, translations):
    clear_screen()
    main_title(translations["app_title"])
    settings = load_settings()
	
    if settings is None:
        settings = {}
    
    if "backup_paramsfo" not in settings:
        print("*" * 50)
        print(Fore.WHITE + Style.BRIGHT + translations["backup_question"].center(50))
        print("*" * 50)
        choice = input(translations["yes_no"]).strip().lower()
        if choice in ["sí", "si", "yes"]:
            settings["backup_paramsfo"] = True
        else:
            settings["backup_paramsfo"] = False
        save_settings(settings)
		
    if settings.get("backup_paramsfo", True):
        backup_sfo()

    while True:
        clear_screen()
        main_title(translations["app_title"])  
        print(Fore.WHITE + Style.BRIGHT + translations["main"].center(50))
        print("=" * 50)	
        print(Fore.WHITE + f"{Fore.WHITE}[1] ►{Style.RESET_ALL} {translations['maintitle']}")
        print(Fore.WHITE + f"{Fore.WHITE}[2] ►{Style.RESET_ALL} {translations['subtitle']}")
        print(Fore.WHITE + f"{Fore.WHITE}[3] ►{Style.RESET_ALL} {translations['both']}")
		
        print("=" * 50) 

        choice = input(translations["select"]).strip()
        print("=" * 50)

        if choice == "1":
            title_value = input(translations["title_value"]).strip()
            if len(title_value) > 71:
                print("*" * 50)
                print(Fore.RED + Style.BRIGHT + f'{translations["character_limit"]}'.center(50))
                print("*" * 50)
                break
            if not title_value:
                print("*" * 50)
                print(Fore.RED + Style.BRIGHT + f'{translations["invalid"]}'.center(50))
                print("*" * 50)
                break
            os.system(f'{sfo_command} -e maintitle "{title_value}" param.sfo')
            print("=" * 50)
            print(Fore.GREEN + Style.BRIGHT + f'{translations["command_success"]}'.center(50))
            print("=" * 50)
            break
			
        elif choice == "2":
            title_value = input(translations["description_value"]).strip()
            if len(title_value) > 128:
                print("*" * 50)
                print(Fore.RED + Style.BRIGHT + f'{translations["character_limit"]}'.center(50))
                print("*" * 50)
                break
            if not title_value:
                print("*" * 50)
                print(Fore.RED + Style.BRIGHT + f'{translations["invalid"]}'.center(50))
                print("*" * 50)
                break
            os.system(f'{sfo_command} -e subtitle "{title_value}" param.sfo')
            print("=" * 50)
            print(Fore.GREEN + Style.BRIGHT + f'{translations["command_success"]}'.center(50))
            print("=" * 50)
            break
			
        elif choice == "3":
            maintitle_value = input(translations["title_value"]).strip()
            if len(maintitle_value) > 71:
                print("*" * 50)
                print(Fore.RED + Style.BRIGHT + f'{translations["character_limit"]}'.center(50))
                print("*" * 50)
                break
            if not maintitle_value:
                print("*" * 50)
                print(Fore.RED + Style.BRIGHT + f'{translations["invalid"]}'.center(50))
                print("*" * 50)
                break
            subtitle_value = input(translations["description_value"]).strip()
            if len(subtitle_value) > 128:
                print("*" * 50)
                print(Fore.RED + Style.BRIGHT + f'{translations["character_limit"]}'.center(50))
                print("*" * 50)
                break
            if not subtitle_value:
                print("*" * 50)
                print(Fore.RED + Style.BRIGHT + f'{translations["invalid"]}'.center(50))
                print("*" * 50)
                break
            os.system(f'{sfo_command} -e maintitle "{maintitle_value}" param.sfo')
            os.system(f'{sfo_command} -e subtitle "{subtitle_value}" param.sfo')
            print("=" * 50)
            print(Fore.GREEN + Style.BRIGHT + f'{translations["command_success"]}'.center(50))
            print("=" * 50)
            break
        else:
            print_invalid_choice(translations)
            input(translations["press_enter"])
            continue

# Load Configuration
def load_configuration(sfo_command, translations):
    while True:
        clear_screen()
        main_title(translations["app_title"])
        settings = load_settings()
        config_dir = "config"
    
        if "backup_configsfo" not in settings:
            print("*" * 50)
            print(Fore.WHITE + Style.BRIGHT + translations["backup_question"].center(50))
            print("*" * 50)
            choice = input(translations["yes_no"]).strip().lower()
    
            if choice in ["sí", "si", "yes"]:
                settings["backup_configsfo"] = True
            else:
                settings["backup_configsfo"] = False
            save_settings(settings)
        else:
            choice = "yes" if settings.get("backup_configsfo", True) else "no"
    
        if settings.get("backup_configsfo", True):
            backup_config_sfo()
    
        if not os.path.isdir(config_dir):
            print("*" * 50)
            print(Fore.RED + Style.BRIGHT + translations["no_config_dir"].center(50))
            print("*" * 50)
            break
    
        config_files = [f for f in os.listdir(config_dir) if f.endswith(".json")]
        if not config_files:
            print("*" * 50)
            print(Fore.RED + Style.BRIGHT + translations["no_config_files"].center(50))
            print("*" * 50)
            break
    
        print(Fore.WHITE + Style.BRIGHT + translations["select_config_file"].center(50))
        print("=" * 50)
    
        config_choices = []
        for idx, file in enumerate(config_files):
            config_path = os.path.join(config_dir, file)
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config_data = json.load(f)
                    name_config = f"🛠️ {config_data.get('ConfigName', '❌ Unknown Config Name')}"
                    config_choices.append((name_config, config_path))
            except Exception as e:
                break
    
        # Preview JSON Config
        for idx, (name_config, _) in enumerate(config_choices):
            print(Fore.WHITE + f"[{idx + 1}] ►{Style.RESET_ALL} {name_config}")
        print("=" * 50)

        choice = input(translations["select"]).strip()

		
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(config_choices):
            print_invalid_choice(translations)
            input(translations["press_enter"])
            break
    
        selected_name, config_path = config_choices[int(choice) - 1]

        try:
            with open(config_path, "r", encoding="utf-8") as file:
                config_data = json.load(file) 
        except Exception as e:
            print(Fore.RED + translations["error_loading_config"].format(error=str(e)))
            break

        print("*" * 50)
        print(Fore.RED + Style.BRIGHT + translations["config_preview"].center(50))
        print("*" * 50)
        for key, value in config_data.items():
            if key != "ConfigName":
                print(Style.BRIGHT + f"⚙️ {key}: " + Style.RESET_ALL + f" {value}")
    
        print("*" * 50)
        confirm = input(translations["confirm_load"]).strip().lower()
        if confirm not in ["yes", "y", "si", "s"]:
            print("*" * 50)
            print(Fore.RED + Style.BRIGHT + translations["cancelled"].center(50))
            print("*" * 50)
            input(translations["press_enter"])
            break
    
        # Apply the JSON Config to SFO
        if "Maintitle" in config_data:
            maintitle_value = config_data["Maintitle"]
            os.system(f'{sfo_command} -e maintitle "{maintitle_value}" param.sfo')
            print("=" * 50)
    
        if "Subtitle" in config_data:
            subtitle_value = config_data["Subtitle"]
            os.system(f'{sfo_command} -e subtitle "{subtitle_value}" param.sfo')
            print(Fore.GREEN + Style.BRIGHT + f'{translations["config_loaded"]}'.center(50))
            print("=" * 50)
            input(translations["press_enter"])
            break

# Help/Questions Menu
def help_menu(translations):
    while True:
        clear_screen()
        main_title(translations["app_title"])
        print(Fore.WHITE + Style.BRIGHT + f"{translations['question_prompt']}".center(50))
        print("=" * 50)

        menu_items = {
            "question_1": translations["question_1"],
            "question_2": translations["question_2"]
        }
		
        for index, (key, value) in enumerate(menu_items.items()):
            print(f"{Fore.WHITE}[{index + 1}] ►{Style.RESET_ALL} {value}")
        print("=" * 50)

        choice = input(translations["select"]).strip()

        if choice == "1":
            print("=" * 50)
            print(Fore.WHITE + translations["answer_1"])
            print("=" * 50)
            break 
        elif choice == "2":
            print("=" * 50)
            print(Fore.WHITE + translations["answer_2"])
            print("=" * 50)
            break
        else:
            print_invalid_choice(translations)
            input(translations["press_enter"])

		
# Main
def main():
    sfo_command = get_sfo_command()
	
    settings = load_settings()

    translations = load_translations()

    if not translations:
 
        return

    while True:
        clear_screen()
        main_menu(translations)
        choice = input(translations["select"]).strip()

        if choice == "1":
            modify_sfo(sfo_command, translations)
        elif choice == "2":
            auto_configuration(sfo_command, translations)
        elif choice == "3":
            help_menu(translations)
        elif choice == "4":
            settings_menu(translations)
        elif choice == "0":
            print("=" * 50)
            print(Fore.RED + Style.BRIGHT + "¡Closing the Script!".center(50))
            print("=" * 50)
            break
        else:
            print_invalid_choice(translations)

        input(translations["press_enter"])

if __name__ == "__main__":
    main()
	