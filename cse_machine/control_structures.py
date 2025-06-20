import pprint
from typing import Iterator, List

from .symbol import *
from .st import STNode
# from logger import logger

class ControlStruct(Iterable):
    """
    Represents a control structure in the CSE machine.

    Implemented as a List[Symbol]
    """
    
    def __init__(self, index):

        self.__index = index
        self.__array: List[Symbol] = []

    def getIndex(self):
        """Returns the index of the control structure."""
        return self.__index
    
    def __iter__(self) -> Iterator:
        """Returns an iterator for the control structure.
        
        Example:
            for symbol in controlStruct:
                print(symbol)

        This similar to accessing the array attribute in this class.
        """
        return iter(self.__array)

    def addSymbol(self, symbol: Symbol):
        """Appends a symbol to the control structure"""
        self.__array.append(symbol)

    def __repr__(self):
        return f"delta-{self.__index} = {self.__array}"
    

class ControlStructures:
    """
    A class which represents the control structures as an object.
    
    Attributes: 
        control_structure_map (dict): A dictionary of control structures.
        
    """
    
    def __init__(self, control_structure_map: dict):
        self.__control_structure_map = control_structure_map

    def get(self, delta_index) -> ControlStruct:   
        """Returns the control structure for the given delta index."""
        
        return self.__control_structure_map[delta_index]

    def __repr__(self):
        return pprint.pformat(self.__control_structure_map)


class CSInitializer:

    def __init__(self, st:STNode) -> None:
        self.__st = st
        self.__controlStructureMap = None
        
    def init(self) -> ControlStructures:
        """
        Generates the control structures for the CSE machine from the Standardized Tree.
        
        Returns: 
            ControlStructures object containing the control structures.
        """
        self.__initializeCS(self.__st)
        return ControlStructures(self.__controlStructureMap)
    
    def __get(self, delta_index) -> ControlStruct:
        return self.__controlStructureMap[delta_index]

    def __initializeCS(self, st) -> dict:
        """
        Generates the control structures for the CSE machine from the Standardized Tree.
        
        Args: st (STNode): The Standardized Tree.
        
        Returns: 
            A dictionary of control structures.
        """
        
        def traverse(node: STNode, deltaIndex: int):
            """
            Traverses the tree using pre-order traversal.
            
            Args:
                node (STNode): The node to traverse.
                deltaIndex (int): The index of the control structure.

            """

            if node is None:
                return
            visit(node, deltaIndex)
            # if node is lambda dont traverse left instead traverse right of left
            traverse(node.getLeft(), deltaIndex)
            traverse(node.getRight(), deltaIndex)

        def visit(node:STNode, deltaIndex: int):
            """
            Visit the node and add the symbol to the control structure.
            """
            currentCS:ControlStruct = self.__get(deltaIndex)
            symbol = None
            if node.is_lambda():
                handleLambda(node, deltaIndex, currentCS)
            elif node.is_conditional():
                # add beta to the control structure
                handleConditional(node, deltaIndex, currentCS)
            elif node.is_tau():
                handleTau(node, deltaIndex, currentCS)
            else:
                # add to current CS 
                symbol = SymbolFactory.createSymbol(node)
                currentCS.addSymbol(symbol)
            

        def handleLambda(node, deltaIndex, currentCS):
            deltaIndex = self.__addNewControlStruct(deltaIndex)
                # add x to the control structure
            x:STNode = node.getLeft()
            x_value = x.parseValueInToken()
            if x_value != Nodes.COMMA:
                symbol = LambdaSymbol(deltaIndex, [x_value])
            else:
                values = valuesOfChildren(x)
                symbol = LambdaSymbol(deltaIndex, values)
            currentCS.addSymbol(symbol)
                # don't traverse left of lambda
            node.setLeft(None)
            traverse(x.getRight(), deltaIndex)
            return deltaIndex
        
        def valuesOfChildren(node:STNode):
            node = node.getLeft()
            values = []
            while node is not None:
                values.append(node.parseValueInToken())
                node = node.getRight()
            return values

        def handleConditional(node:STNode, deltaIndex:int, currentCS:ControlStruct):
            symbol = BetaSymbol()
            delta_then = self.__addNewControlStruct(deltaIndex)
            delta_else = self.__addNewControlStruct(delta_then)
            delta_then_symbol = DeltaSymbol(delta_then)
            delta_else_symbol = DeltaSymbol(delta_else)
            currentCS.addSymbol(delta_then_symbol)
            currentCS.addSymbol(delta_else_symbol)
            currentCS.addSymbol(symbol)
            boolean_exp:STNode = node.getLeft()
            # dont traverse left of node
            node.setLeft(None)
            then_exp:STNode = boolean_exp.getRight()
            boolean_exp.setRight(None)
            else_exp:STNode = then_exp.getRight() 
            then_exp.setRight(None)
            traverse(boolean_exp, deltaIndex)
            traverse(then_exp, delta_then)
            traverse(else_exp, delta_else)


        def handleTau(node:STNode, deltaIndex:int, currentCS:ControlStruct):
            n = node.getChildrenCount()
            symbol = TauSymbol(n)
            currentCS.addSymbol(symbol)
            return deltaIndex

        # Initialize the control structure map
        self.__controlStructureMap = {}   
        # create the control structure for delta 0
        deltaIndex = 0
        self.__addNewControlStruct(deltaIndex)

        # start the traversal from the root of the tree
        traverse(st, deltaIndex)
        return self.__controlStructureMap

    def __addNewControlStruct(self, deltaIndex: int):
        """Adds a new control structure to the Control Structure Map by linear probing"""
        
        while deltaIndex in self.__controlStructureMap.keys():
            deltaIndex+=1
        self.__controlStructureMap[deltaIndex] = ControlStruct(deltaIndex)
        return deltaIndex


