import setuptools

VERSION = '1.1.0'
DESCRIPTION = 'A python package for handling keyboard and mouse inputs'
LONG_DESCRIPTION = """
pymousekey is made for halding keyboard and mouse inputs simular to how pyautogui does but instead using ctypes for almost everything.

Keep in mind their is no failsafe wrapper for any function so use with caution.

No extra dependencies are needed on windows to use this package
"""

setuptools.setup(
    name="PyMouseKey",
    version=VERSION,
    author="Chasss",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
)
