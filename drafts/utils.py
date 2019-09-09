# starting to test and use typed_dmms

def set_dict(dict, key_path, value):
    """ set_dict(dict, [key_0, ..., key_n], value) is 
        a correct implementation of
        
        dict[key_0]...[key_n] = value
    """
    len_key_path = len(key_path)
    dict_ptr = dict
    assert (len_key_path >= 1) 
    assert (type(dict) == type({}))    
    for i in range(len_key_path - 1):
        key = key_path[i]        
        if key not in dict_ptr:
            dict_ptr[key] = {}
        dict_ptr = dict_ptr[key]
        assert (type(dict_ptr) == type({}))
    dict_ptr[key_path[len_key_path - 1]] = value
            
