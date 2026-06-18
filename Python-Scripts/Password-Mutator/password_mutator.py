print("Password Mutator")
print("----------------")

base = input("Enter base word: ")

mutations = set()

# Original

mutations.add(base)

# Capitalization

mutations.add(base.capitalize())
mutations.add(base.upper())

# Numbers

numbers = [
"1",
"12",
"123",
"1234",
"2024",
"2025",
"2026"
]

for num in numbers:

```
mutations.add(base + num)
mutations.add(base.capitalize() + num)
```

# Special Characters

specials = [
"!",
"@",
"#",
"$"
]

for special in specials:

```
mutations.add(base + special)
mutations.add(base.capitalize() + special)
```

# Number + Special

for num in numbers:

```
mutations.add(base + num + "!")
mutations.add(base.capitalize() + num + "!")
```

print("\nGenerated Passwords")
print("-------------------")

for password in sorted(mutations):

```
print(password)
```

print(f"\nTotal Passwords Generated: {len(mutations)}")
