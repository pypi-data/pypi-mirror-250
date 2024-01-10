"""Init file of GitAddNB package
"""
try:
    from gitaddnb._version import __version__  # type:ignore
except ImportError:
    try:
        from setuptools_scm import get_version  # type:ignore

        __version__ = get_version()
    except (ImportError, LookupError) as e:
        __version__ = str(e)
