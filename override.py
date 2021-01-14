from exceptions import OverrideError


# just so i won't run into problems, the method must be called like this:
# @override([the class where the function to override is])
# def foo(*args, **kwargs):..

def override(interface_class):
    # assert im overriding an existing method
    def overrider(method):
        if method.__name__ in dir(interface_class):
            return method
        else:
            raise OverrideError(method.__name__, interface_class.__name__)

    return overrider
