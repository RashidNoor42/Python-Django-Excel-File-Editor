from django.http import HttpResponse
from django.shortcuts import render
import openpyxl
import csv

#file upload
def index(request):
    if "GET" == request.method:
        return render(request, 'index.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        sheet = request.POST.get("sheet")

        outputColArray = []
        rowNumber = 0
        rowNo = 0

        if sheet != '':
            
            try:
                wb = openpyxl.load_workbook(excel_file)

                # getting a particular sheet by name out of many sheets
                # worksheet = wb["TrainData"]
                worksheet = wb[sheet]
                # print(worksheet)

                excel_data = list()
                # iterating over the rows and
                # getting value from each cell in row
                for row in worksheet.iter_rows():
                    row_data = list()
                    colNumber = 0
                    rowNumber = rowNumber + 1

                    for cell in row:
                        colNumber = colNumber + 1
                        row_data.append(str(cell.value))

                        if "Output" in str(cell.value):
                            outputColArray.append(colNumber)
                            rowNo = rowNumber + 1
                            # print(rowNo)
                            # print(outputColArray)

                    excel_data.append(row_data)

                    # save data to session
                    request.session['allData'] = excel_data
                    request.session['colArr'] = outputColArray
                    request.session['row'] = rowNo

                return render(request, 'index.html', {"data":excel_data, "outputColumns": outputColArray, "outputRow": rowNo, })
            
            except Exception as e:
                print(e)
                return render(request, 'index.html', {"error":"Error Please Enter Valid Sheet Name"})
        
        else:
            return render(request, 'index.html', {"error":"Error. Please Enter Sheet Name"})


# export data into csv
def printExcel(request):

    if "POST" == request.method:

        data = request.session['allData']
        colArr = request.session['colArr']
        rowNo = request.session['row']

        # print(data, colArr, row)

        # print to csv
        response = HttpResponse(content_type="text/csv")
        writer = csv.writer(response)

        rowCount = 0

        for row in data:
            arr = []
            rowCount = rowCount + 1
            colCount = 0

            for col in row:
                colCount = colCount + 1
                colValue = col
                # print(colCount, rowCount)

                for colItem in colArr:
                    if(colItem == colCount and rowCount >= rowNo):
                        inputFieldName = str(colCount)+"-"+str(rowCount)
                        colValue = request.POST.get(inputFieldName)

                if(colValue != 'None'):
                    arr.append(colValue)
                else:
                    arr.append(" ")

            writer.writerow(arr)
            # print(arr)

        response['Content-Disposition'] = 'attachment; filename="modifiedData.csv"'
        return response
        # return render(request, 'finalData.html', {"data":data,} )
    