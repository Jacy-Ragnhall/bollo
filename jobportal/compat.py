"""Compatibility shims for upstream runtime changes."""

from django.template.context import BaseContext


def patch_template_context_copy():
    if getattr(BaseContext.__copy__, "_python314_compat_patch", False):
        return

    def _compat_copy(self):
        duplicate = object.__new__(type(self))
        duplicate.__dict__.update(self.__dict__)
        duplicate.dicts = self.dicts[:]
        return duplicate

    _compat_copy._python314_compat_patch = True
    BaseContext.__copy__ = _compat_copy


patch_template_context_copy()
