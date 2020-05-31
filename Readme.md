
# Evolutionary Multi-Agent Systems  Mesa implementation  
  
## Summary  
  
Python Mesa framework implementation of basic Evolutionary Multi-Agent Systems based on http://home.agh.edu.pl/~drezew/papers/drezewski2015evolutionary.pdf paper.  
  
Emas module enables a multi island agent simulation with basic emas operations: reproduction, death, migration.  
  
  
## Installation  
  
To install the dependencies use pip and the requirements.txt. Use run_emas.py to start EMAS template server.  
  
## Hawk and dove example

Symulation of a popular [https://en.wikipedia.org/wiki/Chicken_(game)](https://en.wikipedia.org/wiki/Chicken_(game)). 

Hawks and doves interaction outcomes are listed below:

|  | HAWK | DOVE |
|--|--|--|
| HAWK | -3 \ -3 | 1 \ 1 |
| DOVE |-1 \ 1  | 0.5 \ 0.5 |

Use run_hawk_dove.py to run hawk and dove server.