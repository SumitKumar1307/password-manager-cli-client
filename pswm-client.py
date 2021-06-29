import requests
import os
import os.path
import platform

url = "https://b1bca8f74fd8.ngrok.io"
key = "not-found"

OS = "linux/macos/windows"
user_directory = os.path.expanduser("~")
path = f"{user_directory}/.config/pswm"

def config():
    if "linux" in platform.platform().casefold(): OS = "linux"

    elif "windows" in platform.platform().casefold():
        OS = "windows"
        path = f"{user_directory}\\password-manager"

    if "mac" in platform.platform().casefold():
        OS = "mac"
        path = f"{user_directory}/.config/.pswm"

    if os.path.isdir(path) == False:
        if OS != "windows": os.system(f"mkdir -p {path}")
        else: os.system(f"mkdir {path}")

    if OS != "windows":
        if not os.path.isfile(f"{path}/keys"):
            os.system(f"touch {path}/keys")
    else:
        if not os.path.isfile(f"{path}\\keys"):
            os.system(f"echo not-found > {path}\\keys")

    if OS != "windows": 
        with open(f"{path}/keys", "r+") as file:
            key = file.read()
            if key == '':
                file.write("not-found")
                key = "not-found"
    else:
        with open(f"{path}\\keys", "r+") as file:
            key = file.read()
            print(len(key))
            if key == '':
                file.write("not-found")
                key = "not-found"

def write_key(key):
    if OS != "windows":
        with open(f"{path}/keys", "r+") as file:
            file.truncate(0)
            file.write(key)
    else:
        with open(f"{path}\\keys", "r+") as file:
            print("IN")
            file.truncate(0)
            file.write(key)

def add_password(website: str, password):
    global key
    global url

    print(url)
    site = website.casefold()
    _url = f"{url}/POST/{key}/{site}:{password}"
    print(_url)
    response = requests.get(_url)
    response = response.json()
    if key == "not-found" and response["result"] == 1:
        print("Gotcha")
        write_key(response["key"])
    return response["result"]

def get_password(website: str):
    site = website.casefold()
    response = requests.get(f"{url}/GET/PASS/{key}/{site}").json()
    return {
        "success": True if response["result"] == "success" else False,
        "passwords": response["passwords"] if "passwords" in response else []
    }

def all():
    print(requests.get(f"{url}//APP/ALL/{key}").json())

def edit(service: str, password):
    response = requests.get(f"{url}/EDIT/{key}/{service.casefold()}:"+\
        "{password}").json()
    if response["result"] == 0:
        pass
    else:
        print(f"Password for {service.capitalize()} has been changed to"+ \
        " {password}")

if len(key) != 44:
    key = "not-found"

if __name__ == '__main__':
    print(key)
    try:
        while True:
            print("What Would You Like To Do?")
            print("1. Add A Password")
            print("2. Get A Password")
            print("3. Edit A Password")

            choice = input("Enter a index: ")
            if choice == "1":
                site = input("Name of the site: ")
                password = input("Enter your password: ")

                print("Adding...")
                try:
                    add_password(site, password)
                    print("Added")
                except:
                    print("It Didn't Worked!!!")
                    print("It was most likely due to a Fernet Key loss, We advice to immediately withdraw all your data!")
                break
            if choice == "2":
                site = input("Enter the name of the site: ")
                print("Making a Request to the API...")
                result = get_password(site)
                if result["success"] == True:
                    print("Password found: ")
                    print(result["passwords"])
                else:
                    print("Password not found! Try re-checking the Fernet key and the site name")
                break
            if choice == "3":
                service = input("Enter the name of the service: ")
                password = input("Enter the new password: ")
                edit(service, password)
                break
    except KeyboardInterrupt:
        print("\nQuitting...\n")
        exit()
