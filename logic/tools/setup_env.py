global SCRIPT_BASE_DIR
try:
    SCRIPT_BASE_DIR
except:
    import os
    import sys

    SCRIPT_BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    SCRIPT_BASE_DIR = os.path.dirname(SCRIPT_BASE_DIR)
    SCRIPT_BASE_DIR = os.path.dirname(SCRIPT_BASE_DIR)

    sys.path.append(SCRIPT_BASE_DIR)