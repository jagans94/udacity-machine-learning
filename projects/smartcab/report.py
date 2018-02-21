import numpy as np
import pandas as pd
import os
import ast

def calculate_reliability(data):
	""" Calculates the reliability rating of the smartcab during testing. """

	success_ratio = data['success'].sum() * 1.0 / len(data)
	print "Reliability: {}".format(success_ratio)

def calculate_safety(data):
	""" Calculates the safety rating of the smartcab during testing. """

	good_actions = data['actions'].apply(lambda x: ast.literal_eval(x)[0])
	good_ratio = good_actions.sum() * 1.0 / (data['initial_deadline'] - data['final_deadline']).sum()

	if good_ratio == 1: # Perfect driving
		print "Perfect Driving!!"
	else:
		print "Imperfect Driving :("
	 
	major_acc = data['actions'].apply(lambda x: ast.literal_eval(x)[4]).sum()
	minor_acc = data['actions'].apply(lambda x: ast.literal_eval(x)[3]).sum()
	major_vio = data['actions'].apply(lambda x: ast.literal_eval(x)[2]).sum()
	minor_vio = data['actions'].apply(lambda x: ast.literal_eval(x)[1]).sum()

	print "Major accident = {}, Minor accident = {}, Major violation = {}, Minor violation = {}"\
	.format(major_acc, minor_acc, major_vio, minor_vio)

	if major_acc > 0: # Major accident
		grade = "F"
	elif minor_acc > 0: # Minor accident
		grade = "D"
	elif major_vio > 0: # Major violation
		grade = "C"
	else: # Minor violation
		if minor_vio >= len(data)/2: # Minor violation in at least half of the trials
			grade = "B"
		else:
			grade = "A"

	print "Grade: {}".format(grade)

def run():
	csv = 'sim_improved-learning.csv'
	data = pd.read_csv(os.path.join("logs", csv))
	testing_data = data[data['testing'] == True]
	calculate_reliability(testing_data)
	calculate_safety(testing_data)

if __name__ == '__main__':
    run()