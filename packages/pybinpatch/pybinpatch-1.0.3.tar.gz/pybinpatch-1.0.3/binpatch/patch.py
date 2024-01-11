
from .file import readBinaryFromPath, readJsonAtPath, writeBinaryToPath


def patchBufferAtIndex(data, index, old, new):
    index_int = int(index, base=16)

    if isinstance(old, str):
        old = b''.fromhex(old)

    old_len = len(old)

    if isinstance(new, str):
        new = b''.fromhex(new)

    new_len = len(new)

    if old_len != new_len:
        raise Exception('Source lengths differ!')

    buffer = data[index_int:index_int+old_len]
    buffer_len = len(buffer)

    if buffer_len != old_len:
        raise Exception('Buffer size mismatch!')

    if buffer == old:
        data[index_int:index_int+old_len] = new


def patchFilesWithJson(path1, path2, file):
    data = readBinaryFromPath(path1)

    patch_info = readJsonAtPath(file)

    for offset in patch_info:
        old = patch_info[offset]['old']
        new = patch_info[offset]['new']

        print(f'Patching at offset: {offset}')
        print(f'{old} -> {new}')

        patchBufferAtIndex(data, offset, old, new)

    writeBinaryToPath(path2, data)
