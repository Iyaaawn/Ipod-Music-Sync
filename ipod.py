import os
import subprocess
import shutil

# -----------------------------
# PATHS (EDIT THESE)
# -----------------------------
DOWNLOAD_PATH = "/Users/yourname/Music/Downloads"
IPOD_PATH = "/Volumes/DRAGO'S IPO/Music"

# -----------------------------
# DATA STRUCTURE
# { Artist : [yt_link, type(0 album / 1 single), name] }
# -----------------------------
yt_links = {}

# -----------------------------
# MENU FUNCTIONS
# -----------------------------
def displayMenu():
    print("""
_______________________________________
---------------------------------------
Main Menu

1) Display Queue
2) Add to Queue
3) Remove from Queue
4) Execute ONE
5) Execute ALL
0) Quit
""")

def getInput():
    try:
        return int(input("Enter Option: "))
    except ValueError:
        return -1

# -----------------------------
# QUEUE FUNCTIONS
# -----------------------------
def displayQueue():
    if not yt_links:
        print("\nNo items in queue.")
        return

    print("\nCurrent Queue:")
    for artist, details in yt_links.items():
        type_str = "Album" if details[1] == 0 else "Single"
        print(f" - {artist} | {type_str} | {details[2]}")

def addToQueue():
    artist = input("Artist: ")
    link = input("YouTube Link: ")
    name = input("Album/Single Name: ")
    
    try:
        type_flag = int(input("Album(0) or Single(1): "))
        if type_flag not in [0, 1]:
            raise ValueError
    except:
        print("Invalid type.")
        return

    yt_links[artist] = [link, type_flag, name]
    print(f"Added {artist} to queue.")

def removeFromQueue():
    displayQueue()
    artist = input("Remove which artist: ")

    try:
        yt_links.pop(artist)
        print("Removed.")
    except KeyError:
        print("Not found.")

# -----------------------------
# CORE LOGIC
# -----------------------------
def download_audio(link):
    command = [
        "yt-dlp",
        "-x",
        "--audio-format", "flac",
        "-o", f"{DOWNLOAD_PATH}/%(title)s.%(ext)s",
        link
    ]
    subprocess.run(command)

def convert_folder():
    command = f"""
    for file in "{DOWNLOAD_PATH}"/*.flac; do
      temp_file="${{file%.flac}}_temp.flac"
      ffmpeg -i "$file" -ar 44100 -sample_fmt s16 -y "$temp_file" && mv "$temp_file" "$file"
    done
    """
    subprocess.run(command, shell=True, executable="/bin/bash")

def copy_to_ipod():
    # create path if it doesn't exist
    if not os.path.exists(IPOD_PATH):
        os.makedirs(IPOD_PATH)

    for file in os.listdir(DOWNLOAD_PATH):
        if file.endswith(".flac"):
            src = os.path.join(DOWNLOAD_PATH, file)
            dst = os.path.join(IPOD_PATH, file)
            shutil.copy(src, dst)

    print("Copied to iPod.")

# -----------------------------
# EXECUTION
# -----------------------------
def execute_one():
    displayQueue()
    artist = input("Which artist to run: ")

    if artist not in yt_links:
        print("Not found.")
        return

    link = yt_links[artist][0]

    print("Downloading...")
    download_audio(link)

    print("Converting...")
    convert_folder()

    print("Copying...")
    copy_to_ipod()

    print("Done.")

def execute_all():
    if not yt_links:
        print("Queue empty.")
        return

    for artist in yt_links:
        print(f"\nProcessing {artist}...")

        link = yt_links[artist][0]

        download_audio(link)
        convert_folder()
        copy_to_ipod()

    print("\nAll done.")

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:
    displayMenu()
    option = getInput()

    if option == 1:
        displayQueue()
        input("\n...")

    elif option == 2:
        addToQueue()
        input("\n...")

    elif option == 3:
        removeFromQueue()
        input("\n...")

    elif option == 4:
        execute_one()
        input("\n...")

    elif option == 5:
        execute_all()
        input("\n...")

    elif option == 0:
        print("Goodbye.")
        break

    else:
        print("Invalid option.")
