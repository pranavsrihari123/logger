from flask import Flask, render_template, request, send_file
import datetime
import pandas as pd
import math

app = Flask(__name__)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8002)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    return render_template('logger.html')

@app.route("/data", methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        file_1 = request.files['logger_data']
        output_data = pd.read_csv(file_1, encoding = "ISO-8859-1", names=['first', 'second'], keep_default_na=False).to_dict()
        serials = []
        dfs = []
        sensor_id = []
        curr_ser = ''
        n=0
        started = False
        for n in range(len(output_data['first'])):
            i = output_data['first']
            j = output_data['second']
            if i[n]=='Logger serial number:':
                serial_no = j[n]
                s = serial_no[len(serial_no)-5: len(serial_no)-2]
                sensor_id.append(s)
                curr_ser = s
                d = {'Date/Time': [], s: []}
                serials.append(d)
                started = True
            if i[n]=='Log data: date/time':
                n+=1
                while (n<len(i) and i[n]):
                    curr_datetime = i[n]
                    if curr_datetime[0]!='2': 
                        break
                    serials[len(serials)-1][curr_ser].append(j[n])
                    serials[len(serials)-1]['Date/Time'].append(curr_datetime)
                    #curr_datetime = increment_time(curr_datetime)
                    n+=1
        
        for s in serials:
            dfs.append(pd.DataFrame(data=s))


        with pd.ExcelWriter('output.xlsx') as writer:
            for t in range(len(dfs)):
                s = sensor_id[t]
                dfs[t].to_excel(writer, sheet_name=s, index=False)


        return send_file('output.xlsx', as_attachment=True)


#def increment_time(s):
#    format_string = "%Y/%m/%d %H:%M:%S"
#    date_object = datetime.datetime.strptime(s, format_string)
#    delta1 = datetime.timedelta(minutes=1)
#    date_object += delta1
#    return date_object.strftime(format_string)



    
