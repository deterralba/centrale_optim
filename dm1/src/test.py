import numpy as np
from solver import get_domains, is_compatible, _valid_shape


def test_get_domains():
    inp = np.array([[1,3],
                    [1, 3]],
                   dtype=np.int32)
    res = [[{1, 2, 4, 8}, {3, 6, 9, 12}],
           [{1, 2, 4, 8}, {3, 6, 9, 12}]]
    assert get_domains(inp) == res

def test__valid_shape():
    #(original_shape, direction_original, shape, direction_shape)
    assert _valid_shape(1, 'down', 1, 'up') is False
    assert _valid_shape(8, 'right', 8, 'left') is False

    assert _valid_shape(8, 'right', 2, 'left') is True

def test_is_compatible():
    # (square, original_square, shape, original_square)
    assert is_compatible( (0,1), (0,0), 2, {8}) is True
    assert is_compatible( (0,1), (0,0), 4, {5, 1}) is True
    assert is_compatible( (0,1), (0,0), 2, {8}) is True

    assert is_compatible( (0,1), (0,0), 4, {15}) is False
    assert is_compatible( (0,1), (0,0), 0, {15}) is False
    assert is_compatible( (0,1), (0,0), 8, {8}) is False

