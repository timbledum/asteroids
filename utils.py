

def check_bounds(position, limit, buffer):
    if position < 0 - buffer:
        return limit + buffer
    elif position > limit + buffer:
        return -buffer
    else:
        return position