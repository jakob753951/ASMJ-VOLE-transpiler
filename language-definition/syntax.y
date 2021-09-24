%token int float
%token identifier
%token literal

%%

declassign  : type assignment
			;

declaration	: type identifier
			;

assignment	: identifier '=' expression
			;

expression	: expression '+' expression
			| expression '|' expression
			| expression '&' expression
			| expression '^' expression
			| identifier
			| literal
			;

mark		: identifier ':'
			;

type		: int
            | float
			;

%%