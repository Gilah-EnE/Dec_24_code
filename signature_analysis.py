signatures = {
    'ZIP archive': b'\x50\x4b\x03\x04',
    'Empty ZIP archive': b'\x50\x4b\x05\x06',
    'Spanned ZIP archive': b'\x50\x4b\x07\x08',
    'RAR archive': b'\x52\x61\x72\x21\x1a\x07',
    'Portable Network Graphics': b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a',
    'JPEG quantization table ': b'\xff\xd8\xff\xdb',
    'JPEG file start': b'\xff\xd8\xff\xe0',
    'JPEG Exif data': b'\xff\xd8\xff\xe1',
    'GIF version 87a': b'\x47\x49\x46\x38\x37\x61',
    'GIF version 89a': b'\x47\x49\x46\x38\x39\x61',
    'Portable Document Format': b'\x25\x50\x44\x46\x2d',
    'Microsoft WAVE/BWF': b'\x57\x41\x56\x45',
    'Audio-Video Interleave container': b'\x41\x56\x49\x20',
    'Generic RIFF file': b'\x52\x49\x46\x46',
    'MPEG-1 Audio Layer III audio frame': b'\xff\xfb',
    'MPEG-1 Audio Layer II audio frame': b'\xff\xf3',
    'MPEG-1 Audio Layer I audio frame': b'\xff\xf2',
    'MPEG-1 Audio Layer III ID3v2 tag': b'\x49\x44\x33',
    'MPEG-1 Audio Layer III ID3v1 tag': b'\x54\x41\x47',
    'OGG File': b'\x4f\x67\x67\x53',
    'Free Lossless Audio Codec': b'\x66\x4c\x61\x43',
    'MIDI track': b'\x4d\x54\x68\x64',
    'TAR (Tape Archive)': b'\x75\x73\x74\x61\x72'
}

data = b'\x50\x4b\x03\x04\x00\x50\x4b\x03\x04\x41\x56\x49\x20\x41\x56\x49\x20'

for sig_type in signatures:
    positions = []
    sig = signatures[sig_type]
    pos = 0
    while True:
        pos = data.find(sig, pos)
        if pos == -1:
            break
        positions.append(pos)
        pos += 1

    print(sig_type, positions)