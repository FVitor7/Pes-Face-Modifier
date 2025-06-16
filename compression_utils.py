import zlib
import struct
import logging
from typing import Union

import bpy
from versions import PESVersion, PES_VERSIONS


def _get_version(version: Union[str, PESVersion]) -> PESVersion:
    """Return the :class:`PESVersion` instance for ``version``."""
    if isinstance(version, PESVersion):
        return version
    return PES_VERSIONS[version]


def unzlib(input_path, temp_path, pes_version):
    """Decompress binary data used in PES files."""
    version = _get_version(pes_version)
    logging.debug("Starting unzlib")
    with open(input_path, 'rb') as data:
        data.seek(16)
        if version.extra_skip:
            data.seek(16, 1)
        raw_data = data.read()
    decompressed = zlib.decompress(raw_data, 32)
    with open(temp_path, 'wb') as out:
        out.write(decompressed)
    logging.debug("Finishing unzlib")
    return open(temp_path, 'rb')


def zlib_comp(temp_path, output_path, pes_version, tool_id):
    """Compress binary data back to PES format."""
    version = _get_version(pes_version)
    logging.debug("Starting zlib")
    exp1 = open(temp_path, 'rb').read()
    exp2 = zlib.compress(exp1, 9)
    with open(output_path, 'wb') as exp:
        exp.write(struct.pack('I', version.header))
        if version.esys:
            exp.write(struct.pack('4s', version.esys))
        exp.write(struct.pack('I', len(exp2)))
        exp.write(struct.pack('I', len(exp1)))
        if version.extra_padding:
            exp.write(struct.pack('20s', b''))
        exp.write(exp2)
        if version.extra_padding:
            exp.write(struct.pack('16s', b''))
        exp.write(
            struct.pack(
                'I%dsI%ds' % (len(tool_id), len(version.copyright)),
                0,
                tool_id.encode(),
                0,
                version.copyright.encode(),
            )
        )
    logging.debug("Finishing zlib")

