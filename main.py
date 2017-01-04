import sys

import matplotlib.pyplot as plt
from numpy import *
from scipy import *
from scipy.io import wavfile

def recognize_gender(file):
    print(file)

    # czestotliwosc, wartosci probek
    w, signal = wavfile.read(file)
    # 1 kanal
    if isinstance(signal[0], list):
        signal = [s[0] for s in signal]
    # licza probek
    n = len(signal)

    # wyliczanie czestotliwosci sygnalu
    fftSig = fft(signal)
    drawfftSig = abs(fftSig)

    # odciecie prawej symetrycznej strony
    drawfftSig = drawfftSig[0:len(fftSig)//2]

    # wyliczenie x
    freqs = linspace(0, w, n)
    freqs = freqs[0:len(fftSig)//2]


    # wyrysowanie wykresow
    fig = plt.figure(figsize=(15, 6), dpi=80)
    ax = fig.add_subplot(211)
    ax.plot(signal, 'o')

    ax = fig.add_subplot(212)
    ax.set_ylim([0.0, 1.1 * max(drawfftSig) * 2 / n])

    # zmniejszenie ilosci rysowanych probek
    drawDiv = 25
    plt.stem(freqs[::drawDiv], (drawfftSig[::drawDiv] * 2) / n, '-*')

    plt.show()

def main():
    print(sys.argv)
    recognize_gender("resources/003_K.wav")

if __name__ == "__main__":
    main()
