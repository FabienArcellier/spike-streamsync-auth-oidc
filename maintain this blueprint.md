# Maintain this blueprint

This blueprint is a python project template. It may need to be rebuilt regularly, especially to update the stack dependencies.

### 1. update the dependencies

```bash
poetry add streamsync@latest
```

### 2. refresh streamsync application

```bash
rm -rf src/app
poetry run streamsync create src/app
touch src/app/static/main.css
```

### 3. register the custom stylesheet

*src/app/main.py*
```python
initial_state.import_stylesheet('main', '/static/main.css')
```
