import matplotlib.pyplot as plt
from scipy import *
from scipy.io import wavfile

import sys


def recognize_gender(file, freqFilter=1):
    print(file)

    # czestotliwosc, wartosci probek
    w, signal = wavfile.read(file)
    # 1 kanal
    if isinstance(signal[0], ndarray):
        signal = [s[0] for s in signal]

    # uprosc sygnal dla szybszych obliczen
    signal = signal[::freqFilter]

    # wyliczanie czestotliwosci sygnalu
    fftSig = fft(signal)
    drawfftSig = abs(fftSig)

    # odciecie prawej symetrycznej strony
    drawfftSig = drawfftSig[0:len(fftSig) // 2]

    # licza probek
    n = len(signal)

    # wyliczenie x
    freqs = linspace(0, w, n)
    freqs = freqs[0:len(fftSig) // 2]

    # wyrysowanie wykresow
    fig = plt.figure(figsize=(15, 6), dpi=80)
    ax = fig.add_subplot(211)
    ax.plot(signal, 'o')

    ax = fig.add_subplot(212)
    ax.set_ylim([0.0, 1.1 * max(drawfftSig) * 2 / n])

    # zmniejszenie ilosci rysowanych probek
    drawFirst = int(n / 10)
    drawDiv = 5
    # plt.stem(freqs[:drawFirst:drawDiv], (drawfftSig[:drawFirst:drawDiv] * 2) / n, '-*')

    print(frequencyCheck(drawfftSig, freqs))

    # plt.show()


def frequencyCheck(signal, freqs, freqCheckVal=118, mainFreqFealeVeto=180, checkFreqs=500):
    order = sorted(arange(len(signal)), key=lambda i: signal[i])[-checkFreqs:]
    freqsToCheck = [freqs[i] for i in order[::-1]]
    # print(freqsToCheck)

    mainFreq, diff = findMainFreq(freqsToCheck)

    if diff < freqCheckVal:
        if mainFreq > mainFreqFealeVeto:
            return "K"
        return "M"
    else:
        return "K"


def findMainFreq(freqs, sd=55):
    main = {freqs[0]: 0}
    # dla kazdego elementu na liscie
    for i in range(1, len(freqs)):
        # jezeli jest w main jako key dodaj 1 do count
        inMain = False
        for key, count in main.items():
            if abs(freqs[i] - key) < sd:
                main[key] = count + 1
                inMain = True
                break

        # jezeli nie bylo w main jako key dodaj
        if inMain == False:
            main[freqs[i]] = 0

    main = dict((key, val) for key, val in main.items() if val != 0)
    # print(main)

    mainFreq, diff = calculateDiff(main)
    print(mainFreq, diff)
    return mainFreq, diff


def calculateDiff(dict):
    sum, count = 0, 0
    keys = list(dict.keys())
    vals = list(dict.values())
    order = sorted(arange(len(keys)), key=lambda i: keys[i])

    # for i in order:
    #     print(keys[i], vals[i])

    for i in range(len(order) - 1):
        diff = abs(keys[order[i]] - keys[order[i + 1]])
        sum += diff * (vals[order[i]] + vals[order[i + 1]])
        count += (vals[order[i]] + vals[order[i + 1]])

    return min(keys), (sum / count)


def main():
    files = sys.argv[1:]
    for i in files:
        recognize_gender(i)

    if(len(files) > 0):
        return

    # tests
    files = ["resources/002_M.wav", "resources/003_K.wav", "resources/004_M.wav", "resources/005_M.wav",
             "resources/006_K.wav", "resources/007_M.wav", "resources/008_K.wav", "resources/009_K.wav",
             "resources/010_M.wav", "resources/011_M.wav"]

    files2 = ["resources/012_K.wav", "resources/013_M.wav", "resources/014_K.wav", "resources/015_K.wav",
              "resources/016_K.wav", "resources/017_M.wav", "resources/018_K.wav", "resources/019_M.wav",
              "resources/020_M.wav", "resources/021_M.wav"]

    for i in files2:
        recognize_gender(i)


if __name__ == "__main__":
    main()
