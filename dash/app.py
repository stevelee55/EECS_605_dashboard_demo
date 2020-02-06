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
				'width': '500px',
				'height': '60px',
				'lineHeight': '60px',
				'borderWidth': '2px',
				'borderStyle': 'dashed',
				'borderRadius': '5px',
				'textAlign': 'center',
				'margin': '10px',
				'margin-left': 'auto',
				'margin-right': 'auto'
			},
			multiple=True
		),
		html.Div(
			id="button-container",
			children=[
				html.Button(
					"Download Image",
					id="download-image-button",
				)
			],
			style={
				'textAlign': 'center',
				'margin-left': 'auto',
				'margin-right': 'auto'
			}
		),

		html.Div(
			id="image-viewer",
			style={
				'width': '500px',
				'height': '500px',
				'lineHeight': '60px',
				'borderWidth': '2px',
				'borderStyle': 'solid',
				'borderRadius': '5px',
				'textAlign': 'center',
				'margin': '10px',
				'margin-left': 'auto',
				'margin-right': 'auto',
				'position': 'relative'
			}
		),
		html.Div(id="output-data-upload"),
		html.Div(
			id="button-output",
			children="Enter a value and press submit",
			style={
				'textAlign': 'center'
			}
		),
		html.Div(
			id="graph-button-container",
			children=[
				html.Button(
					"Plot Graph",
					id="graph-feature-demo",
				)
			],
			style={
				'textAlign': 'center',
				'margin-left': 'auto',
				'margin-right': 'auto'
			}
		),
		dcc.Input(id='input', value='', type='text'),
		html.Div(id='output-graph'),

	]
)


import pandas_datareader.data as web
import datetime
@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value'), Input("graph-feature-demo", "n_clicks")]
)
def graph_demo_button(input_data, n_clicks):
	try:
		if int(n_clicks) > 0:
			start = datetime.datetime(2015, 1, 1)
			end = datetime.datetime.now()
			df = web.DataReader(input_data, 'stooq', start, end)
			# return str(df)
			df.reset_index(inplace=True)
			df.set_index("Date", inplace=True)
			df = df.drop("Volume", axis=1)

			return dcc.Graph(
				id='example-graph',
				figure={
					'data': [
						{'x': df.index, 'y': df.Close, 'type': 'line', 'name': input_data},
					],
					'layout': {
						'title': input_data
					}
				}
			)
		else:
			return
	except:
		return

import base64

@app.callback(
	Output(component_id="image-viewer", component_property="children"),
	[Input(component_id="upload_image", component_property="contents")],
	[State("upload_image", "filename"), State("upload_image", "last_modified")]
)
def update(contents, filename,last_modified):
	try:
		global image_data_bytes
		image_data_bytes = str.encode(contents[0].split(",")[1])

		return html.Img(
					src=contents[0],
					style={
						'max-height': '100%',
					    'max-width': '100%',
					    'width': 'auto',
					    'height': 'auto',
					    'position': 'absolute',
					    'top': '0',
					    'bottom': '0',
					    'left': '0',
					    'right': '0',
					    'margin': 'auto',
						'max-height': '100%'
					}
				) # str(base64.decodebytes(image_data_bytes))
	except:
		return html.Div(
			"Image Viewer",
			style={
				'max-height': '100%',
			    'max-width': '100%',
			    'width': 'auto',
			    'height': 'auto',
			    'position': 'absolute',
			    'top': '0',
			    'bottom': '0',
			    'left': '0',
			    'right': '0',
			    'margin': 'auto',
				'max-height': '100%'
			}
		)

# Why "n_clicks"?
@app.callback(
	Output("button-output", "children"),
	[Input("download-image-button", "n_clicks")],
)
def download_button(n_clicks):
	try:
		# Extracing image.
		f = open("downloaded_image.png", "wb")
		f.write(base64.decodebytes(image_data_bytes))
		f.close()
		return str("Downloaded")
	except:
		return

if __name__ == '__main__':
	try:
		app.run_server(debug=True,port=int(os.environ["$PORT"]),host='0.0.0.0')
	except:
		app.run_server(debug=True,port=8080,host='0.0.0.0')
