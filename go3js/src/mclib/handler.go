package mclib

import (
	"fmt"
	"net/http"
)

var html_template = `
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <meta name='viewport' content='width=device-width, initial-scale=1.0, maximum-scale=1.0'>
    <title>indodict</title>
    <!-- link rel="stylesheet" href="/static/css/style.css" -->

    <script src="/static/js/es-module-shims-1.6.3.js"></script>

    <script type="importmap">
      {
        "imports": {
          "three": "https://unpkg.com/three@0.155.0/build/three.module.js",
          "three/addons/": "https://unpkg.com/three@0.155.0/examples/jsm/"
        }
      }
    </script>
  </head>
  <body>
    <script type="module" src="/static/js/main.js"></script>
  %s
  </body>
</html>
`

func defaultHandler(w http.ResponseWriter, r *http.Request) {

	content := ""
	fmt.Fprintf(w, html_template, content)
}
