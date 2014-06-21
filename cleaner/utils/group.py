def group(n, list):
    """
        @param n
        @param list

        See http://stackoverflow.com/questions/2231663/slicing-a-list-into-a-list-of-sub-lists#answer-2231685
    """
    return [list[i:i+n] for i in range(0, len(list), n)]