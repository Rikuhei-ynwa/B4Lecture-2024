"""
This code does the following.

Make the high pass filter.
Do the convolution.
Draw the spectrogram.
"""

import argparse

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import soundfile as sf


def convolution(inputs, filt):
    """
    Do the convolution.

    Parameters
    -------------
    inputs : 入力データ
    filt : filter

    Returns
    ------------
    output : 出力データ
    """
    # 畳み込みを行う
    outputs = np.zeros(len(inputs) + len(filt) - 1)
    # inputの配列の前後に0を追加。
    add = np.zeros(len(filt) - 1)
    inputs = np.concatenate((add, inputs))
    inputs = np.concatenate((inputs, add))
    # フィルタ配列を反転
    filt = filt[::-1]
    for i in range(len(outputs)):
        outputs[i] = np.dot(inputs[i : i + len(filt)], filt)
    return outputs


def hpf(fs, fc, N):
    """
    Make the high pass filter.

    Parameters
    ----------
    fs : サンプル周波数
    fc : カットオフ周波数
    N : 次数

    Returns
    -------
    filter : フィルター
    """
    # 一度ローパスフィルターを作るためfcを反対に
    fc = fs/2 - fc
    omega_c = 2.0 * np.pi * (fc / fs)
    window = signal.windows.hann(2 * N + 1)

    # 理想ハイパスフィルタを作成
    n = np.arange(1, N + 1)
    ideal_fil = np.zeros(2 * N + 1)
    # 理想ローパスフィルタを反転
    ideal_fil_half = np.cos(n * np.pi) * 2 * (fc / fs) * np.sin(omega_c * n) / (omega_c * n)
    ideal_fil[0:N] = ideal_fil_half[::-1]
    ideal_fil[N] = 2 * (fc / fs)
    ideal_fil[N + 1 : 2 * N + 1] = ideal_fil_half

    # 窓関数をかける
    filt = ideal_fil * window
    return filt


def main():
    """
    Make the high pass filter.

    Do the convolution.
    Draw the spectrogram.
    """
    parser = argparse.ArgumentParser(
        description="hpfをつくり、wavfileのdataと畳み込みして、スペクトログラムを描画する"
    )
    parser.add_argument(
        "-file",
        help="ファイルを入力",
        default=r"C:\Users\kyskn\B4Lecture-2024\ex2\k_namizaki\recoMono.wav",
    )
    parser.add_argument("-cut", help="カットオフ周波数", default=5000, type=int)
    parser.add_argument("-n", help="次数", default=64, type=int)
    args = parser.parse_args()

    # データを読み込み
    data, rate = sf.read(args.file)
    fc = args.cut
    N = args.n

    # filterの作成
    filt = hpf(rate, fc, N)

    # フィルタの振幅特性を計算
    mag = np.abs(np.fft.fft(filt, 1024))
    mag_db = 20 * np.log10(mag)
    # 周波数軸の計算
    freq_axis = np.linspace(0, rate, 1024)
    # フィルタの位相特性を計算(unwrapなしだと2pi分が毎回巻き戻されてしまう)
    phase = np.unwrap(np.angle(np.fft.fft(filt, 1024)))
    # 角度に変更
    phase = phase * 180 / np.pi

    # filterの振幅を描画
    plt.plot(freq_axis[: len(mag) // 2], mag_db[: len(mag) // 2])
    plt.title("high pass filter(amplitude)")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Amplitude [dB]")
    plt.show()
    # filterの位相を描画
    plt.plot(freq_axis[: len(mag) // 2], phase[: len(mag) // 2])
    plt.title("high pass filter(degree)")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Degree [°]")
    plt.show()

    # dataとhpfを畳み込み
    filteredData = convolution(data, filt)

    # 入力と出力の大きさをそろえる
    length = len(data)
    filteredData = filteredData[0:length]
    # フィルター前のスペクトログラム分析
    f, t, Sxx = signal.spectrogram(data, rate)

    # フィルター前のスペクトログラムの描画
    plt.pcolormesh(t, f, 10 * np.log(Sxx), shading="gouraud")
    plt.title("spectrogram(original)")
    plt.ylabel("Frequency [Hz]")
    plt.xlabel("Time [sec]")
    plt.colorbar()
    plt.show()

    # フィルター後のスペクトログラム分析
    f, t, Sxx = signal.spectrogram(filteredData, rate)

    # フィルター後のスペクトログラムの描画
    plt.pcolormesh(t, f, 10 * np.log(Sxx), shading="gouraud")
    plt.title("spectrogram(filtered)")
    plt.ylabel("Frequency [Hz]")
    plt.xlabel("Time [sec]")
    plt.colorbar()
    plt.show()


if __name__ == "__main__":
    main()
