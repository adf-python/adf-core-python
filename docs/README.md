# sphinx-documentation

## Generate documentation

```bash
sphinx-apidoc -f -o ./docs/source/adf_core_python ./src/adf_core_python
sphinx-build -M html ./docs/source ./docs/build -a
```

## Generate localized documentation (Japanese)

```bash
sphinx-apidoc -f -o ./docs/source/adf_core_python ./src/adf_core_python
sphinx-build -M html ./docs/source ./docs/build -D language=ja -a
```
