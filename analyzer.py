from collections import defaultdict
import re

MIN_FREQ = 5

file = 'history.txt'
# My zsh history has numbers before each command, need to parse them out.
_capture = r' *\d*\*? +(.*)'


def find_frequencies(file):
    apps = defaultdict(lambda: defaultdict(int))
    with open(file, "r") as f:
        for line in f:
            line = line.strip('\n')
            group = re.match(_capture, line).group(1)
            args = group.split(" ")
            app = args[0]
            target = ''
            if len(args) > 1:
                target = args[1]

            # Default dicts are amazing
            apps[app][target] += 1

    # Get the frequency of each application use.
    totals = defaultdict(int)
    for app in apps:
        totals[app] = sum((x[1] for x in apps[app].items()))

    # Sort those frequencies
    totals = reversed(sorted(totals.items(), key=lambda x: x[1]))

    for application in totals:
        app = application[0]
        freq = application[1]

        # Only display commands that occur frequently.
        if freq > MIN_FREQ:
            print app + ": " + str(freq)
            sorted_targets = sorted(apps[app].items(), key=lambda x: x[1])
            sorted_targets = reversed(sorted_targets)
            for targ in sorted_targets:
                if targ[1] > 2:
                    if targ[0] == '':
                        print "\t'': " + str(targ[1])
                    else:
                        print "\t" + targ[0] + ": " + str(targ[1])
            print ''

if __name__ == "__main__":
    find_frequencies(file)
