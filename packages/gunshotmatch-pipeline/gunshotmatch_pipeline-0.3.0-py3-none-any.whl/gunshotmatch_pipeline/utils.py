#!/usr/bin/env python3
#
#  utils.py
"""
General utility functions.
"""
#
#  Copyright © 2023 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# 3rd party
from domdf_python_tools.words import Plural

try:
	# 3rd party
	import tomllib  # type: ignore[import]
except ImportError:
	# 3rd party
	import tomli as tomllib  # type: ignore[no-redef]

__all__ = ("project_plural", "friendly_name_mapping", "tomllib")

#: :class:`domdf_python_tools.words.Plural` for ``project``.
project_plural = Plural("project", "projects")

#: Mapping of IUPAC preferred names to more common, friendlier names.
friendly_name_mapping = {
		# IUPAC: Friendly
		"Benzenamine, 4-nitro-N-phenyl-": "4-NDPA",
		"Benzenamine, 2-nitro-N-phenyl-": "2-NDPA",
		"N,N'-Diethyl-N,N'-diphenylurea": "Ethyl Centralite",
		"Benzene, nitro-": "Nitrobenzene",
		"Benzene, 2-methyl-1,3-dinitro-": "2,6-DNT",
		"Benzene, 1-methyl-2,3-dinitro-": "2,3-DNT",
		"Benzene, 1-methyl-2,4-dinitro-": "2,4-DNT"
		}
