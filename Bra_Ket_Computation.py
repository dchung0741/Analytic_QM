from ast import operator
from webbrowser import Opera
import numpy as np
from fractions import Fraction
import math
from sympy import Rational, sqrt, I
import sympy as sp
from functools import reduce
from copy import deepcopy


class Abstract_Vec:

    def __init__(self, Abstract_Type, Label_Coeff_List: list):

        # Label_Coeff_List = [ ( (label_1), coeff_1, [operators] ), ( (label_2), coeff_2 ), ( (label_3), coeff_3 ) ]
        self.Label_Coeff_List = Label_Coeff_List
        self.Label_Dict = {}
        
        for i in Label_Coeff_List:

            if i[1] != 0:
                #self.Label_Dict[ i[0] ] = Abstract_Type(i[0], i[1], i[2])
                if str(Abstract_Type(i[0], 1, i[2])) in self.Label_Dict:
                    #self.Label_Dict[ str(Abstract_Type(i[0], 1, i[2])) ] += Abstract_Type(i[0], i[1], i[2])
                    tmp_coeff = self.Label_Dict[ str(Abstract_Type(i[0], 1, i[2])) ].coeff + Abstract_Type(i[0], i[1], i[2]).coeff
                    if tmp_coeff != 0:
                        self.Label_Dict[ str(Abstract_Type(i[0], 1, i[2])) ].coeff = tmp_coeff
                    else:
                        del self.Label_Dict[ str(Abstract_Type(i[0], 1, i[2])) ]


                else:
                    self.Label_Dict[ str(Abstract_Type(i[0], 1, i[2])) ] = Abstract_Type(i[0], i[1], i[2])


    ######################################################################
    #  Basic Algebra
    ######################################################################
    def __add__(self, Other):

        if type(Other) == type(self):
            
            label_set_1 = set(self.Label_Dict)
            label_set_2 = set(Other.Label_Dict)


            New_Ket_Label_set = label_set_1.union(label_set_2)
            New_Label_Coeff_List = []

            for el in New_Ket_Label_set:

                if el in label_set_1 and el in label_set_2:
                    new_coeff = self.Label_Dict[el].coeff + Other.Label_Dict[el].coeff
                    
                    if new_coeff != 0:
                        New_Label_Coeff_List.append( [ self.Label_Dict[el].label, new_coeff, self.Label_Dict[el].operators ] )
                    
                
                elif el in label_set_1 and (el in label_set_2) is False:
                    new_coeff = self.Label_Dict[el].coeff

                    if new_coeff != 0:
                        New_Label_Coeff_List.append( [ self.Label_Dict[el].label, new_coeff, self.Label_Dict[el].operators ] )
                    

                elif el in label_set_2 and (el in label_set_1) is False:
                    new_coeff = Other.Label_Dict[el].coeff

                    if new_coeff != 0:
                        New_Label_Coeff_List.append( [ Other.Label_Dict[el].label, new_coeff, Other.Label_Dict[el].operators ] )
                
        
            return type(self)(New_Label_Coeff_List)
        
        
        else:
            raise Exception(f'{type(self)} can only be added to {type(self)}.')


    def __neg__(self):

        neg_coeff_list = list(map( lambda x: type(x)([x[0], - x[1], x[2]]), self.Label_Coeff_List ))
        return type(self)(neg_coeff_list)
    
    def __sub__(self, Other):

        return self + (-Other)
    
    def __mul__(self, X):
        mul_coeff_list = list(map( lambda x: type(x)([x[0], X * x[1], x[2]]), self.Label_Coeff_List ))
        return type(self)(mul_coeff_list)

    def __rmul__(self, X):
        return self * X
    
    def __truediv__(self, X):
        div_coeff_list = list(map( lambda x: type(x)([x[0], x[1]/ X, x[2]]), self.Label_Coeff_List ))
        return type(self)(div_coeff_list)
    
    def __rmatmul__(self, operator):
        op_list = list(map( lambda x: type(x)([x[0], x[1], [operator] + x[2]]), self.Label_Coeff_List ))
        return type(self)(op_list)


    ######################################################################
    #  Representation
    ######################################################################
    def __str__(self):
        return str( list(self.Label_Dict.values()) )
    
    def __repr__(self):
        return self.__str__()



##########################################################################################################################################################################
class Single_Op:

    def __init__(self, name) -> None:
        
        self.op_name = name
    
    def __matmul__(self, other):

        if type(other) is Operators:

            return 
    
    def __str__(self) -> str:
        return self.op_name
    
    def __repr__(self) -> str:
        return self.__str__()


class Operators:

    def __init__(self, operator_sequence) -> None:
        
        self.op_seq = operator_sequence
    


"""
class Operators:
    
    def __init__(self, names):
        
        self.op_name = []

        for name in names:
            self.op_name.append(name)

    
    def __matmul__(self, other):

        if type(other) is Operators:
            
            new_op_list = self.op_name + other.op_name
            
            return Operators(new_op_list)
        
        elif isinstance(other, Ket):
            return other.__rmatmul__(self)

    ######################################################################
    #  Representation
    ######################################################################
    def __str__(self):

        return ' @ '.join(map(str, self.op_name)) 

    def __repr__(self) -> str:
        return self.__str__()
    
"""

##########################################################################################################################################################################
class Single_Ket:

    def __init__(self, label: tuple, coeff, operator = []):

        self.label = label
        self.coeff = coeff
        self.operators = operator
        self.operators_flat = [] if self.operators == [] else reduce(lambda x, y: x + y, list(map( lambda x: x.op_name, self.operators )))
        
    
    ######################################################################
    #  Representation
    ######################################################################    
    def __str__(self):
        
        if self.operators == []:

            if self.coeff == 1:

                if type(self.label) is tuple:
                    #return '| ' + ', '.join(map(str, self.label)) + ' >'
                    return '| {} >'.format(', '.join(map(str, self.label)))
                
                else:
                    return f'|{self.label}>'
            
            else:

                if type(self.label) is tuple:
                    return '{} * | {} >'.format(self.coeff, ', '.join(map(str, self.label)))
                
                else:
                    return f'{self.coeff} * |{self.label}>'
        
        else:
            
            
            Operator_Str = ' @ '.join(map(str, self.operators))
            

            if self.coeff == 1:

                if type(self.label) is tuple:
                    
                    return '{} @ | {} >'.format(Operator_Str, ', '.join(map(str, self.label)))
                
                else:
                    return f'{Operator_Str}.|{self.label}>'
            
            else:

                if type(self.label) is tuple:
                    
                    return '{} * {} @ | {} >'.format(self.coeff, Operator_Str, ', '.join(map(str, self.label)))
                
                else:
                    return f'{self.coeff} * {Operator_Str}.|{self.label}>'


    
    def __repr__(self):
        return self.__str__()

##########################################################################################################################################################################

class Ket(Abstract_Vec):

    def __init__(self, Label_Coeff_List):

        super().__init__(Single_Ket, Label_Coeff_List)




##########################################################################################################################################################################
if __name__ == '__main__':

    Jx = Operators(['Jx'])
    Jy = Operators(['Jy'])
    Jz = Operators(['Jz'])
    Jp = Operators(['Jp'])
    Jm = Operators(['Jm'])
    J2 = Operators(['J2'])

    ket_1 = Ket([ [(1, 1), 1, [Jp @ Jm]], [(1, 0), 3, [Jz]] ])
    ket_2 = Ket([ [(1, 0), -1, []], [(1, 1), -1, []] ])
    ket_3 = Ket([ [(1, 1), 87, [Jz]] ])

    print(ket_1)
