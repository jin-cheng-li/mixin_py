# -*- coding: utf-8 -*-
from inspect import getmembers, isfunction


def do_patch_moudle(cl, module):
    funlst = [o for o in getmembers(module) if isfunction(o[1])]
    for t in funlst:
        f_name = t[0]
        f = t[1]
        if f_name.startswith('__'):
            continue
        assert not hasattr(cl, f_name), "repeat function, module:%s, f_name:%s" % (module, f_name)
        setattr(cl, f_name, f)


def do_patch_cls(target_cl, cl):
    for f_name in cl.__dict__:
        if f_name.startswith('__'):
            continue
        obj = getattr(cl, f_name)
        if not callable(obj):
            continue
        assert not hasattr(target_cl, f_name), "repeat function, cl:%s, f_name:%s" % (cl, f_name)
        setattr(target_cl, f_name, obj.im_func)
