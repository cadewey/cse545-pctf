# Gets the team and service flags
def name():
    return "get-service-flags"

def help():
    return "Get list of Team and Flag for service"

def args():
    return ['serviceid']

def run(args):
    import swpag_client
    serviceid = args.serviceid
    t = swpag_client.Team("http://34.195.187.175", "f67634a9373be60a439287965e1d8562")
    flags = t.get_targets(int(serviceid))

    for target in flags:
        team = target['hostname']
        flag_id = target['flag_id']
        print("Team: {0}, FLAG: {1}".format(team, flag_id))