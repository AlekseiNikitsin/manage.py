# import base64
# s = '''SGVsbG8gd29ybGQgISBHbyB0byBiZWQh'''#расшифровка
# print(base64.b64decode(s).decode())#расшиф
# import quopri
#
# s = '''=D0=9F=D1=80=D0=B8=D0=B2=D0=B5=D1=82'''
# Str_1 = bytes(s, 'UTF-8')
# Str_2 = quopri.decodestring(Str_1)
# Str_3 = Str_2.decode('UTF-8')
# print(Str_3)
#
# #Приводим кириллицу из кодировки quoted printable в кодировку UTF-8