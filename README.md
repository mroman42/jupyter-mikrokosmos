# IMikrokosmos
**IMikrokosmos** is a Jupyter/IPython kernel for
the [Mikrokosmos](https://github.com/mroman42/mikrokosmos) lambda
interpreter.

**Important**: Please note that this Jupyter kernel only works on
Windows on its `windows-support` branch. Certain features, such
as unicode output, cause problems in this case. Windows users may
also use the Windows Subsystem for Linux (WSL). Note that only
WSL1 has been tested.

![mikrokosmos2](https://user-images.githubusercontent.com/5337877/28381708-11a1608a-6cbc-11e7-80da-2292d4716cdb.png)


## Installation

```
sudo pip install imikrokosmos
```


### Manual installation
The `kernel.json` file must be placed inside a folder named
`jupyter-mikrokosmos` in one of the following paths

```
~/.local/share/jupyter/kernels/jupyter-mikrokosmos/
/usr/share/jupyter/kernels/jupyter-mikrokosmos/
```

the `mikrokosmoskernel.py` file must be available for Python on the
working directory, or, more generally, on
the [sys-path](https://docs.python.org/2/library/sys.html#sys.path).

## Support and contributing

If you are an user seeking support, please use the 
[GitHub issue tracker](https://github.com/mroman42/mikrokosmos/issues)
of the main repository. The main repository also provides a CONTRIBUTING
file where contribution guidelines are detailed.
