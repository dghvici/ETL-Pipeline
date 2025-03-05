import re

def get_table_name(file_key):
    """function to extract the table name from the
    filenames"""
    try:
        if "ingested" in file_key:
            re_pattern = r"ingested-(\w+)"
        elif "transformed" in file_key:
            re_pattern = r"transformed-(\w+)"

        match = re.search(re_pattern, file_key)
        table_name = match.group(1)
        return table_name
    except UnboundLocalError as e:
        #needs something else adding
        return None