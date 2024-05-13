
# Elections Scraper

This program downloads data for chosen territorial unit based on url as 1st argument. Returns specific data for every district code with district name, number of voters, envelopes, valid votes and votes for parties in csv file named based on the 2nd argument.



## Installation

The virtual environment needs to be created and additional libraries installed.


1)  Virtual envirement:
- Open Visual Studio Code
- Create a folder where your data will be saved
- Press (Ctrl+Shift+P) and search for Python: Create Environment 
- Choose venv
- Choose Python version you want to work with (the newest one)
- Wait until you see environment created on the right down corner and .venv in your folder

2) Installing libraries
- Open terminal in VS Code
- Write: pip install (name of the library) and wait until the installation is successful
- For the purpose of this program you need to install beautifulsoup4 and requests

```bash
  pip install beautifulsoup4
  pip install requests
```


    
## Arguments 

The program will notify the user in case of incorrect input or in case any of the arguments are missing.
1) 1st mandatory argument  - url
- URL needs to be in the correct format
2) 2nd mandatory argument  - file name
- file name needs to contain .csv file type
- can not contain forbidden characters to be able to save the file

When starting a program both arguments are mentioned in the terminal of VS Code + enter:

```bash
'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101' 'benesov.csv'
```





## Demo

https://drive.google.com/file/d/1WrB9IwxAK6jpOqzFmgi8TOrtehm_Rr4x/view?usp=sharing


## Author

https://github.com/DominikaKubova)

