import sys

import matplotlib.pyplot as plt
from numpy import *
from scipy import *
from scipy.io import wavfile
from skimage import measure


def recognize_gender(file, freqFilter=1):
    print(file)

    # czestotliwosc, wartosci probek
    w, signal = wavfile.read(file)
    # 1 kanal
    if isinstance(signal[0], ndarray):
        signal = [s[0] for s in signal]

    #uprosc sygnal dla szybszych obliczen
    signal = signal[::freqFilter]

    # wyliczanie czestotliwosci sygnalu
    fftSig = fft(signal)
    drawfftSig = abs(fftSig)

    # odciecie prawej symetrycznej strony
    drawfftSig = drawfftSig[0:len(fftSig)//2]

    # licza probek
    n = len(signal)

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
    drawFirst = int(n/10)
    drawDiv = 5
    # plt.stem(freqs[:drawFirst:drawDiv], (drawfftSig[:drawFirst:drawDiv] * 2) / n, '-*')

    print(frequencyCheck(drawfftSig, freqs))

    # plt.show()


def frequencyCheck(signal, freqs, maleMin=0, maleMax=180, femaleMin=165, femaleMax=500, diffSD=100, checkFreqs=300):
    order = sorted(arange(len(signal)), key = lambda i : signal[i])[-checkFreqs:]
    freqsToCheck = [freqs[i] for i in order[::-1]]
    # print(freqsToCheck)

    mainFreq, diff = findMainFreq(freqsToCheck)
    if mainFreq < maleMax and mainFreq > femaleMin:
        if diff < diffSD :
            return "M"
        else:
            return "K"
    if mainFreq > maleMin and mainFreq < maleMax:
        return "M"
    if mainFreq > femaleMin and mainFreq < femaleMax:
        return "K"

    return "IDK"

def findMainFreq(freqs, sd=55):
    main = {freqs[0] : 0}
    # dla kazdego elementu na liscie
    for i in range(1, len(freqs)):
        # jezeli jest w main jako key dodaj 1 do count
        inMain = False
        for key, count in main.items():
            if abs(freqs[i] - key) < sd :
                main[key] = count + 1
                inMain = True
                break

        # jezeli nie bylo w main jako key dodaj
        if inMain == False :
            main[freqs[i]] = 0

    main = dict((key, val) for key, val in main.items() if val != 0)
    # print(main)

    mainFreq, diff = calculateDiff(main)
    print(mainFreq, diff)
    return mainFreq, diff

def calculateDiff(dict, outlierFilter=100):
    sum, count = 0, 0
    keys = list(dict.keys())
    vals = list(dict.values())
    order = sorted(arange(len(keys)), key=lambda i: keys[i])

    for i in order:
        print(keys[i], vals[i])

    for i in range(len(order) - 1):
        diff = abs(keys[order[i]] - keys[order[i+1]])
        sum += diff * (vals[order[i]] + vals[order[i+1]])
        count += (vals[order[i]] + vals[order[i+1]])

    return (sum / count) + min(keys), (sum/count)

def main():
    print(sys.argv)
    recognize_gender("resources/010_M.wav", freqFilter=1)

if __name__ == "__main__":
    main()
