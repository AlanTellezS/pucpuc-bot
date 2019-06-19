from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os
import json

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.
spreadsheet = '1JVWv1nTdpagMDC5cEExYvQmiluBnpkx4Y1Kypl74bIk'

#Ranges of each state and the name of the file
info = [
    ["'1-3 Star Ema List'!D3:G", "Hitagi Crab"],
    ["'1-3 Star Ema List'!J3:M", "Mayoi Snail"],
    ["'1-3 Star Ema List'!P3:S", "Suruga Monkey"],
    ["'1-3 Star Ema List'!V3:Y", "Nadeko Snake"],
    ["'1-3 Star Ema List'!AB3:AE", "Tsubasa Cat"],
    ["'1-3 Star Ema List'!AH3:AK", "Karen Bee"],
    ["'1-3 Star Ema List'!AT3:AW", "Zaregoto"]
]

ema4_5 = "'4-5 Star Ema Skills'!B2:P102"

puc = "'Puc Skills'!B2:S88"

skills = "'1-3 Star Ema Guide'!A3:C30"

strats = "'Ema Combos'!C4:L"

def updateStrats():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet = service.spreadsheets()

    f = open("strats.json", "w")

    f.write("{\n")
    f.write('\t"data" : [\n')

    result = sheet.values().get(spreadsheetId=spreadsheet,
                                range=strats).execute()
    values = result.get('values', [])
    l = len(values)

    if not values:
        print('No data found.')
    else:
        for i in range(0, l):
            if len(values[i]) == 0:
                continue
            f.write('\t\t[')
            for j in range(0,len(values[i])):
                if (values[i][j] != ''):
                    f.write('"%s"' % values[i][j])
                    if (j<len(values[i])-1):
                        f.write(",")
            f.write("]")
            if(i<l-1):
                f.write(",")
            
            f.write("\n")
            
    f.write("\t]\n")
    f.write("}")
    f.close()

def updateDB1_3():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
        
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet = service.spreadsheets()

    f = open("emaList.json", "w")

    f.write("{\n")
    f.write('"data" : [\n')

    for inf in info:
        result = sheet.values().get(spreadsheetId=spreadsheet,
                                    range=inf[0]).execute()
        values = result.get('values', [])
        l = len(values)

        if not values:
            print('No data found.')
        else:
            for i in range(0, l):
                howto = values[i][0].replace('\n', " ")

                f.write('\t\t[ "%s", "%s", "%s", "%s", "%s" ]' % (howto, values[i][1], values[i][2], values[i][3], inf[1]))

                if (inf[1] != "Zaregoto" or i<l-1):
                    f.write(",\n")

    f.write("\t]\n")
    f.write("}")
    f.close()

def updateDB4_5():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet = service.spreadsheets()

    f = open("emaList4_5.json", "w")

    f.write("{\n")
    f.write('\t"data" : [\n')

    result = sheet.values().get(spreadsheetId=spreadsheet,
                                range=ema4_5).execute()
    values = result.get('values', [])
    l = len(values)

    if not values:
        print('No data found.')
    else:
        for i in range(0, l):
            skill = values[i][2].split("\n")
            skill = ", ".join(skill)
            f.write('\t\t[ "%s", "%s", "%s", "%s", "%s"]' % (values[i][0], values[i][1], skill, values[i][10], values[i][14]))
            if(i<l-1):
                f.write(",")
            f.write("\n")

    f.write("\t]\n")
    f.write("}")
    f.close()

def updatePuc():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet = service.spreadsheets()

    f = open("puc.json", "w")

    f.write("{\n")
    f.write('\t"data" : [\n')

    result = sheet.values().get(spreadsheetId=spreadsheet,
                                range=puc).execute()
    values = result.get('values', [])
    l = len(values)

    if not values:
        print('No data found.')
    else:
        for i in range(0, l):
            if(len(values[i])<10): continue
            else:
                skill = values[i][1].split("\n")
                skill = ", ".join(skill)
                ema = values[i][12].split("\n")
                ema = ",".join(ema)
                f.write('\t\t[ ')
                f.write('%d, ' % (i+1))
                for j in range (0, len(values[i])):
                    if(j==1): f.write('"' + skill + '"')
                    elif(j==12): f.write('"' + ema + '"')
                    else: f.write('"%s"' % values[i][j])
                    if(j<len(values[i])-1): f.write(", ")
                f.write("]")
                if(i<l-1):
                    f.write(",")
                f.write("\n")

    f.write("\t]\n")
    f.write("}")
    f.close()

def updateSkills():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet = service.spreadsheets()

    f = open("skills.json", "w")

    f.write("{\n")
    f.write('\t"data" : [\n')

    result = sheet.values().get(spreadsheetId=spreadsheet,
                                range=skills).execute()
    values = result.get('values', [])
    l = len(values)

    if not values:
        print('No data found.')
    else:
        for i in range(0, l):
            f.write('\t\t[ "%s", "%s"]' % (values[i][0], values[i][2]))
            if(i<l-1):
                f.write(",")
            f.write("\n")

    f.write("\t]\n")
    f.write("}")
    f.close()

if __name__ == "__main__":
    updateStrats()
    updateDB4_5()

