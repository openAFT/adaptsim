# The `adaptsim` repository

## About

`adaptsim` is the python repository to calculate adaptive fractionation schemes with simulations on real and synthetic data. It also allows to plot sparing factors from real patient data. Essentially it is an example implementation of simulated adaptive fractionated plans using the package `adaptfx`.


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
$ pip install -e .
```

Install adaptfx with pip
```
$ pip install adaptfx
```

or manually build from source
```
$ cd aft_env
$ source bin/activate
$ git clone https://github.com/openAFT/adaptfx.git
$ cd jupyter_env/adaptsim
$ pip install -e /path/to/aft_env_/adaptfx
```


the command line tool for simulation is then available
```
$ ast [options] -f <patient_model> -s <simulation_file>
```


```
$ pip install -U pip setuptools wheel
$ pip install -r requirements.txt
```