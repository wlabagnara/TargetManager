''' Example use case of doctest in Class '''


# Reference for testing a class with python's DOCTEST
class TestMe:
    """ TEST CASES - with deliberate error!
    >>> a = TestMe()
    >>> a.sum_me(1,2)
    3
    >>> a.sum_me(1,0)
    1
    >>> a.sum_me(1,-1)
    1
    """            
    def sum_me(self, in_a, in_b):
        out = in_a + in_b
        return out
    
import doctest # enable doctest
doctest.testmod()