# SW3-Workshop-10-27
Gym Membership Quote - Continuous Integration workshop (Jenkins + GitHub Actions)
#Prueba

## Run the tests

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install pytest pylint
pytest
pylint $(git ls-files '*.py')
```

## Workflow

Each member works on a `feature/<name>` branch and opens a pull request to `main`.
GitHub Actions must pass and another member must review before merging.
Every merge to `main` triggers a Jenkins build.

## Mensaje de Prueba para Webhook
## Mensaje de Prueba para Webhook Visual Studio Code
## Mensaje de Prueba para Webhook CI merged
