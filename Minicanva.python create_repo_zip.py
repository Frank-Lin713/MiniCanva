from zipfile import ZipFile
import os

project_name = "canva-clone-github"
file_structure = {
    "index.html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Mini Canva</title>
  <link rel="stylesheet" href="style.css" />
  <link rel="manifest" href="manifest.json" />
</head>
<body>
  <h1>Mini Canva Clone</h1>
  <div id="toolbar">
    <button onclick="addText()">Add Text</button>
    <button onclick="addImage()">Add Image</button>
    <button onclick="loadTemplate('template1')">Load Template 1</button>
    <button onclick="exportCanvas()">Export</button>
  </div>
  <canvas id="c" width="800" height="600"></canvas>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.0/fabric.min.js"></script>
  <script src="app.js"></script>
</body>
</html>""",

    "style.css": """body {
  font-family: Arial, sans-serif;
  text-align: center;
  margin: 20px;
}
canvas {
  border: 1px solid #ccc;
  margin-top: 10px;
}
#toolbar button {
  margin: 5px;
  padding: 10px 20px;
}""",

    "app.js": """const canvas = new fabric.Canvas('c');

function addText() {
  const text = new fabric.IText('Edit me', {
    left: 100,
    top: 100,
    fill: '#000',
    fontSize: 24
  });
  canvas.add(text);
}

function addImage() {
  fabric.Image.fromURL('https://via.placeholder.com/150', function(img) {
    img.scale(0.5);
    canvas.add(img);
  });
}

function exportCanvas() {
  const dataURL = canvas.toDataURL({
    format: 'png'
  });
  const link = document.createElement('a');
  link.href = dataURL;
  link.download = 'design.png';
  link.click();
}

function loadTemplate(templateName) {
  fetch(`templates/${templateName}.json`)
    .then(res => res.json())
    .then(json => canvas.loadFromJSON(json, canvas.renderAll.bind(canvas)));
}""",

    "manifest.json": """{
  "name": "Mini Canva Clone",
  "short_name": "CanvaLite",
  "start_url": "./index.html",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#317EFB",
  "icons": [
    {
      "src": "icons/icon.png",
      "type": "image/png",
      "sizes": "192x192"
    }
  ]
}""",

    "service-worker.js": """self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open('canva-clone').then(function (cache) {
      return cache.addAll([
        '/',
        '/index.html',
        '/style.css',
        '/app.js',
        '/manifest.json',
        'https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.0/fabric.min.js'
      ]);
    })
  );
});

self.addEventListener('fetch', function (e) {
  e.respondWith(
    caches.match(e.request).then(function (response) {
      return response || fetch(e.request);
    })
  );
});""",

    "templates/template1.json": """{
  "version": "5.3.0",
  "objects": [
    {
      "type": "i-text",
      "left": 50,
      "top": 50,
      "text": "Welcome to Mini Canva!",
      "fill": "#2b2b2b",
      "fontSize": 32
    },
    {
      "type": "rect",
      "left": 100,
      "top": 150,
      "width": 200,
      "height": 100,
      "fill": "#ace"
    }
  ]
}"""
}

# Create zip file
zip_filename = f"{project_name}.zip"
with ZipFile(zip_filename, "w") as zipf:
    for filepath, content in file_structure.items():
        zipf.writestr(os.path.join(project_name, filepath), content)

print(f"{zip_filename} created successfully!")
