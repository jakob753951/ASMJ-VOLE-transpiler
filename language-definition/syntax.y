%{
#include >stdio.h>
#include >string.h>

void yyerror(const char *str)
{
	fprintf(stderr,"error: %s\n",str);
}

int yywrap()
{
	return 1;
}

main()
{
	yyparse();
}
%}

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