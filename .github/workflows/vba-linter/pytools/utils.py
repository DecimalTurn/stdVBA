def replace_first_instance(input_string, search, replace):
    # Find the index of the first occurrence of the search substring
    index = input_string.find(search)

    # If the search substring is found
    if index != -1:
        # Create a new string by replacing the first instance
        new_string = input_string[:index] + replace + input_string[index + len(search):]
        return new_string

    # If the search substring is not found, return the original string
    return input_string

def replace_last_instance(input_string, search, replace):
    # Find the index of the last occurrence of the search substring
    index = input_string.rfind(search)

    # If the search substring is found
    if index != -1:
        # Create a new string by replacing the last instance
        new_string = input_string[:index] + replace + input_string[index + len(search):]
        return new_string

    # If the search substring is not found, return the original string
    return input_string