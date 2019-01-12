from operator import methodcaller


def text_to_list(raw):
    """Transform a raw text list to a python sorted object list
    Supported separators: coma, space and carriage return
    """
    return sorted(
        list(
            set(
                id.strip()
                for r in map(methodcaller("split", ","), raw.split())
                for id in r
                if len(id)
            )
        )
    )
