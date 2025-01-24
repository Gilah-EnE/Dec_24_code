import re

def find_bytes_pattern(data: bytes, pattern: bytes) -> list[int]:
   pattern_escaped = re.escape(pattern)
   regex = re.compile(pattern_escaped, re.DOTALL)
   return [match.start() for match in regex.finditer(data)]

def perform_signature_analysis(filename: str) -> bool:

    signatures = {
        "ZIP archive": b"\x50\x4b\x03\x04",
        "Empty ZIP archive": b"\x50\x4b\x05\x06",
        "Spanned ZIP archive": b"\x50\x4b\x07\x08",
        "RAR archive": b"\x52\x61\x72\x21\x1a\x07",
        "Portable Network Graphics": b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a",
        "JPEG quantization table ": b"\xff\xd8\xff\xdb",
        "JPEG file start": b"\xff\xd8\xff\xe0",
        "JPEG Exif data": b"\xff\xd8\xff\xe1",
        "GIF version 87a": b"\x47\x49\x46\x38\x37\x61",
        "GIF version 89a": b"\x47\x49\x46\x38\x39\x61",
        "Portable Document Format": b"\x25\x50\x44\x46\x2d",
        "Microsoft WAVE/BWF": b"\x57\x41\x56\x45",
        "Audio-Video Interleave container": b"\x41\x56\x49\x20",
        "Generic RIFF file": b"\x52\x49\x46\x46",
        # "MPEG-1 Audio Layer III audio frame": b"\xff\xfb",    # визначення MP3 за сигнатурою початку файлу є ненадійним у зв'язку з її малим розміром, виявлення по ID3-метаданих є надійнішим, проте воно вимагає наявності таких метаданих в файлах
        # "MPEG-1 Audio Layer II audio frame": b"\xff\xf3",
        # "MPEG-1 Audio Layer I audio frame": b"\xff\xf2",
        "MPEG-1 Audio Layer III ID3v2 tag": b"\x49\x44\x33",
        "MPEG-1 Audio Layer III ID3v1 tag": b"\x54\x41\x47",
        "OGG File": b"\x4f\x67\x67\x53",
        "Free Lossless Audio Codec": b"\x66\x4c\x61\x43",
        "MIDI track": b"\x4d\x54\x68\x64",
        "TAR (Tape Archive)": b"\x75\x73\x74\x61\x72",
        "MPEG-4 Part 14 top-level mdat atom": b'\x6d\x64\x61\x74',
        "MPEG-4 Part 14 type atom": b'\x66\x74\x79\x70'
    }

    found_signatures_total = dict.fromkeys(signatures.keys(), 0)

    with open(filename, 'rb') as file:
        n = 0
        while True:
            chunk = file.read(256*1024*1024)
            if not chunk:
                break
            n += len(chunk)
            print(n/1024/1024)
            
            for sig_type in signatures:
                sig = signatures[sig_type]
                found_signatures_total[sig_type] += len(find_bytes_pattern(chunk, sig))
            del chunk

    return found_signatures_total

print(perform_signature_analysis(r'c:\Users\Gilah\Documents\test.img'))
print(perform_signature_analysis(r'urandom_10mb.bin'))