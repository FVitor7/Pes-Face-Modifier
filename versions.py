from dataclasses import dataclass

@dataclass(frozen=True)
class PESVersion:
    code: str
    header: int
    esys: bytes = b''
    extra_skip: bool = False
    extra_padding: bool = False
    copyright: str = "Made by Suat CAGDAS 'sxsxsx'"

# Define supported game versions
PES_VERSIONS = {
    'pes13': PESVersion(
        code='pes13',
        header=0x57010100,
        esys=b'ESYS',
    ),
    'pes_pc': PESVersion(
        code='pes_pc',
        header=0x00010600,
        extra_skip=True,
        extra_padding=True,
        copyright='Made by PES Indie Team',
    ),
    'pes_ps2': PESVersion(
        code='pes_ps2',
        header=0x00010600,
        extra_skip=True,
        extra_padding=True,
        copyright='Made by PES Indie Team',
    ),
    'pes_psp': PESVersion(
        code='pes_psp',
        header=0x00010600,
        extra_skip=True,
        extra_padding=True,
        copyright='Made by PES Indie Team',
    ),
}
