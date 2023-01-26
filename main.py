import opendssdirect as dss

dss.Text.Command('Redirect dss/IEEE13Nodes/IEEE13NodeCkt.dss')

for i in dss.Circuit.AllBusNames():
    print(i)