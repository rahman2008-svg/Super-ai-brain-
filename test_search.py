import wikipedia
wikipedia.set_lang("bn")
query = "বাংলাদেশের রাজধানী"
try:
    print("Wikipedia:", wikipedia.summary(query, sentences=2))
except:
    print("Wikipedia not found")
