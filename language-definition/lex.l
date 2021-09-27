%{
#include <stdio.h>
#include "y.tab.h"
extern int yylval;
%}

%%
(int|float) return TYPE;
[1-9][0-9]* return LITERAL;
[a-zA-Z][a-zA-Z0-9]* return IDENTIFIER;
\n
[ \t]+
%%