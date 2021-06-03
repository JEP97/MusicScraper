import sys
from cx_Freeze import setup, Executable

# setup files required to run cx_Freeze

base = None

if sys.platform == 'Win32':
    base = 'Win32Gui'

setup(
    name="Kiss 925 JB Scraper",
    options={"build.exe": {"packages": [""]}},
    version="1.1",
    description="A program to scrape kiss92.5 to see if JB is playing on the radio",
    executables=[Executable("main.py", base=base)],
    requires=['telegram', 'schedule', 'requests', 'time', 'pickle', 'os.path']
)