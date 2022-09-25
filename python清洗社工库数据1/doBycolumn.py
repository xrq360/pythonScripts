
# -*- coding:utf-8 -*-
import sys
import os
import pandas as pd

#infile = sys.argv[1]

#outfile = sys.argv[2]

def do_f(f):
	infile = "e:/sgk/test/"+f
	outfile = 'e:/sgk/new/0_'+f

	titles= ['username','email','password','salt','idcard','mobile','loginip']	

	dataframe = pd.read_csv(infile, error_bad_lines=False,encoding = 'ISO-8859-1')
	#print(dataframe)
	df_title= dataframe.columns.values
	#print(df_title)
	lendf = len(dataframe)	

	gennull = []
	for x in range(lendf):
		gennull.append('---')	

	username =gennull
	email = gennull
	password = gennull
	salt = gennull
	idcard = gennull
	mobile = gennull
	loginip = gennull	
	
	for t in df_title:
		#t=t.strip()
		print(t)
		if t not in titles:
			continue
		if t == 'username':
			username = dataframe[t]
			continue
		if t == 'email':
			email = dataframe[t]
			continue
		if t == 'password':
			password = dataframe[t]
			continue
		if t == 'salt':
			salt = dataframe[t]
			continue
		if t == 'idcard':
			idcard = dataframe[t]
			continue
		if t == 'mobile':
			mobile = dataframe[t]
			continue
		if t == 'loginip':
			loginip = dataframe[t]
			continue	

	newdf = {'username': username, 'email': email, 'password':password,'salt':salt,'idcard':idcard,'mobile':mobile,'loginip':loginip}
	#print(newdf)
	df = pd.DataFrame(newdf)
	df.to_csv(outfile, index=False,encoding = 'ISO-8859-1')
	print('[+] '+f)

dirs = os.listdir('e:/sgk/test')
for file in dirs:
	print(file)
	do_f(file) 
