import os, pandas

cwd = os.getcwd()


names = ["Player", "Season", "Team", "Position", "GP", "TOI", "G", "A", "P", "P1", "P/60", "P1/60", "GS", "GS/60", "CF", "CA", "C+/-", "CF%", "Rel CF%", "GF", "GA", "G+/-", "GF%", "Rel GF%", "xGF", "xGA", "xG+/-", "xGF%", "Rel xGF%", "iPENT", "iPEND", "iP+/-", "iCF", "iCF/60", "ixGF", "ixGF/60", "iSh%", "PDO", "ZSR", "TOI%", "TOI% QoT", "CF% QoT", "TOI% QoC", "CF% QoC"]


seventeen_eighteen = pandas.read_csv(cwd+'/2017_18.csv', names=names)
sixteen_seventeen = pandas.read_csv(cwd+'/2016_17.csv', names=names)
fifteen_sixteen = pandas.read_csv(cwd+'/2015_16.csv', names=names)


replacement_cols = ["G", "A", "P", "P1", "P/60", "P1/60", "GF", "GA", "G+/-", "GF%"]
seventeen_eighteen[replacement_cols] = seventeen_eighteen[replacement_cols].replace('--', 0)
sixteen_seventeen[replacement_cols] = sixteen_seventeen[replacement_cols].replace('--', 0)
fifteen_sixteen[replacement_cols] = fifteen_sixteen[replacement_cols].replace('--', 0)

s1 = seventeen_eighteen.to_dict('records')
s2 = sixteen_seventeen.to_dict('records')
s3 = fifteen_sixteen.to_dict('records')

data = s1+s2+s3
