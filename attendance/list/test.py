import csv
import os
import pandas as pd
import numpy as np
from datetime import datetime

# dir = os.path.dirname(os.path.realpath(__file__))
# print(dir)
# exist = False
# df1 = pd.read_csv('C:/Users/aryar/Documents/GitHub/FaceDetection/Attendance/Attendance.csv')
# for i in range(len(df1['id'])):
#     if df1['id'].iloc[i] == 8:
#         exist = True
# if not exist:
#     arr = [8,'Ankit']
#     arr = np.concatenate((arr,[0]*(len(df1.columns)-2)))
#     print(arr)
#     df1.loc[len(df1.index)] = arr
#     print(df1)
    #df1.to_csv('C:/Users/aryar/Documents/GitHub/FaceDetection/Attendance/Attendance.csv', index=False)

# os.startfile(dir + '/students.csv')
# now = datetime.now()
# date_time = now.strftime("%d/%m/%Y %H:%M:%S")
# date = now.strftime("%d/%m/%Y")
# dataset_path = path = os.path.join(dir, 'dataset')
# if not (os.path.isdir(dataset_path)):
#     os.mkdir(dataset_path)
# df = pd.read_csv(dir + '/students.csv')
# coll = ['0']*len(df['id'])
# print(df)
# df.loc[len(df.index)] = [8,'me']
# print(df)
# df['Attendance'] = coll
# df.to_csv(dir + '/students.csv', index=False)
# if date in df.columns:
#     if (int(df.loc[df['id'] == 7, date].iloc[0]))==0:
#         df.loc[df['id'] == 7, date]=1
#         df.to_csv(dir + '/students.csv', index=False)
#     else:
#         print("Already Exist")
# else:
#     df[date] = coll
#     df.loc[df['id'] == 7, date]=1
#     df.to_csv(dir + '/students.csv', index=False)
# exist = False
# for i in range(len(df['id'])):
#     if df['id'].iloc[i] == 8:
#         exist = True
# if not exist:
#     pass
    # with open(dir + '/students.csv', mode='a', newline='') as csv_file:
    #     fieldnames = ['id', 'name']
    #     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    #     writer.writerow({'id': "1", 'name': "Ankit Raj"})
    # csv_file.close()
