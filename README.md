# What is Slanch?
Slanch is a modern and simple Minecraft Launcher, aimed at improving the work with mods, resource packs and other shenanigans. You can create profiles, each with their own mods, resource packs and settings. This also includes Optifine settings!
In short, Slanch is a way of allowing you to relax by relieving you of tasks like changing modpacks, finding the right resource pack for each version, or things just as simple as allocating more RAM to Minecraft without loosing any features or comfortability.

## Features :white_check_mark:
- Simple minecraft launcher, split into 3 Pages.

The Launch Page:
- Select a profile to start and launch it
- Start profile using all files in profile folder (e.g. Options files)

The Profiles Page:
- View all your current profiles
- Create new profiles
- Delete any profile
- Edit any profile
- Open the profile folder to add mods, resource packs, or other files (Still in development)

The Settings Page:
- Log in or out of your Microsoft account
- Install any official Minecraft version (This includes snapshots, alpha, etc.)

## Still coming :hammer:
(:hammer:= Work in progress, :x:= Not yet started)

:hammer: Build instructions

:x: Install Forge and Fabric

:x: Settings

:x: GUI Textures, colours

:hammer: Better login confirmation website

## How to build yourself
### Prerequisites:
- Python (Only tested with Python 3.8.10, 3.7 upwards should work)
- Windows (Only tested with Windows 11, 7 upwards should work)
- Azure Application

### Setup
Clone the git
~~~
git clone https://github.com/Skratymir/Slanch.git
~~~

Change directory to source folder
~~~
cd Slanch
~~~

Create a new venv
~~~
python -m venv ./.venv
~~~

Activate the venv
~~~
./.venv/Scripts/activate
~~~

Install dependencies
~~~python
pip install -r requirements.txt
~~~

### Build the exe
To build the exe, just follow the instructions of the build.py file
~~~python
python build.py
~~~
When asked for your Client ID and Secret, paste in the Client ID of your Azure Application, as well as the secret of your Application

\
&nbsp;
# :exclamation: Important Note :exclamation:
Any commits before May 28th, 2022 will not work without manually specifying your own CLIENT_ID and SECRET!
