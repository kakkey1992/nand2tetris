import SymbolTable

s=SymbolTable.SymbolTable()

print(s.contains('sum'))
s.addEntry('sum',400)
print(s.contains('sum'))
print(s.getAddress('sum'))
