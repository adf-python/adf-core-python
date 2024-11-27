# sphinx-documentation

## Generate documentation

```bash
sphinx-apidoc -f -o ./docs/source ./adf_core_python
sphinx-build -M html ./docs/source ./docs/build -a
```
