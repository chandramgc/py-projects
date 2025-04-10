# py-projects

## Execution commands

```bash
python dependency_finder.py code
```

```bash
Dependency Graph:
-----------------
Module: commands
  depends on: persistence
  depends on: todolist

Module: main
  depends on: commands
  depends on: persistence
  depends on: todolist

Module: persistence
  depends on: task
  depends on: todolist

Module: task
  no dependencies

Module: todolist
  depends on: task
```