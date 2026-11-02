CONFIG ?= config.yaml

.PHONY: run test demo

run:
	python3 -m src.main $(CONFIG)

test:
	python3 -m unittest -v

demo:
	python3 -m src.main configs/simple.yaml
	python3 -m src.main configs/cycle.yaml
	python3 -m src.main configs/deep.yaml
