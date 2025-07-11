""" example for GitHub Actions with Sphinx """


def hello_world() -> str:
    """
    do the usual 'hello world'
    
    Adding more text

    :return: Hello World
    :rtype: String
    """
    return "hello world!! :) "


def greeter_msg(*, greeter: str) -> str:
    """
    Custom greeting\n
    JOSH KEMPPAINEN auto-doc test
    
    Moved requirements.txt to docs/ folder


    :param greeter: name of a person who message will be from
    :type greeter: str
    :return: a greeting from the greeter
    :rtype: str
    """
    return f"Hello to you from {greeter}"