from tech_detect import detect_technology
from directories import enumerate_directories

target = input("Target URL: ")

results = detect_technology(target)

print("\nResults")
print("-------")

for key, value in results.items():
    print(f"{key}: {value}")

directories = enumerate_directories(target)

print("\nDirectories Found")
print("-----------------")

for directory, status, title in directories:
    print(
    f"{directory} ({status}) - {title}"
)
