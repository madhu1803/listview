from flask import Flask, render_template,request,flash
from datetime import datetime
import forms
import mysql.connector
from mysql.connector.errors import ProgrammingError
import json
from datetime import date

app = Flask(__name__)
import copy

mydb = mysql.connector.connect(
    host="localhost", database="madhu_db1", user="root",
)
mycursor = mydb.cursor(buffered=True)


@app.route("/", methods=["GET", "POST"])
def form():
   # define init forms | for fields
    form1 = forms.Form1Form()
    form2 = forms.Form2Form()
    form3 = forms.Form3Form()
    #copy dict
    form1_data = copy.deepcopy(form1.data)
    form2_data = copy.deepcopy(form2.data)
    form3_data = copy.deepcopy(form3.data)
    #del csrf token
    form1_data.pop('csrf_token')
    form2_data.pop('csrf_token')
    form3_data.pop('csrf_token')
    
    records = []
    date=None

    if request.method == 'POST':
        
        if 'searchsubmit' in request.form:
            date = request.form['selected_date']
       
        
    # select query for 3 three forms
        try:
            mycursor.execute(f"SELECT {', '.join(form1_data.keys())} FROM form1 where date='{date}'")
            raw_data1 = mycursor.fetchall()
            print(raw_data1)

            mycursor.execute(f"SELECT {', '.join(form2_data.keys())} FROM form2 where date='{date}'")
            raw_data2 = mycursor.fetchall()
            print(raw_data2)

            mycursor.execute(f"SELECT {', '.join(form3_data.keys())} FROM form3 where date='{date}'")
            raw_data3 = mycursor.fetchall()
            print(raw_data3)
    
        except:
            # override it by creating empty list
            raw_data1 = []
            raw_data2 = []
            raw_data3 = []
            
        if len(raw_data1) == 0:
            flash("data not found")
        else:
            # form1
            values1 = raw_data1[0]
            names1 = [name for name in form1_data.keys()]
            data_form1 = {}
            for index in range(len(values1)):
                data_form1[names1[index]] = values1[index]
            form1 = forms.Form1Form(data=data_form1)

            # form2
            values2 = raw_data2[0]
            names2 = [name for name in form2_data.keys()]
            data_form2 = {}
            for index in range(len(values2)):
                data_form2[names2[index]] = values2[index]
            form2 = forms.Form2Form(data=data_form2)

            # form3
            values3 = raw_data3[0]
            names3 = [name for name in form3_data.keys()]
            data_form3 = {}
            for index in range(len(values3)):
                data_form3[names3[index]] = values3[index]
            form3 = forms.Form3Form(data=data_form3)

   
    
    return render_template(
        "form.html", form1=form1, form2=form2, form3=form3, records=records,date=date
    )


if __name__ == "__main__":
    app.secret_key = "secret"
    app.run(debug=True)
