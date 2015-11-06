import sys
def p_decorator(func):
    def func_wrapper(name):
        print '1',func_wrapper
        return "<p>{0}</p>".format(func(name))
    return func_wrapper

@p_decorator
def get_text(name):
    print '2'
    return "2 ten toi la %s"%name
print get_text
get_text = p_decorator(get_text)
print 'get_text after',get_text
def a():
    print 'adf'
print sys.getsizeof(a)
'''

def get_text(name):
    print '2'
    return "2 ten toi la %s"%name
print get_text
get_text = p_decorator(get_text)
print 'get_text after',get_text


print get_text("tu")
'''