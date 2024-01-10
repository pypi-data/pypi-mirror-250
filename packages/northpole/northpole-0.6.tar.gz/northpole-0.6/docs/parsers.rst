Parsers
=======

The parsers module contains a collection of methods that can be used for parsing
input data for the challenges.

.. function:: string_parser(input_data: str)

    Take the input data as a string, and return the string after having stripped
    any whitespace from the end.

    :param input_data: The input data for the challenge.
    :type data: str

    :return: The data string trimmed of following whitespace.
    :rtype: str

    Example 1::

        data: str = string_parser("Santa")

        # Result: "Santa"
    
    Example 2::

        data: str = string_parser("Elves\n")

        # Result: "Elves"
