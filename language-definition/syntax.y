%{
#include <stdio.h>
#include <string.h>

int yywrap()
{
	return 1;
}
int yydebug = 1;

void yyerror (char *s) {fprintf(stderr, "%s\n", s);}
int yylex();
%}
%token TYPE IDENTIFIER LITERAL

%%

declassign  : TYPE assignment
			;

assignment	: IDENTIFIER '=' expression
			;

expression	: factor
			| expression '+' factor
			| expression '|' factor
			| expression '&' factor
			| expression '^' factor
			;

factor		: LITERAL
			| IDENTIFIER
			;

%%

int main (void) {return yyparse();}