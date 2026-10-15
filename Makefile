.PHONY: help check test demo-imperative demo-idempotent demo-plan demo-apply clean

help:
	@echo "make check            verify the toolbox (Lab 0, step 3)"
	@echo "make test             run the autograder tests locally"
	@echo "make demo-imperative  run the naive script (try it twice)"
	@echo "make demo-idempotent  run the guarded script (try it twice)"
	@echo "make demo-plan        declarative engine: show the plan"
	@echo "make demo-apply       declarative engine: converge"
	@echo "make clean            delete every fake cloud"

check:
	@bash scripts/check.sh

test:
	@python3 -m pytest -q tests

demo-imperative:
	@bash demo/imperative/provision.sh

demo-idempotent:
	@bash demo/imperative/provision-idempotent.sh

demo-plan:
	@python3 demo/declarative/reconcile.py plan

demo-apply:
	@python3 demo/declarative/reconcile.py apply

clean:
	rm -rf .fakecloud-imperative demo/declarative/.fakecloud demo/terraform-local/out
	@echo "Fake clouds deleted."
