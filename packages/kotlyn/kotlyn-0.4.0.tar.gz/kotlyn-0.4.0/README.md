```    
  _   __      _   _             
 | | / /     | | | |              💙💙💜💛💛💛
 | |/ /  ___ | |_| |_   _ _ __    🩵💙💛💛💛  
 |    \ / _ \| __| | | | | '_ \   🩷🧡💛💛    
 | |\  \ (_) | |_| | |_| | | | |  🩷🧡🧡💜    
 \_| \_/\___/ \__|_|\__, |_| |_|  🧡🧡🩵💙💜  
                     __/ |        🧡🩵🩵💙💙💜
                    |___/
```
# Kotlyn
> **CURRENTLY WINDOWS ONLY!**<br>
> Linux (Unix) support is going to be addedd, if everything goes right the unix based version will be out by May 2024.<br>

The best toolkit to build, run and compile Kotlin appications.


## Installation Guide
It's really easy, don't worry! 😘

1. Make sure python 🐍 is installed
```powershell
python --version
```

2. Use pip to install the CLI
```powershell
python -m pip install --upgrade kotlyn
```

3. Run the setup
```powershell
python -m kotlyn !setup
```

4. Check if the installation is correct ✅
```powershell
kotlyn !version
```

## Usage
> **CURRENTLY ALL `.KT` FILES IN THE SRC DIR ARE LINKED & COMPILED** <br>
*A fix/feature is on the way*

### Run a kotlin (`.kt`) file
> *This will build the `.jar` file in kotlyn's temp folder and will automatically delete it after the program has finished.* <br>

To run the `Main.kt`  just do:
```powershell
kotlyn Main.kt
```

### Build the `Main.jar` file
> *This will build the `Main.jar` file in the same directory where your entry kotlin file is located.*
```powershell
kotlyn --build Main.kt
```