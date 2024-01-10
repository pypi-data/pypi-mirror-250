def string_parser(input_data: str) -> str:
    """
    Take the input data as a string, and return the string after having stripped
    any whitespace from the end.

    Args:
        input_data (str): The data to parse.

    Returns:
        str: The parsed data.
    """
    return input_data.splitlines()[0]
