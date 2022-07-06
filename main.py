import json
import webbrowser
import xml.etree.ElementTree as ET
from io import BytesIO
from jsonpath import jsonpath

with open('json-doc/via_project_6Jul2022_1h18m_json.json') as json_file:
    via_file = json.load(json_file)

### Extract element content from JSON ###
filename_value = jsonpath(via_file, "$..filename")
size_value = jsonpath(via_file, "$..size")

name_shape_value = jsonpath(via_file, "$..shape_attributes.name")
x_value = jsonpath(via_file, "$..shape_attributes.x")
cx_value = jsonpath(via_file, "$..shape_attributes.cx")
y_value = jsonpath(via_file, "$..shape_attributes.y")
cy_value = jsonpath(via_file, "$..shape_attributes.cy")
width_value = jsonpath(via_file, "$..shape_attributes.width")
rx_value = jsonpath(via_file, "$..shape_attributes.rx")
height_value = jsonpath(via_file, "$..shape_attributes.height")
ry_value = jsonpath(via_file, "$..shape_attributes.ry")

region_attributes = jsonpath(via_file, "$..region_attributes")
name_region_value = jsonpath(via_file, "$..region_attributes.name")
type_value = jsonpath(via_file, "$..region_attributes.type")

caption_value = jsonpath(via_file, "$..file_attributes.caption")
public_domain_value = jsonpath(via_file, "$..file_attributes.public_domain")
image_url_value = jsonpath(via_file, "$..file_attributes.image_url")

### Build XML ElementTree ###
root = ET.Element("image") #XML root node
filename = ET.SubElement(root, "filename")
filename.text = str(filename_value[0])
size = ET.SubElement(root, "size") #Write data to XML ElementTree
size.text = str(size_value[0])
regions = ET.SubElement(root, "regions")

n = 0
for i in range(len(name_shape_value)):
    shape = ET.SubElement(regions, "shape_attributes")
    name_shape = ET.SubElement(shape, "name")
    name_shape.text = str(name_shape_value[i])
    if name_shape_value[i] == "rect": #If the container is rectangular
        x = ET.SubElement(shape, "x")
        x.text = str(x_value[i])
        y = ET.SubElement(shape, "y")
        y.text = str(y_value[i])
        width = ET.SubElement(shape, "width")
        width.text = str(width_value[i])
        height = ET.SubElement(shape, "height")
        height.text = str(height_value[i])
    elif name_shape_value[i] == "ellipse": #If the container is ellipse
        cx = ET.SubElement(shape, "cx")
        cx.text = str(cx_value[n])
        cy = ET.SubElement(shape, "cy")
        cy.text = str(cy_value[n])
        rx = ET.SubElement(shape, "rx")
        rx.text = str(rx_value[n])
        ry = ET.SubElement(shape, "ry")
        ry.text = str(ry_value[n])
        n = n+1
    region = ET.SubElement(regions, "region_attributes")
    name_region = ET.SubElement(region, "name")
    name_region.text = str(name_region_value[i])
    type = ET.SubElement(region, "type")
    type.text = str(type_value[i])
    image_quality = ET.SubElement(region, "image_quality")
    if_blur = jsonpath(region_attributes[i], "$..blur")
    if_good_illumination = jsonpath(region_attributes[i], "$..good_illumination")
    if_frontal = jsonpath(region_attributes[i], "$..frontal")
    blur = ET.SubElement(image_quality, "blur")
    good_illumination = ET.SubElement(image_quality, "good_illumination")
    frontal = ET.SubElement(image_quality, "frontal")
    if if_blur:
        blur.text = "True"
    else:
        blur.text = "False"
    if if_good_illumination:
        good_illumination.text = "True"
    else:
        good_illumination.text = "False"
    if if_frontal:
        frontal.text = "True"
    else:
        frontal.text = "False"

