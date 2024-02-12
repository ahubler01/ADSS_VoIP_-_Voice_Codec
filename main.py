from random import randint
import numpy as np
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import pyaudio
import binascii  # Import binascii for converting data to hex


class Client(DatagramProtocol):
    def startProtocol(self):
        py_audio = pyaudio.PyAudio()
        self.buffer = 1024  # 127.0.0.1
        self.another_client = input("Write address: "), int(input("Write port: "))

        # Control whether to play received messages
        self.play_messages = False  # Default to not playing messages

        self.output_stream = py_audio.open(format=pyaudio.paInt16,
                                           output=True,
                                           rate=44100,
                                           channels=1,
                                           frames_per_buffer=self.buffer)

        self.input_stream = py_audio.open(format=pyaudio.paInt16,
                                          input=True,
                                          rate=44100,
                                          channels=1,
                                          frames_per_buffer=self.buffer)
        reactor.callInThread(self.record)

    def record(self):
        while True:
            data = self.input_stream.read(self.buffer)
            self.transport.write(data, self.another_client)
            # Convert the sent data to a hex representation and print it
            hex_data = binascii.hexlify(data).decode('utf-8')
            print(data)
            # print(hex_data)

            self.amplitude_values = np.frombuffer(data, dtype=np.int16)

            print(self.amplitude_values)
            print(type(self.amplitude_values))
            print(len(self.amplitude_values))


    def datagramReceived(self, datagram, addr):
        print(f"Received {len(datagram)} bytes from {addr}")
        if self.play_messages:
            self.output_stream.write(datagram)


if __name__ == '__main__':
    port = randint(1000, 3000)
    print("Working on port: ", port)

    reactor.listenUDP(port, Client())
    reactor.run()
