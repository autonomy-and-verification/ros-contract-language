Version 0.2

* RCL now includes a types clause, to declare global types. Vanda parses this, but doesn't care if it's not there (at the moment). I've combined the contracts for the case studies into on file each (in the 'demo' folder) so I now run it on one file: e.g.  `python3 vanda.py -t rosmon_rml rcl demo/curiosity.rcl` 

* Each RCL contract has an inputs and outputs list, listing the name and type of each variable.

* The topics list includes a 'matches' part, where you can link the topic name to its variable name (helpful for if they are different/for name clashes)

* RCL lets you say "out.var" to refer to a variable called "var" that is an output, or "in.var" to refer to a variable that is an input. Vanda doesn't check this currently, but that's something I plan to implement. 

* There have been other, smaller tweaks to the grammar, so that the translators have needed some updates. I've tried to move methods that only deal with the structure of the Abstract Syntax Tree up into the fol.py file.
