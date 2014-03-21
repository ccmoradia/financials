# General utilities


def charges(basic = 1, *args, **kwargs):
    """
    Calculate charges based on the given structure
    
    args: Cost structure in the given format
    
    kwargs:
    
    percent: Boolean/default True
        If False, numbers aren't converted to percentages
    
    
    Format
    ======
    Cost 
    Case insensitive
    
    Lets start with a straight forward case
    >>> charges(100, ['tax', 'basic', 10])
    110.0
    
    >>> charges(100, ['tax1', 'basic', 10], ['tax2', 'basic', 15])
    125.0
    
    If you want to subtract something, precede it with a negative sign
    >>> charges(100, ['discount', 'basic', -15])
    85.0
    
    For charges to accumulate all previous values,
    use acc as the second argument
    
    >>> charges(100, ['tax1', 'basic', 10], ['tax2', 'acc', 15])
    126.5
    
    charges is case insensitive as all keys are converted to lower case
    >>> charges(100, ['TAX', 'Basic', 10])
    110.0
    
    charges accumulates values if the first argument is repeated
    
    >>> charges(100, ['tax', 'basic', 10], ['commission', 'basic', 20], ['tax', 'acc', 5])
    136.5
    """
    
    p = 0.01
    result = {}
    result['basic'] = basic    
    for (a,b,c) in args:
     
        if b == 'acc':
            if result.get(a.lower()):
                result[a.lower()] = result[a.lower()] + sum(result.values()) * c * p
            else:
                result[a.lower()] = sum(result.values()) * c * p
        else:
            if result.get(a.lower()):
                result[a.lower()] = result[a.lower()] + result[b.lower()] * c * p
            else:
                result[a.lower()] = result[b.lower()] * c * p
    return sum(result.values())
    
  
print charges(100, ['tax', 'basic', 10])
            
    
