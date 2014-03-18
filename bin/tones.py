#!/usr/bin/env python

"""
Extracts tones from profile _prfldb files and .psarc files

Usage:
    tones.py FILES...
"""

import json
import psarc


# A bit dirty since dict are not hashable
def uniq_append(tones, ts):
    for tone in ts:
        try:
            tones.index(tone)
        except:
            tones.append(tone)


def from_psarc(filename):
    tones = []

    with open(filename, 'rb') as stream:
        entries = psarc.read_toc(stream)
        for idx, entry in enumerate(entries):
            if not entry['filepath'].endswith('.json'):
                continue

            data = psarc.read_entry(stream, entry)
            x = json.loads(data)

            for k, v in x['Entries'].iteritems():
                e = v['Attributes']
                if 'Tones' in e:
                    uniq_append(tones, e['Tones'])

    return tones


def from_profile(filename):
    tones = []

    keys = ['Tones', 'BassTones', 'DemoTones', 'CustomTones']
    with open(filename, 'rb') as stream:
        profile = psarc.decrypt_profile(stream)
        for tone_type in keys:
            if tone_type in profile:
                uniq_append(tones, profile[tone_type])

    return tones


if __name__ == '__main__':
    from docopt import docopt
    args = docopt(__doc__)

    tones = []
    for f in args['FILES']:
        if f.endswith('.psarc'):
            tones += from_psarc(f)
        elif f.endswith('_prfldb'):
            tones += from_profile(f)

    print json.dumps(tones, indent=2)
