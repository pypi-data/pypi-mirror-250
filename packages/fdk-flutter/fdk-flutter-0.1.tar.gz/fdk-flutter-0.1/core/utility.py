import re

def is_valid_project_name(s):
    pattern = r'^[a-z_]+$'
    if re.match(pattern, s):
        return True
    else:
        return False