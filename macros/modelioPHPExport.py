def findParents(element):
    owner = element.getCompositionOwner()
    if (owner != None):
        isProject = (owner.getMClass().getName() == "Project")
        if (isProject):
            return owner
        else:
            return findParents(owner)
    else:
        return None

def indentPrint(txt, indent):
    return "%s%s" % (indent, txt)
    
def getOperationParamsStr(operation):
    ios = operation.getIO()
    paramStr = ""
    for io in ios:
        paramStr += ", $" + io.getName()
    return paramStr.strip(" ,")
    
def printOperation(operation, semicolon, indent):
    ret = ""
    fnHead = "public function " + operation.getName() + "(" + getOperationParamsStr(operation) + ")"
    if (semicolon):
        fnHead += ";"
        ret += indentPrint(fnHead,indent)
    else:
        ret += indentPrint(fnHead + "\n",indent)   
        ret += indentPrint("{\n",indent)
        ret += indentPrint("throw new \\Exception('Implementation missing');\n", indent + "    ")
        ret += indentPrint("}\n",indent)
    ret += "\n"
    return ret

def printInterface(interface, indent):
    ret = ""
    ret += indentPrint("interface " + interface.getName() + "\n", indent)
    ret += indentPrint("{\n", indent)
    for a in interface.getCompositionChildren():
        isOperation = a.getMClass().getName() == "Operation"
        if (isOperation):
            ret += printOperation(a,True, indent + "    ")
    ret += indentPrint("}\n", indent)
    return ret
    
def printClassRealizations(clazz, indent):
    ret = ""
    extends = ""
    implements = ""
    
    for realization in clazz.getRealized():
        isInterface = realization.getMClass().getName() == "InterfaceRealization"
        if (isInterface):
            implements += ", " + realization.getImplemented().getName()
    for parent in clazz.getParent():
        isGeneralization = parent.getMClass().getName() == "Generalization"
        if (isGeneralization):
            extends += ", " + parent.getSuperType().getName()
    if (len(extends) > 0):
        ret += indentPrint(" extends "+ extends.strip(" ,"), indent)
    if (len(implements) > 0):
        ret += indentPrint(" implements " + implements.strip(" ,"), indent)
    return ret
        
def printClass(clazz, indent):
    ret = ""
    ret += indentPrint("class " + clazz.getName() + "", indent)
    ret += printClassRealizations(clazz, indent + "")
    ret += indentPrint("\n{\n\n", indent)
    for a in clazz.getCompositionChildren():
        isOperation = a.getMClass().getName() == "Operation"
        if (isOperation):
            ret += printOperation(a,False, indent + "    ")
    ret += indentPrint("}\n", indent)
    return ret

if (selectedElements.size() > 0):
   
    exportPath = "C:/test/"
    
    for c in selectedElements:
        
        fileName = c.getName() + ".php"
        
        with open(exportPath + fileName, "w") as file:     
            ret = ""
            isInterface = c.getMClass().getName() == "Interface"
            owner = c.getOwner()
            isInPackage = owner.getMClass().getName() == "Package"
            ret += "<?php\n\n"
            if (isInPackage):
                ret += "namespace " + owner.getName() + ";\n\n"
            if (isInterface):
                ret += printInterface(c,"")
            else:
                ret += printClass(c,"")
            file.write(ret)
else:
    print "No element has been selected."
    
