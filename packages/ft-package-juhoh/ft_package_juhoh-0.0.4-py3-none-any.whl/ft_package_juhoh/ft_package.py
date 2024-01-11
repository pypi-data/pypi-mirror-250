def count_in_list(lst: range, key: any):
    if key is None:
        return 0

    count = 0
    for i in lst:
        if i == key:
            count += 1
    return count
