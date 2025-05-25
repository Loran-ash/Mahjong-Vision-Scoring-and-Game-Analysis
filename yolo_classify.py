import os
import tempfile
from ultralytics import YOLO
from ukeire import calc_ukeire
from cal_shanten import cal_shanten_menzu
from tile_utils import tile_names, check_tile

model = YOLO("./trained_model/best.pt")


def classify_tiles(tile_labels):
    suits = {'m': [0]*9, 'p': [0]*9, 's': [0]*9, 'z': [0]*7}

    for label in tile_labels:
        if not check_tile(label):
            print(f"⚠️ 無效牌名: {label}")
            continue

        suit = label[-1]
        index = int(label[:-1]) - 1
        suits[suit][index] += 1

    return [suits['m'], suits['p'], suits['s'], suits['z']]



def convert_label(label):
    if label.startswith("character_"):
        return label.split("_")[1] + "m"
    elif label.startswith("circle_"):
        return label.split("_")[1] + "p"
    elif label.startswith("bamboo_"):
        return label.split("_")[1] + "s"
    map_z = {"east": "1z", "south": "2z", "west": "3z", "north": "4z",
             "white": "5z", "green": "6z", "red": "7z"}
    return map_z.get(label, label)


def predict_tile_labels(image):
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        image.save(tmp.name)
        image_path = tmp.name

    try:
        results = model.predict(source=image_path)
        tile_labels = []

        for r in results:
            if hasattr(r, "boxes") and r.boxes:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    label = model.names[cls_id]
                    tile_labels.append(convert_label(label))

        if len(tile_labels) != 17:
            return f"⚠️ 檢測牌數錯誤（辨識到 {len(tile_labels)} 張）: {tile_labels}"

        return ", ".join(tile_labels)

    finally:
        os.remove(image_path)


def analyze_tile_string(tile_str):
    tile_labels = [t.strip() for t in tile_str.split(",") if t.strip()]

    if len(tile_labels) != 17:
        return f"⚠️ 牌數錯誤：應該是 17 張，現在是 {len(tile_labels)} 張。"

    if any(not check_tile(t) for t in tile_labels):
        return f"⚠️ 包含無效牌名，請確認格式為 '1m, 2m, 3m, ..., 7z'"

    suits = classify_tiles(tile_labels)
    tile_count = sum(sum(suit) for suit in suits)
    if tile_count == 0:
        return "⚠️ 無法從輸入的文字建立合法的手牌，請檢查格式與拼字。"

    try:
        shanten = cal_shanten_menzu(suits)
        ukeire_result = calc_ukeire(suits)
    except Exception as e:
        return f"⚠️ 無法分析手牌：{e}"

    output = [f"📏 向聽數：{ukeire_result['shanten']} 向聽"]

    if 'ukeire' in ukeire_result:
        ukeire_lines = [f"🎯 有效進張：共 {ukeire_result['totalUkeire']} 張"]
        for tile, count in sorted(ukeire_result['ukeire'].items()):
            ukeire_lines.append(f"　- {tile} × {count}")
        output.extend(ukeire_lines)
    elif 'normalDiscard' in ukeire_result:
        output.append("🗑 建議打牌選擇：")
        for tile, uke in ukeire_result['normalDiscard'].items():
            uke_str = ", ".join(f"{k}×{v}" for k, v in uke.items())
            output.append(f"　- 打 {tile} → 有效牌: {uke_str}")

        if ukeire_result['recedingDiscard']:
            output.append("⚠️ 以下打牌會讓向聽變差：")
            for tile, uke in ukeire_result['recedingDiscard'].items():
                uke_str = ", ".join(f"{k}×{v}" for k, v in uke.items())
                output.append(f"　- 打 {tile} → 有效牌: {uke_str}")

    return "\n".join(output)
