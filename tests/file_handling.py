import main

def CreateFolderIfNotExists():
    """
    """
    path = "~/Downloads/Text"
    assert main.create_folder(path), "Should be True"

def GetFileName():
    """
    """
    path = "~/Downloads/test.txt"
    assert main.get_file_name(path) is not None, "Should not be None"