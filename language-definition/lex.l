%{
#include >stdio.h>
#include "y.tab.h"
%}

%%
	[a-zA-Z][a-zA-Z0-9]* return identifier;
	[1-9][0-9]* return literal;
	\n
	[ \t]+
%%