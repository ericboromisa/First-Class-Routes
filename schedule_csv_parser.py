
import csv
import sqlite3
import os
from datetime import date 
from datetime import datetime
from datetime import timedelta

from operator import itemgetter


# Commented Out Test Database

schedule_file = "Flights2015.csv"

MIN_SEATS = 0
MAX_SEATS = 15
MIN_NUM_OF_FLYING_DAYS = 30


def build_database():
	# If table doesn't exist, create it
	

	# Open the CSV and Upsert each row - rows already in will be skipped, new rows added, updated rows updated
	print "Creating Flight Database..."
	keys = []
	routes = []
	equips = ['32B', '330', '332', '333', '33F', '33X', '342', '343', '345', '346', '380', '388', '744', '747', '74E', '74F', '74H', '74M', '74N', '74T', '74X', '74Y', '772', '773', '777', '77F', '77L', '77W', '77X', '787', '788', '789']
	oneworld = ['AA', 'BA', 'CX', 'QR', 'QF', 'MH', 'JL', 'JJ']
	star_alliance = ['UA', 'LH', 'LX', 'NH', 'OZ', 'TG', 'SQ', 'CA', 'UA']
	skyteam = ['AF', 'KE', 'GA', 'CI', 'MU', 'CZ']
	non_aligned = ['EY', 'EK', 'LY']
	alliance_comprehension = {'oneworld': oneworld, 'star_alliance': star_alliance, 'skyteam': skyteam, 'non_aligned': non_aligned}
	colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'black', 'white', 'navy']
	r = open(schedule_file)
	# File must be saved as windows csv
	raw_schedule_reader = csv.reader(r)
	rownum = 0
	for row in raw_schedule_reader:
		if (rownum == 0):
			keys = row
			
			rownum += 1
		
		else:

			carrier = row[keys.index('carrier')]
			opcarrier = row[keys.index('opcarrier')]
			number = row[keys.index('fltno')]
			departure_time = row[keys.index('departure_time')]
			arrival_time = row[keys.index('arrival_time')]
			origin = row[keys.index('origin')]
			destination = row[keys.index('destination')]
			
			equip = row[keys.index('equip')]
			seats_f = int(row[keys.index('seats_fst')])
			seats_c = int(row[keys.index('seats_bus')])
			seats_y = int(row[keys.index('seats_eco')])

			#Filter out freighters and flights with 0 seats
			#print seats_y, seats_c, seats_f
			
			if(seats_f > MIN_SEATS and seats_f < MAX_SEATS):
				
				if(equip in equips):

					effective_from = row[keys.index('effective_from')]
					effective_to = row[keys.index('effective_to')]

					start_date = datetime.strptime(effective_from, "%m/%d/%y").date()
					end_date = datetime.strptime(effective_to, "%m/%d/%y").date()

					days_flying = (end_date-start_date).days
					for alliance in alliance_comprehension:
						if carrier in alliance_comprehension[alliance]:
							if days_flying > MIN_NUM_OF_FLYING_DAYS:
								routes.append([alliance, carrier, origin, destination, equip, seats_f, start_date, end_date, days_flying])

			
					

	routes.sort()

	with open('first_class_routes.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile, dialect='excel')
		str_output = ""
		writer.writerow(['Alliance', 'Carrier', 'Origin', 'Destination', 'Equip', 'seats_f', 'start_date', 'end_date', 'days_flying'])
		
		# Write to CSV
		for route in routes:
			writer.writerow(route)
			print route
		
		# Generate a GCMAP-friendly string that changes colors with each carrier
		user_input = raw_input("Enter which alliance you would like a GCMAP string for (oneworld, skyteam, star_alliance, non_aligned): ")
		curr_carrier = ""
		color_counter = 0
		for route in routes:

			if(route[0] == user_input):
				print route
				
				if route[1] != curr_carrier:
					curr_carrier = route[1]
					print curr_carrier
					str_output += 'color:'
					str_output += colors[color_counter]
					str_output += ", "
					color_counter += 1
				str_output += route[2]
				str_output += "-"
				str_output += route[3]
				str_output += ", "
	
	print str_output


	

				


# This build's a 5 Million line Flight Schedule Database when uncommented - make sure you have sufficient system resources and 2-3 mins to run
build_database()
#read_out_database()

