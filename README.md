# modelioPHPExport
Very simple macro to export classes and interfaces to php code.

# Current state
The modelioPHPExport.py macro can be used on interfaces and classes. It generates methods and extens/implements statements. 
Currently function parameters are generated untyped. Return types are also not generated.

The namespace is derived from the name of the parent package of the class/interface object.

The output folder has to be specified within the macro code. The folder has to exists.

