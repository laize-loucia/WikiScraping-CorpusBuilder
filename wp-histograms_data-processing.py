#configuration :

# list the data files (from the data_collection.py script) you want to process
# (to keep the histograms usable, I recommand not to select more than 6 data files)

    #"2024-04-25_18-58-22_en_Non-fungible token.csv",
    #"2024-04-25_18-58-22_en_Blockchain.csv",
    #"2024-04-25_18-58-22_en_Cryptocurrency.csv",

    #2024-04-25_18-58-22_en_'History of bitcoin', 'en'.csv
    #2024-04-25_18-58-22_en_'Everipedia', 'en'.csv
    #2024-04-25_18-58-22_en_'Do Kwon', 'en'.csv
    #2024-04-25_18-58-22_en_'UBS', 'en'.csv
    #2024-04-25_18-58-22_en_'William Entriken', 'en'.csv
    #2024-04-25_18-58-22_en_'History of video games', 'en'.csv


data_files = [
        
        #"2024-04-25_18-58-22_en_History of video games.csv",
        #"2024-04-25_18-58-22_en_Non-fungible token.csv"
      '2024-04-25_18-58-22_en_Bitcoin.csv',
      #'2024-04-25_18-58-22_en_Cryptocurrency.csv',
      #'2024-04-25_18-58-22_en_History of bitcoin.csv',
      #'2024-04-25_18-58-22_en_Non-fungible token.csv',
    
        #'2024-04-25_18-58-22_en_Everipedia.csv'
        #'2024-04-25_18-58-22_en_History of bitcoin.csv'
        #'2024-04-25_18-58-22_en_List of Internet top-level domains.csv'
        #'2024-04-25_18-58-22_en_History of video games.csv"
        #'2024-04-25_18-58-22_en_Non-fungible token.csv",
        #"2024-04-25_18-58-22_en_Cryptocurrency.csv",
        #"2024-04-25_18-58-22_en_Blockchain.csv",
        #"2024-04-25_18-58-22_en_Bitcoin.csv",
        #"1_Bitcoin.xlsx"

]

# the CSV table and the histogram will present data in this same order

# set the interval of the histogram (the timeframe covered by one bar in the histograms)
# (use 'h' for hour, 'd' for day, 'm' for month, 'y' for year)

histo_interval = 'm'

#histo_interval est utilisé pour spécifier l'intervalle de temps pour les barres dans les histogrammes.
#La valeur 'y' indique que chaque barre dans l'histogramme représente une année.

# set the start / stop timetamps for the histograms (older/newer data will be ignored)
# depending on the interval selected, entire years/months/days/hours will be considered

#Bitcoin 2009 - 2024   
#BCK    2014   2024
# Non-fungible token 2018 2024
# History_of_video_games  2001 2024
# Cryptocurrency 2012 2024
# 6_Do_Kwon       2022 2024
#7_William_Entriken  2023 2024
# 8_List_of_Internet_top_level_domains 2001 2024
#9_History_of_bitcoin 2013  2024
#10_Everipedia 2016 2024

#Par catégorie : Bitcoin Cryptocurrency Non fungible Token
#par période se chevauchant intéressantes : blockchain/bitcoin


histo_start = '2014-01-01_00-00-00'
histo_stop = '2014-12-31_23-59-59'

# When working with histograms, too much data may hinder readability
# I recommand not to exceed 30-40 intervals in the histogram's timeframe
# for exemple, whith a monthly interval, do no plot data for more than 3 years
# If you only use the CSV produced by the script, this limit is not relevant


from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# defining the intervals for the histograms
today_out = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
time_start = datetime.strptime(histo_start, '%Y-%m-%d_%H-%M-%S')
time_stop = datetime.strptime(histo_stop, '%Y-%m-%d_%H-%M-%S')
time_steps = []

if histo_interval == 'h' :
	time_start = time_start.replace(second=0, minute=0)
	time_interval = timedelta(hours=1)
	time_stop = time_stop.replace(second=0, minute=0, hour=time_stop.hour+1)
	time_next = time_start
	while time_next <= time_stop :
		time_steps.append(time_next)
		time_next = time_next + time_interval
elif histo_interval == 'd' :
	time_start = time_start.replace(second=0, minute=0, hour=0)
	time_interval = timedelta(days=1)
	time_stop = time_stop.replace(second=0, minute=0, hour=0, day=time_stop.day+1)
	time_next = time_start
	while time_next <= time_stop :
		time_steps.append(time_next)
		time_next = time_next + time_interval
