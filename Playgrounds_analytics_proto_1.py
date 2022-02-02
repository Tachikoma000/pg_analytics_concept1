# The purpose of this program is to test out and develop a prototype of a custom dashboard which provides personalized
# metrics for users of Olympus Protocol
# ==================================================
# Import libraries for this app
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html, State
from millify import millify

from subgrounds.dash_wrappers import Graph
from subgrounds.plotly_wrappers import Figure, Scatter, Indicator

from olympus_subgrounds import sg, protocol_metrics_1year, last_metric, proposals, immediate

# This is a single page app

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server

# Nav bar creation. Something simple for now
navbar = dbc.NavbarSimple(
    children=[],
    brand='Playgrounds Analytics',
    brand_href='#',
    color='#2e343e',
    dark=True,
    fluid=True,
    style={'font-size': '20px',
           'justify - content': 'stretch'
           }
),

# create the app layout. Nothing too fancy, we just need a way to display the data from the users wallet

app.layout = dbc.Container([
    dbc.Row(navbar),
    # This section is for the Page label
    dbc.Row([
        dbc.Col([
            dbc.Label('Protocol Metrics',
                      style={'font-style': 'normal',
                             'font-weight': '600',
                             'font-size': '64px',
                             'line-height': '96px',
                             'color': '#FFFFFF',
                             }, xs=12, sm=12, md=12, lg=6, xl=6)
        ]),
    ], style={'padding': '10px'}),
    # This section is the first row for displaying the latest protocol metrics we care about
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3('Market Cap', className='display-3', style={'text-align': 'center'}),
                    html.Hr(className='my-2'),
                    html.H1('$' +
                            millify(
                                immediate(sg, last_metric.marketCap),
                                precision=2),
                            style={'text-align': 'center'}
                            ),
                ]),
            ], style={'height': '100%'}, color='#273342', inverse=True),
        ], xs=12, sm=12, md=12, lg=3, xl=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3('OHM Price', className='display-3', style={'text-align': 'center'}),
                    html.Hr(className='my-2'),
                    html.H1('$' +
                            millify(
                                immediate(sg, last_metric.ohmPrice),
                                precision=2),
                            style={'text-align': 'center'}
                            ),
                ]),
            ], style={'height': '100%'}, color='#273342', inverse=True),
        ], xs=12, sm=12, md=12, lg=3, xl=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3('Current APY (%)', className='display-3', style={'text-align': 'center'}),
                    html.Hr(className='my-2'),
                    html.H1(
                        millify(
                            immediate(sg, last_metric.currentAPY),
                            precision=2),
                        style={'text-align': 'center'}
                    ),
                ]),
            ], style={'height': '100%'}, color='#273342', inverse=True),
        ], xs=12, sm=12, md=12, lg=3, xl=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3('TVD', className='display-3', style={'text-align': 'center'}),
                    html.Hr(className='my-2'),
                    html.H1(
                        millify(
                            immediate(sg, last_metric.totalValueLocked),
                            precision=2),
                        style={'text-align': 'center'}
                    ),
                ]),
            ], style={'height': '100%'}, color='#273342', inverse=True),
        ], xs=12, sm=12, md=12, lg=3, xl=3),
    ], style={'padding': '10px'}),
    # This section is the first row of data charts
    dbc.Row([
        dbc.Col([dbc.Card([
            dbc.CardHeader([
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Risk Free Value of Treasury Assets: '),
                    ]),
                    dbc.Col([
                        millify(
                            immediate(sg, last_metric.treasuryRiskFreeValue),
                            precision=2)
                    ]),
                ]),
            ], style={'color': '#FFFFFF',
                      'font-weight': '500',
                      'font-size': '24px',
                      'font-style': 'normal'}),
            dbc.CardBody([
                Graph(Figure(
                    subgrounds=sg,
                    traces=[
                        # Risk free value treasury assets
                        Scatter(
                            name='lusd_rfv',
                            x=protocol_metrics_1year.datetime,
                            y=protocol_metrics_1year.treasuryLusdRiskFreeValue,
                            mode='lines',
                            line={'width': 0.5, 'color': 'rgb(0, 128, 255)'},
                            stackgroup='one',
                        ),
                        Scatter(
                            name='frax_rfv',
                            x=protocol_metrics_1year.datetime,
                            y=protocol_metrics_1year.treasuryFraxRiskFreeValue,
                            mode='lines',
                            line={'width': 0.5, 'color': 'rgb(0, 0, 64)'},
                            stackgroup='one',
                        ),
                        Scatter(
                            name='dai_rfv',
                            x=protocol_metrics_1year.datetime,
                            y=protocol_metrics_1year.treasuryDaiRiskFreeValue,
                            mode='lines',
                            line={'width': 0.5, 'color': 'rgb(255, 128, 64)'},
                            stackgroup='one',
                        ),
                    ],
                    layout={
                        'showlegend': True,
                        'xaxis': {'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white', 'showgrid': False},
                        'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white'},
                        'legend.font.color': 'white',
                        'paper_bgcolor': 'rgba(0,0,0,0)',
                        'plot_bgcolor': 'rgba(0,0,0,0)',
                    }
                ))
            ]),
            dbc.CardFooter('Learn more')
        ], style={'height': '100%'}, color='#273342', inverse=True),
        ], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([dbc.Card([
            dbc.CardHeader([
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Market Value of Treasury Assets: '),
                    ]),
                    dbc.Col([
                        millify(
                            immediate(sg, last_metric.treasuryMarketValue),
                            # sg.execute(
                            #     sg.mk_request([
                            #         last_metric.treasuryMarketValue
                            #     ])
                            # )[0]['protocolMetrics'][0]['treasuryMarketValue'],
                            precision=2)
                    ]),
                ]),
            ], style={'color': '#FFFFFF',
                      'font-weight': '500',
                      'font-size': '24px',
                      'font-style': 'normal'}),
            dbc.CardBody([
                Graph(Figure(
                    subgrounds=sg,
                    traces=[
                        # Market value treasury assets
                        Scatter(
                            name='xsushi_mv',
                            x=protocol_metrics_1year.datetime,
                            y=protocol_metrics_1year.treasuryXsushiMarketValue,
                            mode='lines',
                            line={'width': 0.5, 'color': 'rgb(255, 0, 255)'},
                            stackgroup='one',
                        ),
                        Scatter(
                            name='cvx_mv',
                            x=protocol_metrics_1year.datetime,
                            y=protocol_metrics_1year.treasuryCVXMarketValue,
                            mode='lines',
                            line={'width': 0.5, 'color': 'rgb(0, 128, 128)'},
                            stackgroup='one',
                        ),
                        Scatter(
                            name='weth_mv',
                            x=protocol_metrics_1year.datetime,
                            y=protocol_metrics_1year.treasuryWETHMarketValue,
                            mode='lines',
                            line={'width': 0.5, 'color': 'rgb(128, 0, 128)'},
                            stackgroup='one',
                        ),
                        Scatter(
                            name='lusd_mv',
                            x=protocol_metrics_1year.datetime,
                            y=protocol_metrics_1year.treasuryLusdMarketValue,
                            mode='lines',
                            line={'width': 0.5, 'color': 'rgb(0, 128, 255)'},
                            stackgroup='one',
                        ),
                        Scatter(
                            name='frax_mv',
                            x=protocol_metrics_1year.datetime,
                            y=protocol_metrics_1year.treasuryFraxMarketValue,
                            mode='lines',
                            line={'width': 0.5, 'color': 'rgb(0, 0, 64)'},
                            stackgroup='one',
                        ),
                        Scatter(
                            name='dai_mv',
                            x=protocol_metrics_1year.datetime,
                            y=protocol_metrics_1year.treasuryDaiMarketValue,
                            mode='lines',
                            line={'width': 0.5, 'color': 'rgb(255, 128, 64)'},
                            stackgroup='one',
                        )
                    ],
                    layout={
                        'showlegend': True,
                        'xaxis': {'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white', 'showgrid': False},
                        'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white'},
                        'legend.font.color': 'white',
                        'paper_bgcolor': 'rgba(0,0,0,0)',
                        'plot_bgcolor': 'rgba(0,0,0,0)',
                    }
                ))
            ]),
            dbc.CardFooter('Learn more')
        ], style={'height': '100%'}, color='#273342', inverse=True),
        ], xs=12, sm=12, md=12, lg=6, xl=6)
    ], style={'padding': '10px'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('OHM Market Cap: '),
                        ]),
                        dbc.Col([
                            millify(
                                immediate(sg, last_metric.marketCap),
                                # sg.execute(
                                #     sg.mk_request([
                                #         protocol_metrics_1year.marketCap
                                #     ])
                                # )[0]['protocolMetrics'][0]['marketCap'],
                                precision=2)
                        ]),
                    ]),
                ], style={'color': '#FFFFFF',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Scatter(
                                name='OHM Market Cap',
                                x=protocol_metrics_1year.datetime,
                                y=protocol_metrics_1year.marketCap
                            )
                        ],
                        layout={
                            'showlegend': True,
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white', 'showgrid': False},
                            'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white'},
                            'legend.font.color': 'white',
                            'paper_bgcolor': 'rgba(0,0,0,0)',
                            'plot_bgcolor': 'rgba(0,0,0,0)',
                        }
                    ))
                ]),
                dbc.CardFooter('Learn more')
            ], style={'height': '100%'}, color='#273342', inverse=True)
        ], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Staked OHM (%)'),
                        ]),
                    ]),
                ], style={'color': '#FFFFFF',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Scatter(
                                name='staked_supply_percent',
                                x=protocol_metrics_1year.datetime,
                                y=protocol_metrics_1year.staked_supply_percent,
                                mode='lines',
                                line={'width': 0.5, 'color': 'rgb(0, 255, 0)'},
                                stackgroup='one',
                            ),
                            Scatter(
                                name='unstaked_supply_percent',
                                x=protocol_metrics_1year.datetime,
                                y=protocol_metrics_1year.unstaked_supply_percent,
                                mode='lines',
                                line={'width': 0.5, 'color': 'rgb(255, 0, 0)'},
                                stackgroup='one',
                            )
                        ],
                        layout={
                            'title': {'text': 'Staked OHM (%)'},
                            'yaxis': {
                                'type': 'linear',
                                'range': [1, 100],
                                'ticksuffix': '%',
                                'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white'
                            },
                            'showlegend': True,
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white', 'showgrid': False},
                            'legend.font.color': 'white',
                            'paper_bgcolor': 'rgba(0,0,0,0)',
                            'plot_bgcolor': 'rgba(0,0,0,0)',
                        }
                    ))
                ]),
                dbc.CardFooter('Learn more')
            ], style={'height': '100%'}, color='#273342', inverse=True),
        ], xs=12, sm=12, md=12, lg=6, xl=6)
    ], style={'padding': '10px'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('RFV/OHM vs OHM Price'),
                        ]),
                    ]),
                ], style={'color': '#FFFFFF',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Scatter(
                                name='Risk-Free Value per OHM',
                                x=protocol_metrics_1year.datetime,
                                y=protocol_metrics_1year.rfv_per_ohm,
                                # line={'width': 0.5, 'color': 'rgb(255, 128, 64)'},
                            ),
                            Scatter(
                                name='OHM Price',
                                x=protocol_metrics_1year.datetime,
                                y=protocol_metrics_1year.ohmPrice,
                                # line={'width': 0.5, 'color': 'rgb(255, 128, 64)'},
                            ),
                        ],
                        layout={
                            'showlegend': True,
                            'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white'},
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white', 'showgrid': False},
                            'legend.font.color': 'white',
                            'paper_bgcolor': 'rgba(0,0,0,0)',
                            'plot_bgcolor': 'rgba(0,0,0,0)',
                        }
                    ))
                ]),
                dbc.CardFooter('Learn more')
            ], style={'height': '100%'}, color='#273342', inverse=True),
        ], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('OHM Price / RFV per OHM (%)'),
                        ]),
                    ]),
                ], style={'color': '#FFFFFF',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Scatter(
                                name='OHM Price / Risk-Free Value per OHM (%)',
                                x=protocol_metrics_1year.datetime,
                                y=protocol_metrics_1year.price_rfv_ratio,
                            ),
                        ],
                        layout={
                            'showlegend': True,
                            'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white'},
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white', 'showgrid': False},
                            'legend.font.color': 'white',
                            'paper_bgcolor': 'rgba(0,0,0,0)',
                            'plot_bgcolor': 'rgba(0,0,0,0)',
                        }
                    ))
                ]),
                dbc.CardFooter('Learn more')
            ], style={'height': '100%'}, color='#273342', inverse=True),
        ], xs=12, sm=12, md=12, lg=6, xl=6),
    ], style={'padding': '10px'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Treasury Market Value per OHM vs OHM Price'),
                        ]),
                    ]),
                ], style={'color': '#FFFFFF',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Scatter(
                                name='Treasury Market Value per OHM',
                                x=protocol_metrics_1year.datetime,
                                y=protocol_metrics_1year.tmv_per_ohm,
                                # line={'width': 0.5, 'color': 'rgb(255, 128, 64)'},
                            ),
                            Scatter(
                                name='OHM Price',
                                x=protocol_metrics_1year.datetime,
                                y=protocol_metrics_1year.ohmPrice,
                                # line={'width': 0.5, 'color': 'rgb(255, 128, 64)'},
                            ),
                        ],
                        layout={
                            'showlegend': True,
                            'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white'},
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white', 'showgrid': False},
                            'legend.font.color': 'white',
                            'paper_bgcolor': 'rgba(0,0,0,0)',
                            'plot_bgcolor': 'rgba(0,0,0,0)',
                        }
                    ))
                ]),
                dbc.CardFooter('Learn more')
            ], style={'height': '100%'}, color='#273342', inverse=True),
        ], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('OHM Price / Treasury Market Value per OHM (%)'),
                        ]),
                    ]),
                ], style={'color': '#FFFFFF',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Scatter(
                                name='OHM Price / Treasury Market Value per OHM (%)',
                                x=protocol_metrics_1year.datetime,
                                y=protocol_metrics_1year.price_tmv_ratio,
                            ),
                        ],
                        layout={
                            'showlegend': True,
                            'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white'},
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white', 'showgrid': False},
                            'legend.font.color': 'white',
                            'paper_bgcolor': 'rgba(0,0,0,0)',
                            'plot_bgcolor': 'rgba(0,0,0,0)',
                        }
                    ))
                ]),
                dbc.CardFooter('Learn more')
            ], style={'height': '100%'}, color='#273342', inverse=True),
        ], xs=12, sm=12, md=12, lg=6, xl=6),
    ], style={'padding': '10px'}),
    html.Footer('Powered by Protean Labs and The Graph',
                style={'backgrounds-color': '#2e343e',
                       'color': 'white',
                       'font-size': '20px',
                       'padding': '10px'
                       }),
], style={'backgroundColor': '#2a3847'}, fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)
