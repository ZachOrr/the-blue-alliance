import os


@property
def is_debug() -> bool:
    return not os.getenv('GAE_ENV', None) == 'standard'
