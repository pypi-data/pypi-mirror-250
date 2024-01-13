import sys
import AsciiArt

filepath = sys.argv[1]

output = AsciiArt.image_to_string(filepath, False)
