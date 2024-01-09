# ivette-client

Python client for Ivette Computational chemistry and Bioinformatics project.
Made in the Central University of Venezuela for research purposes.

## Installation

A technical level knowledge of computational chemistry and CLI management is required
to use this program.

Notice this program is currently in alpha stage, thus the following instructions
might vary depending on the system, warnings and or errors might appear and yet
the program could work seamlessly. We'd gratefully receive your feedback and
questions if you submit an issue.

This program is made mainly to run in Unix based systems (Linux and maybe MacOs).
If you happen to be using windows (>=10) you can install WSL (windows subsystem 
for Linux) easily via:

  PowerShell:
```bat
wsl --install
```

First off python must be installed, it ussualy comes pre-installed in Linux distros. 
If not, you can install as follows:

  bash:
```bash
sudo apt update
sudo apt install python3
```

We also recommend you updating pip before doing the installation:

  bash:
```
pip install --upgrade pip
```

Openbabel is also required for everything to work:

  bash:
```bash
sudo apt-get install openbabel
```

We recommend using pipenv to install the package as it provides an isolated local environment that avoid collisions with other packages:

  bash:
```bash
pip install -U pipenv
```

Provided pip is installed (ussualy comes preinstalled along with python).
To install ivette CLI:

  bash:
```bash
pip install -U ivette
```

Or in case you're using pipenv:

  bash:
```bash
pipenv install --python 3.13
pipenv shell
```

Adittionaly you might need to set up the PATH variable to be able to use the command
line interface:

  bash:
```bash
echo "export PATH=\$PATH:/home/$USER/.local/bin" >> ~/.bashrc
sudo ~/.bashrc
```

We highly recommend you to install a computational chemistry software
right away if you dont have any. An easy choice is NWChem which
is avaiable in the linux APT and has plenty of capabilities
at the expense of being slower in comparison to other methods.

  bash:
```bash
sudo apt-get install nwchem
```

After this step the installation process is done, read the documentation to get started.

## Want to contribute?
Further documentation is required

## Support
Contact the dev team at:
eduardob1999@gmail.com

### Third-Party Dependencies

This project uses the following third-party libraries and dependencies:

- [Library A](https://github.com/authorA/library-a) - Licensed under the MIT License
- [Library B](https://github.com/authorB/library-b) - Licensed under the MIT License
- [Library C](https://github.com/authorC/library-c) - Licensed under the MIT License

