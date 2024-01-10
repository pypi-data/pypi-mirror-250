import numpy as np


def batman(x):
    H = lambda x: np.heaviside(x, 0.5)
    sqrt = lambda x: np.sqrt(np.maximum(x, 0.0))

    w = 3 * sqrt(1 - (x / 7) ** 2)
    l = (  # noqa: E741
        0.5 * (x + 3) - 3 / 7 * sqrt(10 * (4 - (x + 1) ** 2)) + 6 / 7 * sqrt(10)
    )
    h = 0.5 * (
        3 * (np.abs(x + 0.5) + np.abs(x - 0.5) + 6)
        - 11 * (np.abs(x - 0.75) + np.abs(x + 0.75))
    )
    r = 0.5 * (3 - x) - 3 / 7 * sqrt(10 * (4 - (x - 1) ** 2)) + 6 / 7 * sqrt(10)

    upper = np.where(
        np.abs(x) > 7,
        np.nan,
        (
            (h - l) * H(x + 1)
            + (r - h) * H(x - 1)
            + (l - w) * H(x + 3)
            + (w - r) * H(x - 3)
            + w
        ),
    )
    lower = np.where(
        np.abs(x) > 7,
        np.nan,
        0.5
        * (
            np.abs(0.5 * x)
            + sqrt(1 - (np.abs(np.abs(x) - 2) - 1) ** 2)
            - (3 * sqrt(33) - 7) / 112 * x**2
            + 3 * sqrt(1 - (x / 7) ** 2)
            - 3
        )
        * (np.sign(x + 4) - np.sign(x - 4))
        - 3 * sqrt(1 - (x / 7) ** 2),
    )

    return upper, lower
