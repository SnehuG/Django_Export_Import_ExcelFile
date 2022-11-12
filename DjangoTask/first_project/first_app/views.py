from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse
import openpyxl
from first_app.models import FileContent
from io import BytesIO
import pandas as pd
from django.db.models import Q, Sum

# Create your views here.
def file_upload(request):
    #import data from excel
    if request.method=="POST":
        FileContent.objects.all().delete()
        excel_file=request.FILES['ufile']
        wb = openpyxl.load_workbook(excel_file)
        #getting a particular sheet name out of many sheets
        excel_worksheet = wb['Input']
        excel_data=list()
        for r in excel_worksheet.iter_rows():
            row_data = list()
            for c in r:
                row_data.append(str(c.value))
            excel_data.append(row_data)

        #insert data into table
        for x in excel_data[1:-1]:
            f1=FileContent(Category=x[0],X=x[1],Y=x[2])
            f1.save()
        return redirect('/export')
    else:
        return render(request,'index.html')

#Export Database data to excel
def exportfile(request):
    if request.method=="GET":
        q1=Q(Category='A')
        q2=Q(Category='B')
        q3=Q(Category='C')
        TotalAX=FileContent.objects.filter(q1).aggregate(TotalX=Sum('X'))
        TotalAY=FileContent.objects.filter(q1).aggregate(TotalY=Sum('Y'))

        TotalBX=FileContent.objects.filter(q2).aggregate(TotalX=Sum('X'))
        TotalBY=FileContent.objects.filter(q2).aggregate(TotalY=Sum('Y'))

        TotalCX=FileContent.objects.filter(q3).aggregate(TotalX=Sum('X'))
        TotalCY=FileContent.objects.filter(q3).aggregate(TotalY=Sum('Y'))

        rowsA=list(FileContent.objects.filter(q1).values('Category','X','Y'))
        dfA = pd.DataFrame(rowsA)
        dfA.loc[-1] = ['Total',TotalAX['TotalX'],TotalAY['TotalY']]

        rowsB=list(FileContent.objects.filter(q2).values('Category','X','Y'))
        dfB = pd.DataFrame(rowsB)
        dfB.loc[-1] = ['Total',TotalBX['TotalX'],TotalBY['TotalY']]

        rowsC=list(FileContent.objects.filter(q3).values('Category','X','Y'))
        dfC = pd.DataFrame(rowsC)
        dfC.loc[-1] = ['Total',TotalCX['TotalX'],TotalCY['TotalY']]

        filename = "Output.xlsx"
        with BytesIO() as b:
            writer=pd.ExcelWriter(b,engine='xlsxwriter')
            dfA.to_excel(writer, sheet_name="Output",index=False,startrow=0)
            dfB.to_excel(writer, sheet_name="Output",index=False,startrow=0+len(dfA)+3)
            dfC.to_excel(writer, sheet_name="Output",index=False,startrow=0+len(dfA)+3+len(dfB)+3)
            writer.save()
            response = HttpResponse(
                b.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            return response