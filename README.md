# The `adaptsim` repository

## About

`adaptsim` is the python repository to calculate adaptive fractionation schemes with simulations on real and synthetic data. It also allows to plot sparing factors from real patient data.


## Installation

It is recommended to create a virtual environment using the `venv` module:

```
$ python3.10 -m venv jupyter_env
```

activate the virtual environment
```
$ cd jupyter_env
$ source bin/activate
```

To install the `adaptsim` package

```
$ git clone https://github.com/openAFT/adaptsim.git
$ cd adaptsim
$ pip install . -e
```

the command line tool for simulation is then available
```
$ ast [options] -f <patient_model> -s <simulation_file>
```


```
$ pip install -U pip setuptools wheel
$ pip install -r requirements.txt
```