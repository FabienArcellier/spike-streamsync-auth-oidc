# Prepare the blueprint to use it as your project base

1. change the project metadata into `./pyproject.toml`

```toml
name = "blueprint-streamsync"
description = "blueprint to implement a python application"
authors = ["Fabien Arcellier <fabien.arcellier@gmail.com>"]
license = "MIT"
```

2. configure the .env file

copy the `.env.template` file into `.env` and change the value of the environment variables to adapt the project behavior between development and production.

3. remove the markdown files relative to the blueprint

```bash
rm "prepare the blueprint.md" 
rm "maintain this blueprint.md"
```

4. modify the CI badget for github action in the readme

The github action badge must point to your repo instead of the blueprint for the badge to match your project.

```markdown
[![ci](https://github.com/{...}/actions/workflows/main.yml/badge.svg)](https://github.com/{...}/actions/workflows/main.yml)
```

5. modify section Run in gitpod in README.md

The ![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg) command should point to your repository instead of the blueprint one

```markdown
[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/...)
```
