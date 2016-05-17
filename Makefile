file = example.mdl
make: $(file) lex.py main.py matrix.py mdl.py script.py yacc.py
	python main.py $(file)

clean:
	rm *pyc *out parsetab.py

clear:
	rm *pyc *out parsetab.py *ppm
