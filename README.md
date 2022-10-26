# smmrt
sharing python and R tools that everyone needs

to install:
- navigate to directory where you would like to place the git folder
- open git bash 
- `git clone https://github.com/vskode/smmrt.git`

to create an environment:
- `conda create --name env_smmrt`
- `pip install -r requirements.txt`

to run a file, for example the resample_files.py script:
- `conda activate env_smmrt`
- `python resample_files.py`

to update your local repository:
- if you have made changes to files, that you don't mind discarding: `git stash`
- `git pull`
- if you have made changes that you would like to add to the remote repository:
- `git add _name_of_changed_files_` or if you want to add all changed files `git add .`
- `git commit -m "message about what you have changed"`
- `git push`