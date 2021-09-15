#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64

open_icon = open("E:\\python\\monkeyUtils\\logo.ico", "rb")
b64str = base64.b64encode(open_icon.read())
open_icon.close()
write_data = "img = %s" % b64str
f = open("E:\\python\\monkeyUtils\\utils\\icon.py", "w+")
f.write(write_data)
f.close()