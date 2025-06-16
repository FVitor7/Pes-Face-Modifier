import zlib
import struct
import logging
import bpy


def unzlib(input_path, temp_path, pes_version):
    """Decompress binary data used in PES files."""
    logging.debug("Starting unzlib")
    with open(input_path, 'rb') as data:
        data.seek(16)
        if pes_version in {"pes_pc", "pes_ps2", "pes_psp"}:
            data.seek(16, 1)
        raw_data = data.read()
    decompressed = zlib.decompress(raw_data, 32)
    with open(temp_path, 'wb') as out:
        out.write(decompressed)
    logging.debug("Finishing unzlib")
    return open(temp_path, 'rb')


def zlib_comp(temp_path, output_path, pes_version, tool_id):
    """Compress binary data back to PES format."""
    logging.debug("Starting zlib")
    exp1 = open(temp_path, 'rb').read()
    exp2 = zlib.compress(exp1, 9)
    with open(output_path, 'wb') as exp:
        if pes_version == 'pes13':
            exp.write(struct.pack('I', 0x57010100))
            exp.write(struct.pack('4s', b'ESYS'))
        else:
            exp.write(struct.pack('I', 0x00010600))
        exp.write(struct.pack('I', len(exp2)))
        exp.write(struct.pack('I', len(exp1)))
        if pes_version in {'pes_pc', 'pes_ps2', 'pes_psp'}:
            exp.write(struct.pack('20s', b''))
        exp.write(exp2)
        copyright = "Made by Suat CAGDAS 'sxsxsx'"
        if pes_version in {'pes_pc', 'pes_ps2', 'pes_psp'}:
            exp.write(struct.pack('16s', b''))
            copyright = 'Made by PES Indie Team'
        exp.write(struct.pack('I%dsI%ds' % (len(tool_id), len(copyright)),
                              0, tool_id.encode(), 0, copyright.encode()))
    logging.debug("Finishing zlib")

