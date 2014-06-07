import fcc

fcc.run(fcc.compile(fcc.parse(fcc.lex(open("tests/basic.c").read()))))
