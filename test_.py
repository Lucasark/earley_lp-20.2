import pytest
import driver
import earley


def test_():
    test = [{"root" : "S",
            "children" : [{"root": "a"},
                          {"root" : "S",
                           "children" : [{"root": "a"}, {"root" : "b"}]},
                          {"root" : "b"}]}]
    
    earley.printDerivation(test)
    
    assert driver.initDriver("grm/anbn.grm", "aabb") == earley.printDerivation(test)
    
# def test_plus_norma():
#     test = [{"root" : "S",
#             "children" : [{"root": "a"},
#                           {"root" : "S",
#                            "children" : [{"root": "a"}, {"root" : "b"}]},
#                           {"root" : "b"}]}]
    
#     earley.printDerivation(test)
    
#     assert driver.initDriver("grm/anbn.grm", "aabb") == earley.printDerivation(test)

def test_plus_amb():
    test = [
        {'children': [{'children': [{'children': [{'root': 'a'}], 'root': 'S'}, 
                                    {'root': '+'}, 
                                    {'children': [{'root': 'a'}], 'root': 'S'}], 
                       'root': 'S'}, 
                      {'root': '+'}, 
                      {'children': [{'root': 'a'}], 'root': 'S'}], 
         'root': 'S'},
        {'children': [{'children': [{'root': 'a'}], 'root': 'S'}, 
                      {'root': '+'}, 
                      {'children': [{'children': [{'root': 'a'}], 'root': 'S'}, 
                                    {'root': '+'}, 
                                    {'children': [{'root': 'a'}], 
                                     'root': 'S'}], 
                       'root': 'S'}], 
         'root': 'S'}
    ]
    
    earley.printDerivation(test)
    
    assert driver.initDriver("grm/plus.grm", "a+a+a") == earley.printDerivation(test)
    
def test_bad():
    # print("<---MAU FORMADA--->")
    test = [
        {'children': [{'root': 'a'}, 
                      {'children': [{'root': 'a'}, {'root': 'b'}], 
                       'root': 'S'}], 
         'root': 'S'}
    ]
    
    earley.printDerivation(test)
    
    assert driver.initDriver("grm/anbn.grm", "aab") == earley.printDerivation(test)