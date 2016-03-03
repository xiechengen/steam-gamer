#!python3
"""
Correct ordinal number display
"""
def ordinal(number: int):
    """
    This function takes an integer number and returns a string that displays
    correct ordinal number. (number is greater than 0)
    For example:
    $ res = ordinal(10)
    $ (res, type(res))
    $ ('10th', <class 'str'>)
    """
    if type(number) != int:
        raise TypeError
    else:
        if 11 <= number <= 20 or number % 10 == 0:
            return str(number) + 'th'
        elif number % 10 == 1:
            return str(number) + 'st'
        elif number % 10 == 2:
            return str(number) + 'nd'
        elif number % 10 == 3:
            return str(number) + 'rd'
        else:
            return str(number) + 'th'

if __name__ == "__main__":
    for i in range(10005):
        ordinal(i)

