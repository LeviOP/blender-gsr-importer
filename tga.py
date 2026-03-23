from dataclasses import dataclass
from typing import BinaryIO, Optional

@dataclass
class Tga:
    width: int
    height: int
    pixels: bytes  # RGBA, top-to-bottom, uint8

    @staticmethod
    def load(f: BinaryIO, buffer_size) -> Optional['Tga']:
        data = f.read()

        if len(data) < 18:  # sizeof(TargaHeader)
            return None

        pos = 0

        id_length      = data[pos];  pos += 1
        colormap_type  = data[pos];  pos += 1
        image_type     = data[pos];  pos += 1

        # colormap_index (2), colormap_length (2)
        pos += 4
        # colormap_size (1)
        pos += 1

        # x_origin (2), y_origin (2)
        pos += 4

        width  = data[pos] | (data[pos + 1] << 8);  pos += 2
        height = data[pos] | (data[pos + 1] << 8);  pos += 2

        pixel_size = data[pos];  pos += 1
        # attributes (1)
        pos += 1

        if image_type != 2 and image_type != 10:
            return None

        if colormap_type != 0 or (pixel_size != 32 and pixel_size != 24):
            return None

        num_pixels = width * height

        if num_pixels > 0x1FFFFFFF:
            return None

        size = num_pixels * 4

        if size > buffer_size:
            return None

        # skip image comment
        pos += id_length

        buffer = bytearray(size)

        if image_type == 2:  # uncompressed RGB
            if pixel_size == 24:
                expected = num_pixels * 3
            else:
                expected = num_pixels * 4

            if pos + expected > len(data):
                return None

            for row in range(height - 1, -1, -1):
                pix_pos = row * width * 4
                for _ in range(width):
                    blue  = data[pos];  pos += 1
                    green = data[pos];  pos += 1
                    red   = data[pos];  pos += 1

                    if pixel_size == 32:
                        alpha = data[pos];  pos += 1
                    else:
                        alpha = 255

                    buffer[pix_pos]     = red
                    buffer[pix_pos + 1] = green
                    buffer[pix_pos + 2] = blue
                    buffer[pix_pos + 3] = alpha
                    pix_pos += 4

        elif image_type == 10:  # RLE
            row = height - 1
            column = 0
            pix_pos = row * width * 4

            while row >= 0:
                if pos >= len(data):
                    break

                packet_header = data[pos];  pos += 1
                packet_size = 1 + (packet_header & 0x7f)

                if packet_header & 0x80:  # run-length packet
                    blue  = data[pos];  pos += 1
                    green = data[pos];  pos += 1
                    red   = data[pos];  pos += 1

                    if pixel_size == 32:
                        alpha = data[pos];  pos += 1
                    else:
                        alpha = 255

                    for _ in range(packet_size):
                        buffer[pix_pos]     = red
                        buffer[pix_pos + 1] = green
                        buffer[pix_pos + 2] = blue
                        buffer[pix_pos + 3] = alpha
                        pix_pos += 4

                        column += 1
                        if column == width:
                            column = 0
                            row -= 1
                            if row < 0:
                                break
                            pix_pos = row * width * 4

                else:  # non run-length packet
                    for _ in range(packet_size):
                        blue  = data[pos];  pos += 1
                        green = data[pos];  pos += 1
                        red   = data[pos];  pos += 1

                        if pixel_size == 32:
                            alpha = data[pos];  pos += 1
                        else:
                            alpha = 255

                        buffer[pix_pos]     = red
                        buffer[pix_pos + 1] = green
                        buffer[pix_pos + 2] = blue
                        buffer[pix_pos + 3] = alpha
                        pix_pos += 4

                        column += 1
                        if column == width:
                            column = 0
                            row -= 1
                            if row < 0:
                                break
                            pix_pos = row * width * 4

        return Tga(width=width, height=height, pixels=bytes(buffer))
