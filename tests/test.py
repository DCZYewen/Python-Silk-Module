import pysilk as m

print(m.__version__)

with open("test.pcm", "rb") as f:
    result = m.silkEncode(f.read(), 24000)

with open("result.pcm" , "wb")as f:
    n_result = m.silkDecode(result , 24000)
    f.write(n_result)
    
print("Done")