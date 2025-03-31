from django import template
register = template.Library()

@register.simple_tag
def total_posts():
    return 'Prueba'


@register.filter
def indexing(indexable, i):
    print(indexable)
    print(i)
    try:
        indexable=eval(indexable)
    except:
        indexable=indexable
    if len(indexable)!=0:
        try:
            return indexable[i]
        except:
            return "[]"
    else:
        return "[]"

@register.filter
def naming(indexable,extra):
    try:
        indexable=indexable+extra
    except:
        indexable=indexable
    return indexable

@register.filter
def get_item(dictionary, key):
    dictionary=eval(dictionary)
    return dictionary.get(key)

@register.filter
def get_key(dictionary, indexable):
    dictionary=eval(dictionary)
    try:
        info=list(dictionary.keys())[int(indexable)]
    except:
        info=''
    return info


@register.filter
def get_index_value(list_, index):
    """
    Custom template tag to get the value at the specified index in a list.
    """
    if list_ and len(list_) > index:
        return list_[index]
    else:
        return None
    

@register.filter
def get_elements(dict_, index):
    """
    Custom template tag to get the value at the specified index in a list.
    """
    if dict_ and index in dict_:
        return dict_[index]
    else:
        return None  # or any other default value you prefer
