# module-importer

This is a Python module for importing modules.

## Usage


```python 

pip install module-importer

```

Import the module:

```python
from module_importer import ModuleLoader
```

Initialize in with valid path to modules:

```python
loader = ModuleLoader[SomeClassTypes]('valid/path')
```

Load modules

```python
loader.load_modules()
```


Use these modules:

```python
for module in loader.modules:
    module.propery
```



## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you would like to contribute.

