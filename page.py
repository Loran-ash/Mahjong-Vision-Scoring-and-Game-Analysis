import gradio as gr
from yolo_classify import predict_tile_labels, analyze_tile_string
from real_time_prediction import detection

global last_result
last_result = "" 

with gr.Blocks() as demo:
    gr.Markdown("# 🀄️ 臺灣麻將向聽計算器")

    gr.Markdown("## 步驟 1：上傳圖片辨識牌組")
    with gr.Row():
        image_input = gr.Image(type="pil", label="📷 上傳含17張牌的圖片")
    submit_btn = gr.Button("🔍 分析圖片 → 產生牌組")

    gr.Markdown("## 步驟 2：確認或修改牌組")
    with gr.Column():
        gr.Image(value="intro.png", label="🧾 牌名格式說明", show_label=True, interactive=False, elem_id="tile-guide")
        text_output = gr.Label(label="模型辨識結果")
        tile_output = gr.Textbox(label="🧾 可編輯牌組（如 1m,2m,3p...）", lines=2, elem_id="output-box")

    stream = gr.Image(sources="webcam", streaming=True)
    stream.stream(fn=detection, inputs=[stream, text_output], outputs=[stream, text_output])


    analyze_btn = gr.Button("📏 分析此牌組 → 向聽與建議")
    result_box = gr.Textbox(label="📋 向聽結果與建議", lines=12, elem_id="output-box")

    # 事件綁定
    submit_btn.click(fn=predict_tile_labels, inputs=image_input, outputs=tile_output)
    analyze_btn.click(fn=analyze_tile_string, inputs=tile_output, outputs=result_box)

    # 自定義 CSS（控制圖片寬度）
    demo.css = """
    #tile-guide img {
        max-width: 400px;
        margin: auto;
        display: block;
    }

    #output-box textarea {
        font-size: 24px !important;
        line-height: 1.6;
        font-family: "Noto Sans TC", sans-serif;
    }
    """


demo.launch()
