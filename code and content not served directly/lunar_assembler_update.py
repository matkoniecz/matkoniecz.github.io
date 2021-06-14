import requests
import os

def main():
  os.chdir("../osm_to_svg_in_browser")

  map_styles = [{'name': "general_high_zoom", 'description': 'area:highway included, general style - works well on scale of junction, neigbourhood, town, maybe also for entire cities'},
                {'name': "laser_neighbourhood", 'description': 'depiction of a neighbourhood - generates map designed to be a template for laser-cut 3D tactile maps'},
                {'name': "laser_road_area", 'description': 'depiction of a single crossing - generates map designed to be a template for laser-cut 3D tactile maps'},
                ]
  write_index_html(map_styles)
  download_map_styles(map_styles)
  get_file('lunar_assembler.dist.js')
  get_file('lunar_assembler.dist.css')
  get_file('lunar_assembler_in_action.gif', binary_file=True)

def write_index_html(map_styles):
  index_html = html_prefix() + """
        <h1>Generation of vector maps from OpenStreetMap data.</h1>
        <ul>
"""
  for map_style in map_styles:
    index_html += '<li><a href="' + map_style['name'] + '">' + map_style['name'].replace('_', ' ') + "</a> - " + map_style['description'] + "</li>\n"
  index_html += """        </ul>
  """
  index_html += html_suffix()
  index_html = add_header(index_html)
  with open('index.html', 'w') as file:
      file.write(index_html)

def html_prefix():
  return """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="https://mapsaregreat.com/style.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>General high zoom - SVG map from OpenStreetMap data</title>
    <link 
        rel="stylesheet" 
        href="lunar_assembler.dist.css"
    />
    <script src="lunar_assembler.dist.js"></script>
</head>
<body>
    <div id="main_content_wrap" class="outer">
    <section id="main_content" class="inner">"""

def html_suffix():
  return """    </section>
</body>
</html>"""

def download_map_styles(map_styles):
  for map_style in map_styles:
    get_file(map_style['name'] + '.html', text_processing_function=add_header)
    get_file(map_style['name'] + '_map_style.js')

def get_file(original_name, text_processing_function=None, new_name=None, binary_file=False):
  if new_name == None:
    new_name = original_name
  session = requests.Session()
  url = 'https://raw.githubusercontent.com/matkoniecz/lunar_assembler/master/examples/' + original_name
  response = session.get(url)
  if response.text.strip() == "404: Not Found":
    raise Exception("404 not found for <" + url + ">")
  write_mode = 'w'
  if binary_file:
    with open(new_name, 'wb') as file:
        if text_processing_function != None:
          raise Exception("binary vs text confusion - marked as binary but text processing function provided")
        file.write(response.content)
  else:
    with open(new_name, 'w') as file:
        text = response.text
        if text_processing_function != None:
          text = text_processing_function(text)
        file.write(response.text)

def add_header(page_text):
  replaced = """<div id="main_content_wrap" class="outer">"""
  new_content = """<div id="main_content_wrap" class="outer">
      <nav role='navigation' class="main-nav">
          <ul id="main-nav-list">
            <li>
              <a href="../index.html">
                <div>
                  Home
                </div>
              </a>
            </li>
            <li>
              <a href="../articles.html">
                <div>
                  Articles
                </div>
              </a>
            </li>
            <li>
              <a href="../recommendations.html">
                <div>
                  Recommendations
                </div>
              </a>
            </li>
            <li>
              <a href="../contact.html">
                <div>
                  Contact
                </div>
              </a>
            </li>
          </ul>
        </nav>"""
  return ensure_text_replacement(page_text, replaced, new_content)

def ensure_text_replacement(page_text, replaced, new_content):
  if replaced not in page_text:
      print(page_text)
      print("==== ^ text ==========")
      print("======================")
      print("==== v replaced ====")
      print(replaced)
      raise "text does not contain searched element"
  page_text = page_text.replace(replaced, new_content)
  return page_text

main()