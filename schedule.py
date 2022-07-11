# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import re
import utility
import pandas as pd

# スケジュールのjsを読み込み

# +
with open(r"public/schedule.js") as f:
    li = f.readlines()

header = ['\n', '// 予定\n', '\n', 'var list_yotei =[\n']

footer = [ '\n',']\n']

naka_header = "    ["
naka_footer = "],\n"

naka = li[4:]
naka = naka[:-2]

out = []
for tex in naka:
    search_result = re.findall(r'(?<=\[).+?(?=\])', tex)
    tex = search_result[0]
    id_num = tex.split(",")[0]
    naiyo = re.findall(r'(?<=\").+?(?=\")', tex)[0]
    nitiji = re.findall(r'(?<=new Date\().+?(?=\))', tex)[0]
    nitiji = nitiji.replace(",","-")
    nitiji = utility.translate_js_date(nitiji,js_opp=False)
    nisu = tex.split(",")[-2]
    biko = tex.split(",")[-1]
    out.append([id_num,naiyo,nitiji,nisu,biko])

df = pd.DataFrame(out,columns=["id_num","名称","年月日","日数","備考"])
# -

# スケジュールをdfに追加したらり、編集したりする



# 元に戻す

# +
df["年月日"] = df["年月日"].apply(utility.translate_js_date)

df["out"] = naka_header + df["id_num"] +',"' + df["名称"] + '", new Date(' + df["年月日"].str.replace("-",",")  + ') ,' + df["日数"] + "," + \
                        df["備考"] + naka_footer

out_list = header + list(df["out"]) + footer
# out_list

with open(r"public/test.js", 'w') as f:
    for d in out_list:
        f.write("%s" % d)
# -


