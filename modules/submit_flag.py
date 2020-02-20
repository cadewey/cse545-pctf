# Attempts to take information for team, make a connection and submit a flag
import swpag_client

def name():
    return "submit-flag"

def help():
    return "Submits a flag to score server."

def args():
    return ['team_ip', 'flag_token', 'flag']

def run(args):
	team_uri = 'http://' + args.team_ip + '/'
	flag_token = args.flag_token
	flag = args.flag
	print('Team IP: ' + team_uri)
	print('Team Flag: ' + flag_token)
	print('Attempted Flag: ' + flag)
	try:
		t = swpag_client.Team(team_uri, flag_token)
		print(t.submit_flag([flag]))
	except:
		print("Unable to submit flag!")