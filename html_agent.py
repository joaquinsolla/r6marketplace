import json
from datetime import datetime


def data_to_html():
    with open('assets/data.json', 'r') as f:
        json_data = json.load(f)

    now = datetime.now()
    now_formatted = now.strftime('%d/%m/%Y %H:%M')

    with open('assets/data.html', 'w') as data_html:
        data_html.write('<!DOCTYPE html>\n')
        data_html.write('<html>\n')
        data_html.write('<head>\n')
        data_html.write('<title>Items</title>\n')
        data_html.write('<style>\n')
        data_html.write('table {\n')
        data_html.write('    width: 100%;\n')
        data_html.write('    border-collapse: collapse;\n')
        data_html.write('}\n')
        data_html.write('table, th, td {\n')
        data_html.write('    border: 1px solid black;\n')
        data_html.write('    padding: 8px;\n')
        data_html.write('    text-align: center;\n')
        data_html.write('}\n')
        data_html.write('button {\n')
        data_html.write('    background-color: transparent;\n')
        data_html.write('    border: none;\n')
        data_html.write('    font-size: inherit;\n')
        data_html.write('    font-weight: bold;\n')
        data_html.write('    text-decoration: underline;\n')
        data_html.write('}\n')
        data_html.write('</style>\n')
        data_html.write('<script>\n')
        data_html.write('function ordenarTabla(colIndex) {\n')
        data_html.write('  var table, rows, switching, i, x, y, shouldSwitch, asc, switchcount = 0;\n')
        data_html.write('  table = document.getElementById("tablaItems");\n')
        data_html.write('  switching = true;\n')
        data_html.write('  asc = true;\n')
        data_html.write('  while (switching) {\n')
        data_html.write('    switching = false;\n')
        data_html.write('    rows = table.rows;\n')
        data_html.write('    for (i = 1; i < (rows.length - 1); i++) {\n')
        data_html.write('      shouldSwitch = false;\n')
        data_html.write('      x = rows[i].getElementsByTagName("td")[colIndex];\n')
        data_html.write('      y = rows[i + 1].getElementsByTagName("td")[colIndex];\n')
        data_html.write('      var xValue = isNaN(x.innerHTML) ? x.innerHTML.toLowerCase() : Number(x.innerHTML);\n')
        data_html.write('      var yValue = isNaN(y.innerHTML) ? y.innerHTML.toLowerCase() : Number(y.innerHTML);\n')
        data_html.write('      if (asc) {\n')
        data_html.write('        if (xValue > yValue) {\n')
        data_html.write('          shouldSwitch= true;\n')
        data_html.write('          break;\n')
        data_html.write('        }\n')
        data_html.write('      } else {\n')
        data_html.write('        if (xValue < yValue) {\n')
        data_html.write('          shouldSwitch= true;\n')
        data_html.write('          break;\n')
        data_html.write('        }\n')
        data_html.write('      }\n')
        data_html.write('    }\n')
        data_html.write('    if (shouldSwitch) {\n')
        data_html.write('      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);\n')
        data_html.write('      switching = true;\n')
        data_html.write('      switchcount ++;\n')
        data_html.write('    } else {\n')
        data_html.write('      if (switchcount == 0 && asc) {\n')
        data_html.write('        asc = false;\n')
        data_html.write('        switching = true;\n')
        data_html.write('      }\n')
        data_html.write('    }\n')
        data_html.write('  }\n')
        data_html.write('}\n')
        data_html.write('</script>\n')
        data_html.write('</head>\n')
        data_html.write('<body style="font-family: Arial, sans-serif;">\n')
        data_html.write('<h1>R6 Marketplace data.</h1>\n')
        data_html.write('<h2>Updated: ' + now_formatted +'</h2>\n')
        data_html.write('<table id="tablaItems">\n')
        data_html.write('<tr>\n')
        data_html.write('<th><button onclick="ordenarTabla(0)">Item</button></th>\n')
        data_html.write('<th>URL</th>\n')
        data_html.write('<th>Image</th>\n')
        data_html.write('<th><button onclick="ordenarTabla(3)">Avg Price</button></th>\n')
        data_html.write('<th><button onclick="ordenarTabla(4)">Lowest Seller</button></th>\n')
        data_html.write('<th><button onclick="ordenarTabla(5)">ROI</button></th>\n')
        data_html.write('<th><button onclick="ordenarTabla(6)">Highest Seller</button></th>\n')
        data_html.write('<th><button onclick="ordenarTabla(7)">Lowest Buyer</button></th>\n')
        data_html.write('<th><button onclick="ordenarTabla(8)">Highest Buyer</button></th>\n')
        data_html.write('<th><button onclick="ordenarTabla(9)">Sellers</button></th>\n')
        data_html.write('<th><button onclick="ordenarTabla(10)">Buyers</button></th>\n')
        data_html.write('<th><button onclick="ordenarTabla(11)">Last Sold</button></th>\n')
        data_html.write('<th><button onclick="ordenarTabla(12)">Updated</button></th>\n')
        data_html.write('<th>Sales Plot</th>\n')
        data_html.write('</tr>\n')

        for item_id, item_data in json_data.items():
            updated_formatted = datetime.fromtimestamp(item_data["updated"]).strftime("%d/%m/%Y %H:%M")

            data_html.write('<tr>\n')
            data_html.write(f'<td style="text-align: left">{item_data["id-name"].upper()}</td>\n')
            data_html.write(f'<td><a href="{item_data["url"]}" target="_blank">URL</a></td>\n')
            data_html.write(f'<td><img src="{item_data["asset-url"]}" alt="Image" height="100px" onclick="window.open(\'{item_data["asset-url"]}\', \'_blank\');"></td>\n')
            data_html.write(f'<td>{item_data["data"]["avg-price"]}</td>\n')
            data_html.write(f'<td style="font-weight: bold">{item_data["data"]["lowest-seller"]}</td>\n')
            data_html.write(f'<td>{item_data["data"]["roi"]}</td>\n')
            data_html.write(f'<td>{item_data["data"]["highest-seller"]}</td>\n')
            data_html.write(f'<td>{item_data["data"]["lowest-buyer"]}</td>\n')
            data_html.write(f'<td>{item_data["data"]["highest-buyer"]}</td>\n')
            data_html.write(f'<td>{item_data["data"]["sellers"]}</td>\n')
            data_html.write(f'<td>{item_data["data"]["buyers"]}</td>\n')
            data_html.write(f'<td>{item_data["data"]["last-sold"]}</td>\n')
            data_html.write(f'<td>{updated_formatted}</td>\n')
            if item_data["sales-plot-path"] == "No data":
                data_html.write(f'<td>{item_data["sales-plot"]}</td>\n')
            else:
                sales_plot_path = item_data["sales-plot-path"].replace("assets/", "")
                data_html.write(f'<td><img src="{sales_plot_path}" alt="Sales" height="100px" onclick="window.open(\'{sales_plot_path}\', \'_blank\');"></td>\n')
            data_html.write('</tr>\n')

        data_html.write('</table>\n')
        data_html.write('</body>\n')
        data_html.write('</html>\n')

    data_html.close()
    print("[ HTML built: assets/data.html ]")

#data_to_html()
