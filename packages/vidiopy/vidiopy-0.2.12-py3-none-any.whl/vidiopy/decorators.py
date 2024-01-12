import decorator

@decorator.decorator
def requires_duration(f, clip, *a, **k):
    """ Raise an error if the clip has no duration."""
    
    if clip.duration is None:
        raise ValueError("Attribute 'duration' not set")
    else:
        return f(clip, *a, **k)

# Make Decorator requires_size 
@decorator.decorator
def requires_size(f, clip, *a, **k):
    """Raise an error if the clip has no size."""
    if clip.size is None:
        raise ValueError("Attribute 'size' not set")
    else:
        return f(clip, *a, **k)

@decorator.decorator 
def requires_fps(f, clip, *a, **k): 
    """ Raise an error if the clip has no duration""" 
    if clip.fps == None or 0: 
        raise ValueError("Attribute 'fps' not set") 
    else: 
        return f(clip, *a, *k)

@decorator.decorator 
def requires_start(f, clip, *a, **k): 
    """ Raise an error if the clip has no start.""" 
    if clip.start is None: 
        raise ValueError("Attribute 'start' not set") 
    else: 
        return f(clip, *a, **k)

@decorator.decorator 
def requires_end(f, clip, *a, **k): 
    """ Raise an error if the clip has no end.""" 
    if clip.end is None: 
        raise ValueError(f"Attribute 'end' not set end={clip.end}") 
    else: 
        return f(clip, *a, **k)

@decorator.decorator 
def requires_start_end(f, clip, *a, **k): 
    """ Raise an error if the clip has no start or end.""" 
    if clip.start is None and clip.end is None: 
        raise ValueError("Attribute 'start' or 'end' not set") 
    else: 
        return f(clip, *a, **k)


