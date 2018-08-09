# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-08 15:41:11
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-08 15:41:15

import re
emphasis_pattern = re.compile(r'''
        \*          # Beginning emphasis tag -- an asterisk
        (           # Begin group for capturing phrase
        [^\*]+      # Capture anything except asterisk
        )           # End group
        \*          # Ending emphasis tag
        ''', re.VERBOSE)
print(re.sub(emphasis_pattern,r'<em>\1</em>','Hello,*world*!'))