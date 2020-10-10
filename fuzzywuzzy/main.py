from fuzzywuzzy import fuzz

print('{}%'.format(fuzz.ratio("hello", "world")))
print('{}%'.format(fuzz.ratio("Austria", "Australia")))
print('{}%'.format(fuzz.ratio("Albert Thompson", "Albert G. Thompson")))

print('{}%'.format(fuzz.partial_ratio("Albert Thompson", "Albert G. Thompson")))
