"""
This code is to do the Principal Component Analysis.

Do the standardization.
Find eigenvalues and eigenvectors of the covariance matrix.
Transform matrix.
Calculate the contribution ratio.
Plot data.
"""

import argparse
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import ArrayLike


def parse_args() -> Any:
    """
    Get Arguments.

    Returns
    -------
    parser.parse_args() : 引数を返す
    """
    parser = argparse.ArgumentParser(description="最小二乗法を用いて回帰分析を行う。")
    parser.add_argument(
        "-file",
        help="ファイルを入力",
        default=r"C:\Users\kyskn\B4Lecture-2024\ex4\data2.csv",
        type=str,
    )
    return parser.parse_args()


class PrincipalComponentAnalysis:
    """PrincipalComponentAnalysis."""

    def __init__(self, file_path: str) -> None:
        """Make self."""
        self.file_path = file_path
        self.data = None
        self.st_data = None
        self.cov_data = None
        self.eig_data = None
        self.Eigenvalues = None
        self.Eigenvectors = None
        self.Y = None
        self.rate = None

    def standardization(self, data: ArrayLike) -> ArrayLike:
        """
        Do the standardization.

        Parameters
        ----------
        data (ArrayLike): データ

        Returns
        -------
        st_data (ArrayLike): 標準化データ
        """
        st_data = (data - np.mean(data, axis=0)) / np.std(data, axis=0)
        return st_data

    def transformation_matrix(self, data: ArrayLike) -> ArrayLike:
        """
        Transform matrix.

        Parameters
        ----------
        data (ArrayLike): データ
        Eigenvectors (ArrayLike): 固有ベクトル

        Returns
        -------
        Y (ArrayLike): 変換後のデータ
        """
        Y = self.Eigenvectors.T @ data.T
        return Y.T

    def cul_rate(self) -> ArrayLike:
        """
        Calculate the contribution ratio.

        Parameters
        ----------
        Eigenvalues (ArrayLike): 固有ベクトル

        Returns
        -------
        sorted_rate (ArrayLike): 大きい順の寄与率
        """
        rate = self.Eigenvalues / sum(self.Eigenvalues)
        sorted_rate = np.sort(rate)[::-1]
        return sorted_rate

    def compression(self) -> ArrayLike:
        """
        Compress the dimension to a cumulative contribution ratio of 90%.

        Parameters
        ----------
        rate (ArrayLike): 寄与率

        Returns
        -------
        cum_rate (ArrayLike): 累積寄与率
        """
        ac_rate = 0.0
        i = 0
        cum_rate = []
        while ac_rate < 0.9:
            ac_rate += self.rate[i]
            cum_rate.append(ac_rate)
            i += 1
        return cum_rate

    def load_data(self) -> None:
        """Load data."""
        self.data = np.loadtxt(self.file_path, delimiter=",", dtype="float")

    def pca(self) -> None:
        """Do all pca."""
        self.st_data = self.standardization(self.data)
        self.cov_data = np.cov(self.st_data, rowvar=0, bias=1)
        self.eig_data = np.linalg.eig(self.cov_data)
        self.Eigenvalues = self.eig_data[0]
        self.Eigenvectors = self.eig_data[1]
        self.Y = self.transformation_matrix(self.data)
        self.rate = self.cul_rate()

    def plot2d(self) -> None:
        """
        Plot in 2 dimensions.

        Parameters
        ----------
        data (array-like): データ
        Eigenvectors (array-like): 固有ベクトル
        rate (array-like): 寄与率
        """
        fig, ax = plt.subplots()
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.scatter(
            self.data[:, 0], self.data[:, 1], self.data[:, 2], color="b", label="data2"
        )

        vec1 = self.Eigenvectors.T[0]
        ax.plot(
            [-2 * vec1[0], 2 * vec1[0]],
            [-2 * vec1[1], 2 * vec1[1]],
            color="red",
            label=round(self.rate[0], 2),
        )
        vec2 = self.Eigenvectors.T[1]
        ax.plot(
            [-2 * vec2[0], 2 * vec2[0]],
            [-2 * vec2[1], 2 * vec2[1]],
            color="green",
            label=round(self.rate[1], 2),
        )
        ax.legend()
        plt.show()

    def plot3d(self) -> None:
        """
        Plot in 3 dimensions.

        Parameters
        ----------
        data (array-like): データ
        Eigenvectors (array-like): 固有ベクトル
        rate (array-like): 寄与率
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(
            self.data[:, 0], self.data[:, 1], self.data[:, 2], color="b", label="data2"
        )

        vec1 = self.Eigenvectors.T[0]
        ax.plot(
            [-2 * vec1[0], 2 * vec1[0]],
            [-2 * vec1[1], 2 * vec1[1]],
            [-2 * vec1[2], 2 * vec1[2]],
            color="r",
            label=round(self.rate[0], 2),
        )
        vec2 = self.Eigenvectors.T[1]
        ax.plot(
            [-2 * vec2[0], 2 * vec2[0]],
            [-2 * vec2[1], 2 * vec2[1]],
            [-2 * vec2[2], 2 * vec2[2]],
            color="g",
            label=round(self.rate[1], 2),
        )
        vec3 = self.Eigenvectors.T[2]
        ax.plot(
            [-2 * vec3[0], 2 * vec3[0]],
            [-2 * vec3[1], 2 * vec3[1]],
            [-2 * vec3[2], 2 * vec3[2]],
            color="y",
            label=round(self.rate[2], 2),
        )
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.legend()
        plt.show()

    def plot_comp(self) -> None:
        """
        Plot the data after compression.

        Parameters
        ----------
        Y (array-like): 変換後のデータ
        """
        fig, ax = plt.subplots()
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.scatter(self.Y[:, 0], self.Y[:, 1], color="b", label="compression data")
        ax.legend()
        plt.show()


def main() -> None:
    """Do the Principal Component Analysis."""
    args = parse_args()
    pca = PrincipalComponentAnalysis(args.file)
    pca.load_data()
    pca.pca()
    if len(pca.data[0]) == 2:
        pca.plot2d()
    elif len(pca.data[0]) == 3:
        pca.plot3d()
        pca.plot_comp()
    else:
        cum_rate = pca.compression()
        print("Contribution rate", pca.rate)
        print("Cumulative contribution rate", cum_rate)
        print("Original:", len(pca.Y[0]), "Compressed:", len(cum_rate))


if __name__ == "__main__":
    main()
