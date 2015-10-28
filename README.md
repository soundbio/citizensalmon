##Citizen Salmon!

### Setup Instructions

First, install `virtualenvwrapper` (might require sudo):
```
$ pip install virtualenvwrapper
```

Then, add the following three lines to your shell startup file (either `~/.bashrc`, or `~/.profile`)
```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh
```

Open a new terminal (or `source ~/.bashrc`) to reload wherever you added the three lines.

Now you have virtualenvwrapper installed and you can create python virtual environments!

Create a virtualenvironment for citizen salmon and install the project requirements
```
$ mkvirtualenv salmon
$ pip install -r requirements.txt
```

Now you're ready to salmon!

Whenever you want to work on the project, do:
```
$ workon salmon
```




