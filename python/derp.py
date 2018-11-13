# derp


def main():
    print("derp")


def derp(term):
    """this does something

    Returns:
        [str] -- [a dumb string]
    """
    if term == "poop":
        return "gross"
    elif term == "hotdog":
        return "yum"
    else:
        return None


def add_two(a, b):
    """adds two numbers

    Arguments:
        a {int} -- num one
        b {int} -- num two

    Returns:
        [int] -- [number added]
    """
    if not a or not b:
        return None
    return a + b


if __name__ == "__main__":
    main()
