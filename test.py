def add_to_list(lst, frame, content):
    length = len(lst)
    if frame >= length:
        lst += [None for x in range(frame - length)] + [content]
    else:
        lst[frame] = content
    return lst
