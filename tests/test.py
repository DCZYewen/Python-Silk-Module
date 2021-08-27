import pysilk as m

print(m.__version__)

with open("test.pcm", "rb") as f:
    result = m.silkEncode(f.read(), 24000)

with open("result.slk" , "wb")as f:
    f.write(result)
    
print(result)