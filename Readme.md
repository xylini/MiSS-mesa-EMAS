
# Evolutionary Multi-Agent Systems  Mesa implementation  
  
## Summary  
  
Python Mesa framework implementation of basic Evolutionary Multi-Agent Systems based on http://home.agh.edu.pl/~drezew/papers/drezewski2015evolutionary.pdf paper.  
  
Emas module enables a multi island agent simulation with basic EMAS operations: 
* reproduction, 
* death, 
* migration.
  
  
## Installation and run
### Unix based
  
  * Run `run_for_linux.sh` file at project top level
  
### Windows
  * Run console at project top level
  * Create new virtual env: `python3 -m venv venv` - only before first run
  * After that type: `call .\\venv\\Scripts\\activate.bat`
  * `pip install -r requirements.txt` - only before first run
  * `python run_hawk_dove.py`
  
## Hawk and dove implementation

Symulation of a popular [https://en.wikipedia.org/wiki/Chicken_(game)](https://en.wikipedia.org/wiki/Chicken_(game)). 

Hawks and doves interaction outcomes are listed below:

|  | HAWK | DOVE |
|--|--|--|
| HAWK | -3 \ -3 | 1 \ 1 |
| DOVE |-1 \ 1  | 0.5 \ 0.5 |