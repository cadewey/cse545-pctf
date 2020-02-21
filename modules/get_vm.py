# Attempts to take information for team, make a connection, and give info!
import swpag_client

def name():
    return "get-vm"

def help():
    return "Reveals Server VM info."

def args():
    return ['team_ip', 'flag_token']

def run(args):
	team_uri = 'http://' + args.team_ip + '/'
	flag_token = args.flag_token
	print('Team IP: ' + team_uri)
	print('Team Flag: ' + flag_token)
	try:
		t = swpag_client.Team(team_uri, flag_token)
		print(t.get_vm())
	except:
		print("Unable to get VM info!")
