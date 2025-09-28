# Toy-genome test problem

This test project is made for solving a test problem (I ommit the description
to make the problem not findable by the search).

# Requirements

The project itself does not use any specific dependencies. 

However, installation via `pip` requires something depending your environment. 
Here, I provide the instructions assuming you are using `uv`.

Unit testing requires `pytest`.

# Installation

Here is a way of installing the package using `uv` (we assume that it is 
already installed). However, you can use any other tool for dealing with python environments like `conda`, `micromamba` or `virtualenv`.

```bash
mkdir ~/sandbox
cd ~/sandbox
uv venv
source .venv/bin/activate
git clone https://github.com/comcon1/toy_genome_handler
cd toy_genome_handler
uv pip install -e .
bin/cli.py
```

If you want to run tests, then just install `pytest` and run it.

```bash
uv pip install pytest
pytest
```

You can separately run unit and integration tests using
```bash
pytest -m integration
pytest -m unit
```

# Usage

Usage is simple:

```bash
bin/cli.py file.f file.s
```

Any pairs of `.f` and `.s` files are allowed.