elif histo_interval == 'm' :
	time_start = time_start.replace(second=0, minute=0, hour=0, day=1)
	if time_stop.month == 12 :
		time_stop = time_stop.replace(second=0, minute=0, hour=0, day=1, month=1, year=time_stop.year+1)
	else :
		time_stop = time_stop.replace(second=0, minute=0, hour=0, day=1, month=time_stop.month+1)
	time_next = time_start
	while time_next <= time_stop :
		time_steps.append(time_next)
		if time_next.month == 12 :
			time_next = time_next.replace(month=1, year=time_next.year+1)
		else :
			time_next = time_next.replace(month=time_next.month+1)
else :
	time_start = time_start.replace(second=0, minute=0, hour=0, day=1, month=1)
	time_stop = time_stop.replace(second=0, minute=0, hour=0, day=1, month=1, year=time_stop.year+1)
	time_next = time_start
	while time_next <= time_stop :
		time_steps.append(time_next)
		time_next = time_next.replace(year=time_next.year+1)



histo_data = {}
# for each data file, we import the data
for data_file in data_files :
	# we initialize the histogram's structure
	histo_data[data_file] = {}
	for time_step in time_steps :
		histo_data[data_file][str(time_step)] = 0
	# opening the file as a list of timestamps
	f = open(data_file)
	r = f.read()
	timestamps = r[:-1].split('\n')
	# for each timestamp
	for timestamp in timestamps :
		time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
		# we look through the time_steps for a match
		for i in range(0, len(time_steps) -1) :
			if time >= time_steps[i] and time < time_steps[i+1] :
				histo_data[data_file][str(time_steps[i])] += 1
				break

# building a nice CSV output
# each timestep is a row, each file is a column
out = 'timeframe'
for data_file in data_files :
	# we name the files in a nice yet short way
	# ex : Dorayaki(fr), Dorayaki(en)
	out += '\t' + data_file[23:-4] + '(' + data_file[20:22] + ')'
out += '\n'
# in the meantime, we also extract nice data tables for the histograms
data_tables = {}
for data_file in data_files :
	data_tables[data_file] = []

# we dont use the last timestep, which was only used as a limit for the previous one
for time_step in time_steps[:-1] :
	# we name the timestep in a clear yet short way
	# ex, for months : 2022 / 1, 2, 3 ... 11, 12, 2023 / 1, 2 3 ....
	if histo_interval == 'h' :
		if time_step.hour == 0 :
			step = str(time_step.day) + ' / 00h'
		else :
			step = str(time_step.hour) + 'h'
	elif histo_interval == 'd' :
		if time_step.hour == 1 :
			step = str(time_step.month) + ' / 1'
		else :
			step = str(time_step.day)
	elif histo_interval == 'm' :
		if time_step.month == 1 :
			step = str(time_step.year) + ' / 1'
		else :
			step = str(time_step.month)
	else :
		step = str(time_step.year)
	out += step
	# then we add the numbers for each datafile
	for data_file in data_files :
		out += '\t' + str(histo_data[data_file][str(time_step)])
		data_tables[data_file].append(histo_data[data_file][str(time_step)])
	out += '\n'



# saving to a text file
f = open(today_out + '_processed-data.csv', 'w', encoding='utf-8')
f.write(out)
f.close()


print(1)
print("making the separated histograms")

f = plt.figure(figsize=(12,2*len(data_files)))
i = 1
# each data file has it's own subplot
for data_file in data_files :
	plt.subplot(len(data_files), 1, i)
	plt.xticks(rotation=90)
	if histo_interval == 'm' :
		plt.bar(time_steps[:-1],data_tables[data_file], width=24)
	elif histo_interval == 'y' :
		plt.bar(time_steps[:-1],data_tables[data_file], width=290)
	else :
		plt.bar(time_steps[:-1],data_tables[data_file])
	plt.title(data_file[23:-4] + '(' + data_file[20:22] + ')')
	i += 1
f.tight_layout()
f.savefig(today_out + 'Culture_separated_.png')


print(2)
print("stacked histogram")


f = plt.figure(figsize=(12,6))
plt.xticks(rotation=90)
# each data file has it's own subplot
for data_file in data_files :
	if histo_interval == 'm' :
		plt.bar(time_steps[:-1],data_tables[data_file], width=24, label=data_file[23:-4] + '(' + data_file[20:22] + ')')
	elif histo_interval == 'y' :
		plt.bar(time_steps[:-1],data_tables[data_file], width=290, label=data_file[23:-4] + '(' + data_file[20:22] + ')')
	else :
		plt.bar(time_steps[:-1],data_tables[data_file], label=data_file[23:-4] + '(' + data_file[20:22] + ')')
plt.legend()
plt.grid(axis='y', color='purple', linestyle='-', linewidth=0.5)
f.tight_layout()
f.savefig(today_out + 'Culture_stacked_histogram.png')


