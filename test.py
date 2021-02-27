# a test file so that i won't have to constantly re run bots

def print_json(json, indent=0):
    if type(json) != dict:
        print_json(serialize(json))
    for i, key, value in zip(range(len(json)), json.keys(), json.values()):
        if type(value) != dict:
            if i != len(json) - 1:
                print(f"{' ' * indent}{key}: {value},")
            else:
                print(f"{' ' * indent}{key}: {value}")
        else:
            print(f"{' ' * indent}{key}: {'{'}")
            print_json(value, indent + 4)
            print(f"{' ' * indent}{'}'}")
    return


def serialize(root):
    value_dict = {}
    skip = [type(None), int, float, str, list, tuple, dict]
    for attr in dir(root):
        act_attr = getattr(root, attr)
        if (
                not hasattr(object, attr)
                and attr != "__weakref__"
                and attr[:2] != "__"
                and attr[-2:] != "__"
        ):
            value_dict[attr] = act_attr if type(act_attr) in skip else serialize(act_attr)
    return value_dict
