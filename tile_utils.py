# 所有牌的名稱對應：萬、筒、索、字牌
tile_names = [
    ['1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m'],
    ['1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p'],
    ['1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s'],
    ['1z', '2z', '3z', '4z', '5z', '6z', '7z'],
]

# 建立 tile 名稱到位置的反查對應
tile_to_index = {
    name: (i, j)
    for i, suit in enumerate(tile_names)
    for j, name in enumerate(suit)
}

def tiles_to_hand(tiles_arr):
    """
    將 ['1m', '2m', '3p', ...] 轉為四個花色的 2D array 表示法
    :param tiles_arr: List[str]
    :return: List[List[int]] (4 個 list 對應萬/筒/索/字)
    """
    hand = [
        [0] * 9,  # 萬
        [0] * 9,  # 筒
        [0] * 9,  # 索
        [0] * 7   # 字
    ]
    for tile in tiles_arr:
        if tile not in tile_to_index:
            raise ValueError(f"Invalid tile: {tile}")
        i, j = tile_to_index[tile]
        hand[i][j] += 1
    return hand

def check_hand(hand):
    """
    驗證手牌合法性，並回傳手牌狀態："To draw" 或 "To play"
    適用 Taiwan 規則（最大 17 張）
    """
    flat = [count for suit in hand for count in suit]
    total = sum(flat)
    if total > 17 or total % 3 == 0:
        raise ValueError(f"Invalid hand length: {total} tiles")

    for i in range(4):
        for j in range(len(hand[i])):
            if hand[i][j] > 4:
                raise ValueError(f"Too many copies of {tile_names[i][j]}: {hand[i][j]}")

    return "To draw" if total % 3 == 1 else "To play"

def check_tile(tile_name):
    return any(tile_name in suit for suit in tile_names)
