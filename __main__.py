import asyncio
from PySide2 import QtWidgets, QtGui

import server  # DON`T REMOVE

HOST = "localhost"
PORT = 8888
MAX_BYTES = 2048
MAX_CHUNKS = 256


async def get_picture():
    reader, writer = await asyncio.open_connection(HOST, PORT)
    chuncks = []
    count = 0
    while count < MAX_CHUNKS:
        writer.write(b"next")
        await writer.drain()
        chunk = await reader.read(MAX_BYTES)
        chuncks.append(chunk)
        if not chunk:
            break
        count += 1
    chuncks.sort()
    chuncks = [x[1:] for x in chuncks]
    return b"".join(chuncks)


def client():
    path_to_image = "picture"
    with open(path_to_image, "wb") as file:
        file.write(asyncio.run(get_picture()))
    return path_to_image


def main():
    path = client()
    app = QtWidgets.QApplication([])
    label = QtWidgets.QLabel()
    label.setMinimumSize(100, 100)
    label.setPixmap(QtGui.QPixmap(path))
    label.show()
    app.exec_()


if __name__ == '__main__':
    main()
