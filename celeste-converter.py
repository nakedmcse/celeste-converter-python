# Celeste Format file converter
import os
import io
import struct
import argparse
from PIL import Image


class CelesteConverter:
    def __init__(self):
        self.input_bytes = bytearray()
        self.output_bytes = bytearray()

    def convert(self, input_path: str, output_path: str, command: str, verbose: bool = False):
        target_is_folder = os.path.isdir(output_path)
        if os.path.isdir(input_path):
            workfiles = [os.path.join(input_path, entry) for entry in os.listdir(input_path)]
        else:
            workfiles = [input_path]

        if len(workfiles) == 0:
            print("No workfiles found")
            return
        elif len(workfiles)>1 and not target_is_folder:
            print("More than one input files and output is not a folder")
            return

        for workfile in workfiles:
            if command=="data2png":
                self.data2png(workfile, output_path, target_is_folder, verbose)
            elif command=="png2data":
                self.png2data(workfile, output_path, target_is_folder, verbose)
            else:
                print("Unknown command")

    def data2png(self, workfile: str, output_path: str, target_is_folder: bool, verbose: bool):
        if verbose:
            print(f"Converting {workfile} to {output_path}{" (folder)" if target_is_folder else ""}")

        with io.open(workfile, "rb") as f:
            self.input_bytes = bytearray(f.read())

        width, height = struct.unpack("<ii", self.input_bytes[:8])
        has_alpha = self.input_bytes[8] != 0
        if verbose:
            print(f"Width: {width}, Height: {height}, Alpha: {has_alpha}")

        index, png_index, offset = 0, 0, 9
        while index < width * height:
            # Read RLE count
            rle_count = self.input_bytes[offset]
            offset += 1
            if rle_count == 0:
                print("RLE count is corrupt")
                return

            # Read RGBA values
            a, r, g, b = 0, 0, 0, 0
            if has_alpha:
                a = self.input_bytes[offset]
                offset += 1
                if a != 0:
                    b = self.input_bytes[offset]
                    offset += 1
                    g = self.input_bytes[offset]
                    offset += 1
                    r = self.input_bytes[offset]
                    offset += 1
            else:
                b = self.input_bytes[offset]
                offset += 1
                g = self.input_bytes[offset]
                offset += 1
                r = self.input_bytes[offset]
                offset += 1

            # Output RLE Span of pixels
            for i in range(rle_count):
                self.output_bytes.append(r)
                self.output_bytes.append(g)
                self.output_bytes.append(b)
                if has_alpha:
                    self.output_bytes.append(a)

            index += rle_count

        if target_is_folder:
            filename = os.path.splitext(os.path.basename(workfile))[0] + ".png"
            output_path = os.path.join(output_path, filename)

        mode = "RGBA" if has_alpha else "RGB"
        image = Image.frombytes(mode, (width, height), self.output_bytes)
        image.save(output_path)

    def png2data(self, workfile: str, output_path: str, target_is_folder: bool, verbose: bool):
        print("To be implemented")


# Main Program
parser = argparse.ArgumentParser()
parser.add_argument("command",help="data2png or png2data")
parser.add_argument("input",help="Input path")
parser.add_argument("output",help="Output path")
parser.add_argument("-v","--verbose",action="store_true",help="Verbose output")
args = parser.parse_args()

# Validate
if args.command != "data2png" and args.command != "png2data":
    print("Unknown command")
    exit(1)

if args.input is None:
    print("No input file or directory specified")
    exit(1)

if args.output is None:
    print("No output file or directory specified")
    exit(1)

celeste = CelesteConverter()
celeste.convert(args.input, args.output, args.command, args.verbose)
