import json

import streamlit as st
import streamlit.components.v1 as components

from bst import BinarySearchTree, Insertion, Node, parse_sequence


DEFAULT_SEQUENCE = "8, 3, 10, 1, 6, 14, 4, 7, 13"

st.set_page_config(page_title="Binary Search Tree 演示", page_icon="🌳", layout="wide")
st.title("🌳 Binary Search Tree 數字落點演示")
st.write("輸入自訂整數序列，觀察每個數字依照比較結果落入 BST 的位置。")

if "sequence_text" not in st.session_state:
    st.session_state.sequence_text = DEFAULT_SEQUENCE

with st.form("sequence_form"):
    st.text_input(
        "整數序列（以逗號或空格分隔）",
        key="sequence_text",
        help="例如：8, 3, 10, 1, 6。重複數字會放在相等節點的右側。",
    )
    submitted = st.form_submit_button("建立並播放")

duration = st.slider(
    "動畫速度（每段移動秒數）",
    min_value=0.2,
    max_value=1.2,
    value=0.45,
    step=0.05,
)

try:
    values = parse_sequence(st.session_state.sequence_text)
except ValueError as error:
    st.error(str(error))
    st.stop()

tree = BinarySearchTree()
for value in values:
    tree.insert(value)


def describe_position(insertion: Insertion) -> str:
    if insertion.node.parent is None:
        return "根節點"
    direction = "左" if insertion.node.parent.left is insertion.node else "右"
    return f"{insertion.node.parent.value} 的{direction}子節點"


def create_animation_html(
    insertions: list[Insertion], ordered_nodes: list[Node], seconds_per_hop: float
) -> str:
    node_count = len(ordered_nodes)
    width = max(760, 120 + (node_count - 1) * 100)
    positions: dict[int, tuple[int, int]] = {}
    for rank, node in enumerate(ordered_nodes):
        positions[node.index] = (60 + rank * 100, 70 + node.depth * 100)
    height = max(180, max(y for _, y in positions.values()) + 90)

    nodes_data = [
        {
            "id": node.index,
            "value": node.value,
            "parent": node.parent.index if node.parent is not None else None,
            "x": positions[node.index][0],
            "y": positions[node.index][1],
        }
        for node in ordered_nodes
    ]
    steps_data = [
        {
            "value": insertion.value,
            "node": insertion.node.index,
            "route": [node.index for node in insertion.route],
        }
        for insertion in insertions
    ]
    payload = json.dumps(
        {
            "nodes": nodes_data,
            "steps": steps_data,
            "width": width,
            "height": height,
            "duration": int(seconds_per_hop * 1000),
        }
    ).replace("</", "<\\/")

    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; color: #1f2937; font: 15px system-ui, sans-serif; }}
  #status {{ min-height: 28px; margin: 0 0 8px; font-weight: 600; color: #166534; }}
  #viewport {{ overflow-x: auto; border: 1px solid #e5e7eb; border-radius: 12px; background: #f9fafb; }}
  svg {{ display: block; }}
  .edge {{ stroke: #94a3b8; stroke-width: 3; }}
  .node circle {{ fill: #dbeafe; stroke: #2563eb; stroke-width: 3; }}
  .node.root circle {{ fill: #dcfce7; stroke: #16a34a; }}
  .node text {{ fill: #111827; font-size: 17px; font-weight: 700; text-anchor: middle; dominant-baseline: central; }}
  .token circle {{ fill: #f97316; stroke: #c2410c; stroke-width: 2; }}
  .token text {{ fill: white; font-size: 16px; font-weight: 700; text-anchor: middle; dominant-baseline: central; }}
</style>
</head>
<body>
<div id="status" role="status">準備開始…</div>
<div id="viewport"><svg id="tree" aria-label="二元搜尋樹數字落點動畫"></svg></div>
<script>
const data = {payload};
const svg = document.getElementById("tree");
const status = document.getElementById("status");
const ns = "http://www.w3.org/2000/svg";
svg.setAttribute("width", data.width);
svg.setAttribute("height", data.height);
svg.setAttribute("viewBox", `0 0 ${{data.width}} ${{data.height}}`);
const nodes = new Map(data.nodes.map(node => [node.id, node]));
const shown = new Set();

function element(name, attributes) {{
  const item = document.createElementNS(ns, name);
  for (const [key, value] of Object.entries(attributes)) item.setAttribute(key, value);
  return item;
}}

function showNode(node) {{
  if (shown.has(node.id)) return;
  if (node.parent !== null) {{
    const parent = nodes.get(node.parent);
    svg.appendChild(element("line", {{
      x1: parent.x, y1: parent.y, x2: node.x, y2: node.y, class: "edge"
    }}));
  }}
  const group = element("g", {{
    class: `node${{node.parent === null ? " root" : ""}}`,
    transform: `translate(${{node.x}} ${{node.y}})`
  }});
  group.appendChild(element("circle", {{r: 25}}));
  const label = element("text", {{y: 1}});
  label.textContent = node.value;
  group.appendChild(label);
  svg.appendChild(group);
  shown.add(node.id);
}}

function moveToken(token, from, to) {{
  return new Promise(resolve => {{
    const start = performance.now();
    function frame(now) {{
      const progress = Math.min(1, (now - start) / data.duration);
      const eased = progress * progress * (3 - 2 * progress);
      token.setAttribute("transform",
        `translate(${{from.x + (to.x - from.x) * eased}} ${{from.y + (to.y - from.y) * eased}})`);
      if (progress < 1) requestAnimationFrame(frame);
      else resolve();
    }}
    requestAnimationFrame(frame);
  }});
}}

async function play() {{
  for (let index = 0; index < data.steps.length; index++) {{
    const step = data.steps[index];
    const route = step.route.map(id => nodes.get(id));
    const path = route.map(node => node.value).join(" → ");
    status.textContent = `正在落下 ${{step.value}}（${{index + 1}}/${{data.steps.length}}）：${{path}}`;
    const token = element("g", {{class: "token"}});
    token.appendChild(element("circle", {{r: 21}}));
    const label = element("text", {{y: 1}});
    label.textContent = step.value;
    token.appendChild(label);
    svg.appendChild(token);

    const points = [{{x: route[0].x, y: 18}}, ...route];
    for (let hop = 0; hop < points.length - 1; hop++) {{
      await moveToken(token, points[hop], points[hop + 1]);
    }}
    token.remove();
    showNode(nodes.get(step.node));
    await new Promise(resolve => setTimeout(resolve, 140));
  }}
  status.textContent = `完成！共插入 ${{data.steps.length}} 個數字。`;
}}
play();
</script>
</body>
</html>"""


st.subheader("數字落下過程")
components.html(
    create_animation_html(tree.insertions, tree.nodes_in_order(), duration),
    height=max(280, min(750, 180 + max(node.depth for node in tree.nodes_in_order()) * 100)),
    scrolling=True,
)

st.subheader("每個數字最後落點")
st.caption("比較規則：較小的數字往左；大於或等於節點的數字往右。")
rows = []
for insertion in tree.insertions:
    route = " → ".join(str(node.value) for node in insertion.route)
    rows.append(
        f"| {insertion.value} | {route} | {describe_position(insertion)} | "
        f"{insertion.node.depth} |"
    )
st.markdown(
    "| 插入數字 | 經過的節點 | 最後落點 | 深度 |\n"
    "|---:|---|---|---:|\n"
    + "\n".join(rows)
)

if submitted:
    st.toast("BST 已建立，動畫已重新播放。")
