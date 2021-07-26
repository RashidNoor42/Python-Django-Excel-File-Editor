from django import template

register = template.Library()

@register.simple_tag
def checkRowsAndColumns(outputColumns, outputRow, colID, rowID):
    res = 0
    for column in outputColumns:
        if column == colID and rowID >= outputRow :
            res = 1

    return res
