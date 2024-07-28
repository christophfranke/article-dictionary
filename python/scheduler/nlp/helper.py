def highlight_first_difference(str1, str2, context_range=5):
    min_len = min(len(str1), len(str2))
    index = None

    for i in range(min_len):
        if str1[i] != str2[i]:
            index = i
            break

    if index is None:
        if len(str1) != len(str2):
            index = min_len
            str1_diff = '' if len(str1) <= min_len else str1[min_len:]
            str2_diff = '' if len(str2) <= min_len else str2[min_len:]
            print(f"Strings differ in length at index {index}.")
            print(f"String 1 extra part: {str1_diff}")
            print(f"String 2 extra part: {str2_diff}")
        else:
            print("Strings are identical.")
        return

    start = max(index - context_range, 0)
    end = min(index + context_range + 1, max(len(str1), len(str2)))

    context_str1 = str1[start:end]
    context_str2 = str2[start:end]

    print(f"First difference at index {index}:")
    print(f"String 1: {context_str1}")
    print(f"String 2: {context_str2}")
    print(f"Character difference: '{str1[index]}' != '{str2[index]}'")
