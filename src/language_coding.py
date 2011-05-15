#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       $$
#
#       Copyright 2010 Michel Samia <m.samia@seznam.cz>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import pycountry
import lmf_merger


def to_ISO_639_2T(code, coding):
    if code is None:
        return None

    # first try the three-letter codes
    if coding == 'ISO 639-3' or coding == 'ISO 639-2':
        try:
            return pycountry.languages.get(bibliographic = code).terminology
        except KeyError:
            pass

        try:
            return pycountry.languages.get(terminology = code).terminology
        except KeyError:
            raise lmf_merger.FatalMergeError('code %s not found in %s' % (code, coding) )

    elif coding == 'ISO 639-1':
        try:
            return pycountry.languages.get(alpha2 = code).terminology
        except KeyError:
            raise lmf_merger.FatalMergeError('code %s not found in %s' % (code, coding) )

    # autodetection
    elif coding == None:
        if len(code) == 2:
            return to_ISO_639_2T(code, 'ISO 639-1')

        elif len(code) == 3:
            return to_ISO_639_2T(code, 'ISO 639-3')

        # try it as a name
        else:
            try:
                return pycountry.languages.get(name = code).terminology
            except KeyError:
                raise lmf_merger.FatalMergeError('Language coding detection failed, unknown code %s' % code)


    else:
        raise lmf_merger.FatalMergeError('Unknown language coding %s' % coding)

