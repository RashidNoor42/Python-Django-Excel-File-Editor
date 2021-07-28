from django import template

register = template.Library()

@register.simple_tag
def checkRowsAndColumns(outputColumns, outputRow, colID, rowID):
    res = 0
    for column in outputColumns:
        if column == colID and rowID >= outputRow :
            res = 1

    return res

#Convert array into string
# @register.simple_tag
# def convertArrayToString(arr):
    
#     string_version = "".join([str(i) for x in arr for i in x ])
#     print("arr:", string_version)

#     return string_version
