class Arg(object):
    def __init__(self, master, arg, kwargs):
        self.master = master
        self.arg = arg
        self.kwargs = kwargs

        if not hasattr(self.master, "_" + arg):

            def prop(value=None):
                if value:
                    setattr(self.master, "_" + arg, value)
                else:
                    return getattr(self.master, "_" + arg)

            setattr(self.master, "_" + arg, kwargs[arg])
            setattr(self.master, arg, prop)
            setattr(self.master, "attr_" + arg, prop)


class AdwBase():
    def attr(self, **kwargs):
        """
        初始或设置多个属性
        """
        if kwargs:
            for arg in kwargs:
                setattr(self, "_arg_" + arg, Arg(self, arg, kwargs))

            self.update()
        else:
            return getattr(self, name)
