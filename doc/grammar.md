# Formal grammar

## as built

element | production
--- | ---
*_declaration_ := | _statement_
| | &#124; ` `  `var` -> _var_declaration_
| | &#124; ` `  `def` -> _definition_
| | &#124; ` `  `%%` -> _command_
*_statement_ := | _block_expr_
| | &#124; ` `  _statement_ ` ; ` _statement_
*_block_expr_ := | _expression_
| | &#124; ` `  `{` _block_ `}`
| | &#124; ` `  `{` _block_ `}  :  (` _tuple_ ` )`
| | &#124; ` `  `{` _block_ `}  :  {` _block_ ` }`
| | &#124; ` `  `any:{` _block_ `}`
| | &#124; ` `  `all:{` _block_ `}`
| | &#124; ` `  `none:{` _block_ `}`
*_expression_ := | _assignment_
| | &#124; ` ` _assignment_  ` ` &#124; ` ` _assignment_ | chain expressions
| | &#124; ` `  _assignment_ `=>` _assignment_ | produce (raise)
| | &#124; ` `  _assignment_ `>>` _assignment_ | apply
| | &#124; ` `  _assignment_ `->` _assignment_ | tbd
*_assignment_ := | _boolean_expr_
| | &#124; ` `  `(` _tuple_ `)`
| | &#124; ` `  `(` _tuple_ `) =` _expression_
| | &#124; ` `  `(` _tuple_ `) :=` _expression_
| | &#124; ` `  `(` _tuple_ `) +=` _expression_
| | &#124; ` `  `(` _tuple_ `) -=` _expression_
*_tuple_ := | _boolean_expr_
| | &#124; ` ` `all: ` _tuple_
| | &#124; ` ` `any: ` _tuple_
| | &#124; ` ` `none: ` _tuple_
| | &#124; ` `  _tuple_ ` : ` _tuple_ | k:v pair definition
| | &#124; ` `  _tuple_ ` , ` _tuple_
*_boolean_expr_ := | _equality_ [ `and` &#124; `or` ] _equality_
*_equality_ := | _comparison_ [ `!=` &#124; `==` ] _comparison_ ]*`
*_comparison_ := | _term_ [ `>` &#124; `>=` &#124; `<` &#124; `<=` &#124; `in` ] _term_
*_term_ := | _factor_ [ `-` &#124; `+` ] _factor_
*_factor_ := | _unary_ [ `/` &#124; `*` &#124; `div` &#124; `mod` ] _factor_
*_unary_ := | [ `-` &#124; `!` &#124; `not` ] _unary_
| | &#124; _primary_
*_primary_ :=  | `NUMBER`
| | &#124; ` `  `DATETIME` 
| | &#124; ` `  `DURATION`
| | &#124; ` `  `SET` 
| | &#124; ` `  `STRING`
| | &#124; ` ` ` true ` &#124; ` false` &#124; `  none`
_block_ := | _declaration_
| | &#124; ` `  _declaration_ ` , ` _declaration_
_command_ := | _expression_ `+` _EOL_
_definition_ := | _tuple_ `:= ` _statement_ | defines a _var_function_
| | &#124; ` `  _tuple_ `= ` _statement_ | defines a _value_function_
_var_declaration_ := | _tuple_ ` := ` _statement_ | defines a _var_function_
| | &#124; ` `  _tuple_ ` = ` _statement_ | defines a _variable_ (tbd)

> TODO: _definition_ includes ':=' parsing which should be surfaced into _declaration_
> 
> TODO: _assignment_ contains `:=', '=', '+=', '-=' parsing.  should it? this seems like duplication
> 
> TODO: _tuple_ parsing should at least mention `(` and `)`
> 
> TODO: _tuple_ parsing is incorrect for k:v pair parsing & perhaps set notation should move elsewhere
> 
> TODO: add in ranges 0..5, a..b
>
----

## idealized

element | production
--- | ---
`declaration :=` | `'var' -> var_declaration`
| | `\| 'def' -> definition`
| | `\| '%%' -> command`
| | `\| term + ':=' + statement`
| | `\| block_expression`
`expression :=` | `boolean_expression`
| | `\| '{' + block + '}'`
| | `\| '{' + block + '}' + ':' tuple`
| | `\| '{' + block + '}' + ':' '{' + block + '}'`
`block :=` | `declaration`
| | `\| declaration ',' + declaration`

----

## original fragment

element | production
--- | ---
`expression :=`  | `literal`
| | `\| unary`
| | `\| binary`
| | `\| assignment`
| | `\| fn_call`
| | `\| grouping`
| | `\| flow`
| | `\| expression ';' expression`

## cutting board

element | production
--- | ---
| | `\| block_expression`
`block_expression :=` | `expression`
| | `\| '{' + block + '}'`
| | `\| '{' + block + '}' + ':' tuple`
| | `\| '{' + block + '}' + ':' '{' + block + '}'`
| | `\| block_expression [ ';' block_expression ]+`
`expression :=` | `boolean_expression`
| | `\| '{' + block + '}'`
| | `\| '{' + block + '}' + ':' tuple`
| | `\| '{' + block + '}' + ':' '{' + block + '}'`
| | `\| expression + [';' expression]+`
| | `\| expression + ['\|' + expression]+`
| | `\| expression + ['>>' + expression]+`
| | `\| '(' expression ')'`
`assignment :=` | `identifier '=' expression`
`flow :=` | `expression [ '\|' expression ]*`
`fn_call :=` | `scoped_identifier parameter_list`
`parameter_list :=` | `'(' [ expression [ ',' expression ]* ]* ')'`
`identifier :=` | `[a-zA-Z_]+ [0-9]* [a-zA-Z_]*`
`unary :=` | `[ '-' \| '!' \| 'not' ] expression`
`binary :=` | `expression operator expression`
`operator :=` | `'==' \| '!=' \| '<' \| '<=' \| '>' \| '>=' \| 'and' \| 'or' \| '+' \| '-' \| '*' \| '/' \| '^' \| \| '>>'`
`set :=` | `'{' [ expression [, epxression]* ]*  '}'`
`number :=` | `integer \| float`
`integer :=` | `[0-9]+`
`float :=` | `[$]* [0-9]+ . [0-9]+`    # [0-9]* . [0-9]+ might be valid also.
`datetime :=` | `<date value> \| <time value> \| <datetime value> ` # precision to milliseconds allowed
`duration :=` | `number [ 'h' \| 'm' \| 's' \| 'd' \| 'mo' \| 'M' \| 'y' ]`
| | `\| '(' expression ')'`
`grouping :=` | `'(' expression ')'`
`| |` `\| '(' expression ')'`
