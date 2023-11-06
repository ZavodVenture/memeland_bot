def convert_ranges_to_array(ranges):
    array = []
    ranges = ranges.split(",")
    ranges = [r.strip() for r in ranges]
    for r in ranges:
        if "-" in r:
            start, end = r.split("-")
            start = int(start)
            end = int(end)
            for i in range(start, end + 1):
                array.append(i)
        else:
            num = int(r)
            array.append(num)
    return list(set(array))
