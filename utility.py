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

def translate_js_date(input_date,js_opp=True):
    if js_opp:
        n = -1
    else:
        n = 1
    li = input_date.split("-")
    month = '{:0=2}'.format(int(li[1])+n)
    return  f"{li[0]}-{month}-{li[2]}"


