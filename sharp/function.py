class Function(object):
    """Data-class to hold meta information about a registered back-end function.
    """

    def __init__(self, rule, f):
        self.rule = rule
        self.f = f
