# CodeTrack

This is a software that employers and employees or independent developers can use to keep a fair track of time using hackatime or wakatime api. 
It provides a clean UI to make the process easy with additional and necessary features for employers. This is lacking in many features and security in the current release but future updates will make it much better.

I implemented it by studying the hackatime repositories using AI and understanding how things work behind the shell, the api injection into the wakatime configuration file and extension installation, etc. It's somewhat simple, in a way...

# Features

### Enterprise Time Tracking

- Employers can generate a secure code using a wakatime/hackatime api key, different for every employee.
  - It will contain the api key (ofc)
  - It may contain a url to their website or their time tracking dashboard website or hackatime website, etc.
  - It may have an employee name as the host_name otherwise the host_name is set at random.
- It is then used by their employees to install wakatime and start tracing time for fair pay and surveillance (I guess?).

###### Currently, the secure code is not very secure. In future versions, it will be processed online making it industry grade and actually secure.  

### Independent Usage

- Solo developers/freelancers can use their, or a provided, unsecured normal API key to track project time for:
  - personal tracking because what is measured is improved
  - or to showcase their clients

### Automatic VS Code Plugin Injection
VS Code plugin is automatically installed. 
###### More plugins in future versions.

### Zero Knowledge Required

- It is very easy to use so people with negligible knowledge can use it for a smooth installation. 
- You may think it's redundant because devs wouldn't mind but with much more features for employers, this will matter.

### Cross-Platform
- Available as a mac .app
###### For Windows & Linux in future release

# Tech Stack
- **Language:** Python
- **GUI:** CustomTkinter
- **Security:** cryptography, ssl, urllib
- **Packaging:** PyInstaller
- **Code Obfuscation:** PyArmor 8
- **Deployment:** PyInstaller, GitHub Actions

# Minor Issues
- None that I've found for now.

# Future

### Version 0.2
- More IDE detection and customizable, automatic plugin installation
- Windows app

### Version 0.3
- Multi-user generation for employers
- Linux release

### Version 0.4 
- Dashboard with three views: Employers, Employees, Independent and maybe a 4th shared view

### Version 1.0
- UI overhaul as currently, it looks pretty ugly imo. It is only a prototype for now, a stepping stone.
- Improved security for key via cloud verification

# How to Run Locally (macOS)

### 1. Environment Setup
**Clone the repository**
```bash
git clone https://github.com/utkarsh29raj10-web/CodeTrack.git
cd CodeTrack
```

**Create and activate a Python virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Install the required dependencies and tools**
```bash
pip install -r requirements.txt
pip install pyarmor pyinstaller
```

**Secure Key**
Create a ".env" file in your root folder containing `MASTER_KEY="your_secure_key"` which can be a randomly generated key. 
Then run this script to safely inject it into the source code:
```bash
python build_secrets.py
```

**Code Obfuscation**
Protect the source code and your embedded keys from reverse engineering by obfuscating the project with PyArmor:
```bash
pyarmor gen -O obf_dist main.py core/
```

**Build Configuration**
Inside the `obf_dist` folder, create a file named `imports.py` and paste this:
```python
import customtkinter
import cryptography
import urllib.request
import ssl
import zipfile
import json
import configparser
import threading
import stat
import platform
import os
import logging
from cryptography.fernet import Fernet
import core.security
import core.installer
import core.config
import core.secrets
```

**App Compilation**
Compile the obfuscated code into a macOS ".app":
```bash
cd obf_dist
pyinstaller --clean --windowed --name "CodeTrack" --hidden-import imports --collect-all customtkinter main.py
```
Find and run the app from here: `root/obf_dist/dist/CodeTrack.app`.

# For Beest Reviewers

## AI is used for:
This is detailed information but the overall amount for each case is not significant. Thus, total AI usage will remain well under 15-20%
- Project Development Plan
- Initial guide to explain me how I can pull this off with hackatime
- Taught myself basics of automated testing and AI acted as an example guide for first test
- Writing github workflow for windows executable

## File Structure
- All antigravity files, other AI files and other random files' time was tracked. And when I say all, I mean **ALL**. Even the files which have nothing to do with this or any project for that matter.
- I was instructed to mention this and the file structure of my project so that the reviewer cna cut time accordingly. 

##### So here's the file structure:

```text
Codetrack/
├── main.py   
├── .env
├── .gitignore                     
├── README.md                 
├── build_secrets.py         
├── requirements.txt         
├── tests/                    
│   ├── test_config.py            
│   └── test_security.py
├── core/                    
│   ├── config.py            
│   ├── installer.py         
│   ├── secrets.py           
│   └── security.py                    
├── .github/
│   └── workflows/
│       └── build-windows.yml 
```

## Screenshots
<img width="912" height="744" alt="Screenshot 2026-07-11 at 4 14 46 PM" src="https://github.com/user-attachments/assets/1fa6fe2e-5571-4795-a94b-6284d52375ac" />
<img width="912" height="744" alt="Screenshot 2026-07-11 at 4 12 58 PM" src="https://github.com/user-attachments/assets/a88a3942-1502-4b96-b9aa-8e569f8753af" />
<img width="912" height="744" alt="Screenshot 2026-07-11 at 4 12 54 PM" src="https://github.com/user-attachments/assets/43da2dce-ce90-450f-a18a-f93573a283ee" />
<img width="912" height="744" alt="Screenshot 2026-07-11 at 4 12 52 PM" src="https://github.com/user-attachments/assets/470918f3-b2b0-4701-b978-973feb8af453" />
<img width="912" height="744" alt="Screenshot 2026-07-11 at 4 12 50 PM" src="https://github.com/user-attachments/assets/ffa25f30-80f6-402a-8ce7-2eecebb04d98" />
