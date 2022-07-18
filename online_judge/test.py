import filecmp

result = filecmp.cmp('output.txt', 'media/test_outputs/output.txt', shallow=False)
print(result)