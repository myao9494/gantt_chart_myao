# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: JavaScript
#     language: javascript
#     name: jslab
# ---

var li_a = [];

var list_yotei =[
    [48,"部活",new Date(2022,6,9),3,222222],
    [48,"部活",new Date(2022,6,18),1,222222],
    [48,"終業式",new Date(2022,6,20),1,222222],
    [15,"音楽会",new Date(2022,6,24),1,222222],
    [66,"排水管掃除",new Date(2022,6,16),1,222222],
    [15,"python研修",new Date(2022,6,13),3,222222],
]


for (const element of list_yotei) {
   console.log(new Date((element[2])));
}

new Date("2022-07-17T15:00:00.000Z")

# +
var li, out_li;
li = ["ss", "ssss"];
out_li = [];

for (var i, _pj_c = 0, _pj_a = list_yotei, _pj_b = _pj_a.length; _pj_c < _pj_b; _pj_c += 1) {
    i = _pj_a[_pj_c];
    out_li.push(i)
    
//     out_li.
//   out_li.append(i);
}

# -

out_li

date.setDate( date.getDate() + 1);

