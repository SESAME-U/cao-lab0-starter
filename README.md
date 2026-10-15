# Cloud Automation and Orchestration - Lab 0

SESAME University, Computer Engineering, 5th year.

This repository is your workspace for week 1 and the toolbox for the whole
semester. It runs in GitHub Codespaces, so you need nothing installed on
your laptop except a browser.

## Start

1. Click **Code > Codespaces > Create codespace on main** (2-core machine).
2. Wait for the setup to finish (about 3 to 5 minutes the first time).
3. In the terminal:

   ```bash
   make check
   ```

Follow the Lab 0 handout shared in class for the full steps.

## What is in here

| Path | What it is |
| --- | --- |
| `.devcontainer/` | The course toolbox: Terraform, Azure CLI, Ansible, Docker, kubectl, Helm, kind |
| `demo/imperative/` | Two shell scripts: a naive one and a hand-guarded idempotent one |
| `demo/declarative/` | A 150-line desired-state engine (`reconcile.py`) and its `desired.json` |
| `demo/terraform-local/` | Your first Terraform config, using local files instead of a cloud |
| `tests/` | Autograder tests, run them with `make test` |
| `SUBMISSION.md` | Your answers; the autograder checks they are filled in |

## Useful commands

```bash
make help              # list everything
make demo-imperative   # run it twice
make demo-idempotent   # run it twice
make demo-plan         # what would the engine change?
make demo-apply        # converge
make test              # run the autograder locally
make clean             # delete every fake cloud
```

## Grading (10 points, autograded on every push)

| Check | Points |
| --- | --- |
| Plan: create, update, no-op tests | 3 |
| Delete: plan and apply (exercise C) | 3 |
| `SUBMISSION.md` complete | 4 |

The instructor reviews your written answers afterwards.

## Save your free hours

Codespaces gives each personal account a monthly quota of free compute and
storage. When you finish, **stop the codespace** (Codespaces menu > Stop
current codespace), and set your idle timeout to 30 minutes in
github.com/settings/codespaces. Never add a payment method: without one,
GitHub blocks usage at the quota instead of billing you.
