[![](https://img.shields.io/maintenance/yes/2024)](https://github.com/jcivitel/)
[![GitHub issues](https://img.shields.io/github/issues/jcivitel/py_djoin_api)](https://github.com/jcivitel/py_djoin_api)
[![GitHub Repo stars](https://img.shields.io/github/stars/jcivitel/py_djoin_api)](https://github.com/jcivitel/py_djoin_api)
[![GitHub License](https://img.shields.io/github/license/jcivitel/py_djoin_api)](https://github.com/jcivitel/py_djoin_api)

# What is the goal of the project?

Joining a computer using the `Djoin` program is a process where the computer is inserted into the domain to gain access to domain resources. This involves creating a provisioning file with the computer's configuration information and executing the `Djoin` command to enroll the computer with this information into the domain.

This project is a working API for webrequests.
<br>

## How to use the binary?

#### If you want to run this project as a windows service, you need to execute following steps:

1. open CMD

1. execute `py_djoin_api.exe --startup auto install`

1. run the service by executing `py_djoin_api.exe start` or `net start py_djoin_api`

#### If you want to run this project just once, you need to execute following steps:

1. open CMD

1. execute `py_djoin_api.exe debug`

## How to install the project?
1. Begin by cloning the repository to a designated local directory on your machine.
```console
git clone https://github.com/jcivitel/py_djoin_api.git
```
2. Launch a Command Prompt (CMD) and navigate to the specified directory. Once in the directory, execute the following command:
```python
python -m venv venv
```

3. Once the virtual Python environment has been successfully created, it is now possible to compile the project:
#### Linux
```python
. venv/bin/activate
pip install -r requirements.txt
pyinstaller --onefile py_djoin_api.py --hidden-import=win32timezone --clean --uac-admin
```
#### Windows
```python
./venv/Scripts/activate.bat
pip install -r requirements.txt
pyinstaller --onefile py_djoin_api.py --hidden-import=win32timezone --clean --uac-admin
```



<br>

## Contributors
[![Contributors Display](https://badges.pufler.dev/contributors/jcivitel/py_djoin_api?size=50&padding=5&bots=false)](https://github.com/jcivitel/py_djoin_api/graphs/contributors)
