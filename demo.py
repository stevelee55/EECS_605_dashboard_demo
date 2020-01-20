import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

image_data_bytes = 0

app.layout = html.Div(
	children=[
		dcc.Upload(
			id="upload_image",
			children=html.Div([
				"Drag and Drop or ",
				html.A("Select Files")
			]),
			style={
				'width': '100%',
				'height': '60px',
				'lineHeight': '60px',
				'borderWidth': '1px',
				'borderStyle': 'dashed',
				'borderRadius': '5px',
				'textAlign': 'center',
				'margin': '10px'
			},
			multiple=True
		),
		html.Button("Submit", id="button"),
		html.Div(id="output-data-upload"),
		html.Div(id="button-output", children="Enter a value and press submit")
	]
)

import base64

@app.callback(
	Output(component_id="output-data-upload", component_property="children"),
	[Input(component_id="upload_image", component_property="contents")],
	[State("upload_image", "filename"), State("upload_image", "last_modified")]
)
def update(contents, filename,last_modified):
	try:
		global image_data_bytes
		image_data_bytes = str.encode(contents[0].split(",")[1])

		return html.Div([html.Img(src=contents[0])]) # str(base64.decodebytes(image_data_bytes))
	except:
		return "Error"

# Why "n_clicks"?
@app.callback(
	Output("button-output", "children"),
	[Input("button", "n_clicks")],
)
def download_button(n_clicks):
	try:
		# Extracing image.
		f = open("test.png", "wb")
		f.write(base64.decodebytes(image_data_bytes))
		f.close()
		return str("Downloaded")
	except:
		return "Global var error."

if __name__ == '__main__':
	app.run_server(debug=True,port=8080,host='0.0.0.0')

