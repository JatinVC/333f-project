# 333f-project
make a virtual environment by doing:
```
python -m venv env
```
in the repository folder.

then do:
```
pip install -r requirements.txt
```
to install all the dependencies to the environment.

Every time you install a new library using pip, please do:
```
pip freeze > requirements.txt
```
in order to keep the requirements.txt file updated so dependencies can be synced between the entire project
