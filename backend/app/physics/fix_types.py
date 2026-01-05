import sys

# Read the file
with open('scene_builder.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all occurrences
content = content.replace("'Sofa.Core.Node'", 'Any')

# Write back
with open('scene_builder.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Replaced all 'Sofa.Core.Node' with 'Any'")
