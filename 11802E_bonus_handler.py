import math
import tqdm
import time
import numpy as np
from numpy import int32
import pandas as pd
import boto3



BONUS_FILENAME = '11802E_bonuses_42_051719.csv'
#BONUS_REASON = 'Thank you for participating in The Estimation Game with the Kellogg School of Management. You have received this bonus based on your performance in the study.\n\nWe hope to have you as a participant again in the near future!\n\nBest,\nKellogg Research Support'
#BONUS_REASON = 'Thanks for participating in the Estimation Game with Real Time Labs.'

# ***
BONUS_REASON = 'Thanks for participating in the Estimation Challenge with the Kellogg School of Management.'
# ***


#BONUS_REASON = 'Thank you for your attempt to participate in the News Assessment Game. Due to a technical error, we were unable to assign you to a game. In appreciation for your time, we are submitting a bonus to your account.'
#BONUS_REASON = 'Hello,\n\nThank you for participating in the Estimation Game.  We experienced an error with our game assignment system that send you straight to the exit survey instead of presenting you with the game.  Please note that you will still receive your guaranteed minimum $0.50 bonus.  Additionally, we will invite you again for the 5pm (ET) game later today.\n\nBest regards,\n\nJoshua Becker and Kellogg eLab'

#BONUS_REASON = 'Thank you for participating in Study 31911E with the Kellogg School of Management.\n\nWe hope to have you as a participant again in the near future!\n\nBest,\nKellogg Research Support'
#BONUS_REASON = 'Please accept our sincere apologies for issues with the News Assessment game on Friday.  For more information, contact Joshua.Becker@Kellogg.Northwestern.edu'


RECEIPT_FILENAME = '11802E_bonuses_42_051719_PROCESSED.txt'
tf = open(RECEIPT_FILENAME, 'a')


# Colors for terminal output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



client = boto3.client(service_name = 'mturk', region_name='us-east-1')


# Grab bonus file
bonus_file = pd.read_csv(BONUS_FILENAME, header = 0, encoding = 'latin')
worker_ids_to_bonus = bonus_file['MID'].tolist()

worker_ids_to_bonus = [str(w).split(' ')[0] for w in worker_ids_to_bonus]

bonuses = bonus_file['bonus'].tolist()


#Grab clean pool file
pool = pd.read_csv('clean_pool.csv', header = 0)



for i in range(len(worker_ids_to_bonus)):
	w_id = worker_ids_to_bonus[i]
	bonus = bonuses[i]
	bonus_string = str(bonus)

	try:

		assignment = pool.loc[pool['worker_id'] == w_id, 'assignment_id'].tolist()[0]

		if (bonus > 0):
	
			try:
			
				#client.send_bonus(
			   	#	WorkerId = w_id,
			    #	BonusAmount = bonus_string,
			    #	AssignmentId = assignment,
			    #	Reason = BONUS_REASON
				#)

				print(bcolors.OKBLUE + bcolors.BOLD + 'Paid : ' + str(i + 1) + ' / ' + str(len(worker_ids_to_bonus)) + ' @ $' + bonus_string + bcolors.ENDC)

				tf.write(w_id + '\t' + assignment + '\t' + bonus_string + '\n')
		
			except:
		
				print('Worker ' + w_id + ' threw an error!')

	except:
		print('Worker ' + w_id + ' is not in the pool!')


tf.close()




