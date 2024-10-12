import plotly.graph_objects as go
import pandas as pd
import numpy as np
def plot_yt_price_points_curve(df, h_range, fair_value_curve, symbol, network, mode, underlying_amount, yt_purchase_time=None,
                               add_difference_curve=False):
    """Plots YT Price, Points Earned, and optionally the Difference Curve."""

    fig = go.Figure()

    # Add YT Price and Points Earned curves
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['yt/underling'], mode='lines', name='YT Price', yaxis='y'))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['points'], mode='lines', name='Points Earned', yaxis='y2'))

    # Add Fair Value Curve
    fig.add_trace(go.Scatter(
        x=h_range,
        y=fair_value_curve,
        mode='lines',
        name='Fair Value Curve of YT',
        line=dict(color='yellow', dash='dot', width=3),
        yaxis='y'
    ))

    # Layout settings
    yaxis_config = dict(title='YT Price', side='left')
    yaxis2_config = dict(title='Points Earned', overlaying='y', side='right')

    layout_config = {
        'title': f'{symbol} on {network} [{underlying_amount} underlying coin]<br />|BUY YT WHEN THE yt Price IS UNDER THE FAIR VALUE CURVE TO MAXIMIZE POINTS EARNED|<br />|在yt价格低于公平价值曲线时购买yt以最大化获得的积分|<br />|yt価格が公正価値曲線よりも低い場合にytを購入してポイントを最大化する|',
        'xaxis_title': 'Certain Time of Purchasing YT',
        'yaxis': yaxis_config,
        'yaxis2': yaxis2_config,
        'template': mode
    }


    fig.update_layout(**layout_config)


    # Display the plot
    fig.show()