file_attributes = ET.SubElement(root, "file_attributes")
caption = ET.SubElement(file_attributes, "caption")
caption.text = str(caption_value[0])
public_domain = ET.SubElement(file_attributes, "public_domain")
public_domain.text = str(public_domain_value[0])
image_url = ET.SubElement(file_attributes, "image_url")
image_url.text = str(image_url_value[0])

tree = ET.ElementTree(root)
format = BytesIO()
tree.write(format)
xml = format.getvalue().decode('UTF8')
xml_tree = ET.fromstring(xml) #XML ElementTree finished

### Extract the image filename ###
url = []
for child in xml_tree.iter('filename'):
    url = child.text

### Extract container shape ###
name_list = []
for child in xml_tree.iter('shape_attributes'):
    name_list.append(child.find('name').text)

### Use loop to generate the DIV structure and css style under HTML ###
grid = ""
div = ""
for a in range(len(name_list)):
    if name_list[a] == "rect":
        grid = grid + """.grid"""+ str(a) +""" {
                    background-color: transparent;
                    position: absolute;
                    height: """ + str(xml_tree[2][2*a][4].text)+"""px;
                    width: """ + str(xml_tree[2][2*a][3].text) +"""px;
                    margin-left: """+ str(xml_tree[2][2*a][1].text) +"""px;
                    margin-top: """+ str(xml_tree[2][2*a][2].text) +"""px;
                    padding: 0;
                    border: 3px solid yellow;
                    display: inline-block;
                }\n
                .table"""+ str(a) +"""{
                    background-color: transparent;
                    position: absolute;
                    border: 1px solid black;
                    left: 40%;
                    top: """ + str(20*a) +"""%;
                    height: 100px;
                    width: 500px;
                }"""

    elif name_list[a] == "ellipse":
        grid = grid + """.grid"""+ str(a) +""" {
                    background-color: transparent;
                    position: absolute;
                    height: """ + str(xml_tree[2][2*a][4].text)+"""px;
                    width: """ + str(xml_tree[2][2*a][3].text) +"""px;
                    margin-left: """+ str(xml_tree[2][2*a][1].text) +"""px;
                    margin-top: """+ str(xml_tree[2][2*a][2].text) +"""px;
                    border-radius:100%;
                    padding: 0;
                    border: 3px solid yellow;
                    display: inline-block;
                }\n                    
                .table"""+ str(a) +"""{
                    background-color: transparent;
                    position: absolute;
                    border: 1px solid black;
                    left: 40%;
                    top: """ + str(20*a) +"""%;
                    height: 100px;
                    width: 500px;
                }"""
    div = div + """<span class="grid""" + str(a) + """"><span style = "color: white">"""+ str(a+1) +"""</span></span>\n
            <table class = "table""" + str(a) + """">
                <tr>
                    <th>number</th>
                    <th>name</th>
                    <th>type</th>
                    <th>image_quality</th>
                </tr>
                <tr>
                    <td>""" + str(a+1) + """</td>
                    <td>""" + str(xml_tree[2][2 * a + 1][0].text) + """</td>
                    <td>""" + str(xml_tree[2][2 * a + 1][1].text) + """</td>
                    <td><p>Blurred region:""" + str(xml_tree[2][2 * a + 1][2][0].text) + """
                    <p>Good Illumination:""" + str(xml_tree[2][2 * a + 1][2][1].text) + """
                    <p>Object in Frontal View:""" + str(xml_tree[2][2 * a + 1][2][2].text) + """
                    </td>
                </tr>
            </table>\n"""

### Write the HTML to The Death of Socrates by David.html ###
index_page = """ 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>The Death of Socrates by David</title>
    <style>
        %s
    </style>

</head>
<body>
    <div>
        <img src="image/%s" style = "position: absolute">
        %s
    </div>
</body>
</html>
"""% (grid, url, div)

GET_HTML = "The Death of Socrates by David.html"
f = open(GET_HTML, 'w')
f.write(index_page)
f.close()

### Run the HTML file one-box-test.html ###
webbrowser.open("The Death of Socrates by David.html")
