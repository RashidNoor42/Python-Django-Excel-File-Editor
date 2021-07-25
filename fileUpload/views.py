from django.shortcuts import render
from django.http import HttpResponse
import openpyxl

# Create your views here.
# def index(request):
#     return render(request, 'index.html')

#file upload
def index(request):
    if "GET" == request.method:
        return render(request, 'index.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        sheet = request.POST.get("sheet")

        outputColArray = []

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

                    for cell in row:
                        colNumber = colNumber + 1
                        row_data.append(str(cell.value))

                        if "Output" in str(cell.value):
                            outputColArray.append(colNumber)
                            # print(colNumber)

                    excel_data.append(row_data)

                # print(excel_data)

                return render(request, 'index.html', {"data":excel_data, "outputColumns": outputColArray,})
            
            except Exception as e:
                print(e)
                return render(request, 'index.html', {"error":"Error Please Enter Valid Sheet Name"})
        
        else:
            return render(request, 'index.html', {"error":"Error. Please Enter Sheet Name"})

