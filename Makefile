.PHONY: oracle test benchmark verify
oracle:
	mkdir -p build
	cc -std=c11 -Wall -Wextra -Werror -pedantic -O2 legacy/sensor_config.c -o build/oracle
test: oracle
	python -m unittest discover -s tests -v
benchmark: oracle
	python -m benchmark.cli run
verify: test
	npm run typecheck
	npm run build
