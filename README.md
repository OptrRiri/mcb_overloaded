mcb but with a bunch of unnecessary crap

how to use:

1. download mcb_overloaded to target folder
2. in a vscode terminal, navigate to the mcb_overloaded directory
3. in terminal: execute "python -m venv venv"
4. in terminal: execute "pip install -r requirements.txt"
5. in file explorer, navigate to the mcb_overloaded directory
6. in file explorer, navigate to mcb/logs
7. check if all 3 word document files can be opened; if they can't, re-create all 3 word document files with the same names (content does not matter)
   
(if existing mcb.bak, mcb.dat and mcb.dir files already exist; otherwise ignore steps 8 and 9) 
8. in file explorer, navigate to mcb/store
9. paste existing mcb.bak, mcb.dat and mcb.dir files in mcb/store

(creating batch files to run using Win+R)
- in a directory with PATH access, create file 'mcbo.bat' and 'mcbogui.bat'
- in both files, on a new line, type 'cd', then paste the directory path of the mcb_overloaded directory
- in 'mcbo.bat', add the line 'venv\Scripts\python -m mcb.mcb %*'
- in 'mcbogui.bat', add the line 'venv\Scripts\python -m mcb.mcbgui %*'

(running mcb via terminal)
- in a vscode terminal, navigate to the mcb_overloaded directory
- type "venv\Scripts\python -m mcb.mcb ", followed by keyword and any other flags

(running mcbgui via terminal)
- in a vscode terminal, navigate to the mcb_overloaded directory
- type "venv\Scripts\python -m mcb.mcbgui"
