# BrainGenix-NES
# AGPLv3


def GetID(_Object):

    ID = None
    if (type(_Object) == str):
        ID = str(_Object)
    elif (type(_Object) == int):
        ID = str(_Object)
    else:
        ID = str(_Object.ID)

    return ID