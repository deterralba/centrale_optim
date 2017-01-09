import numpy as np
from solver import get_domaines


def test_get_domaines():
    inp = np.array([[1,3],
                    [1, 3]],
                   dtype=np.int32)
    res = [[{1, 2, 4, 8}, {3, 6, 9, 12}],
           [{1, 2, 4, 8}, {3, 6, 9, 12}]]
    assert get_domaines(inp) == res
