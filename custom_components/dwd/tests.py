# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 19:50:36 2024

@author: Bobby
"""
from dataclasses import dataclass
from operator import attrgetter


def x():
    return 0

print(x())

if (_power := -208 + 300) < 0:
    print(_power)



class TestDescriptor:
    """State descriptor class."""

    def __init__(self):
        """Initialize instance."""
        pass

    def __set_name__(self, owner, name) -> None:
        """Set the owner and name of the descriptor."""
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, obj, objtype=None):
        """Dunder method."""
        value = getattr(obj, self.private_name)
        print(self.test_value)
        return value
        
    def __set__(self, obj, value):
        """Dunder method."""
        setattr(obj, self.private_name, value)
        self.test_value = value


class Test:
    
    
    descriptor_1 = TestDescriptor()
    descriptor_2 = TestDescriptor()
    
    
    def __init__(self, val_1, val_2):
        self.descriptor_1 = val_1
        self.descriptor_2 = val_2


test = Test("descriptor_test_1", "descriptor_test_2")  
    
test.descriptor_1
test.descriptor_2