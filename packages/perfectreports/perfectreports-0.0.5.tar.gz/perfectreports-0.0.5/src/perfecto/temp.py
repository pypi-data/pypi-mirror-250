from prophet.plot import plot_plotly
import pandas
import statsmodels.api as sm
import os
import sys
from plotly import io
from base64 import b64encode
import plotly.graph_objects as go
import datetime
import matplotlib.pyplot as plt

type = "prediction"
duration = "dates"


def update_fig(fig, type, job, duration):
    fig.update_layout(
        title={"text": "History", "y": 0.97, "x": 0.5,
               "xanchor": "center", "yanchor": "top"},
        xaxis_title=duration,
        yaxis_title="Test Status",
        font=dict(
            family="Trebuchet MS, Helvetica, sans-serif", size=12, color="black",
        ),
        autosize=True,
        hovermode="x unified",
        yaxis={"tickformat": ".0f"},
        xaxis_tickformat="%d/%b/%y",
    )
    fig.update_yaxes(automargin=True)
    if type == "prediction":
        fig.update_layout(
            title={"text": "Trends"}, yaxis_title="Total tests executed", autosize=True,
        )
    return fig


"""
   suppress prophet logs
"""


class suppress_stdout_stderr(object):
    """
    A context manager for doing a "deep suppression" of stdout and stderr in
    Python, i.e. will suppress all print, even if the print originates in a
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).

    """

    def __init__(self):
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = (os.dup(1), os.dup(2))

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close the null files
        os.close(self.null_fds[0])
        os.close(self.null_fds[1])


job = "mas-automation-framework-parallel-web"
df = pandas.read_csv(
    '/Users/genesis.thomas/workspace/python/generic/PerfectoCustomReport/src/perfecto/output1.csv', low_memory=False)

# filter if job exists
if job != "":
    df = df[(df['job/name'] == job)]

df["startHour"] = pandas.to_datetime(
    pandas.to_datetime(df["startTime"], format="%Y-%m-%d %H:%M:%S")
    .dt.to_period("D")
    .astype(str)
)

df_hour = df['startHour'].value_counts().rename_axis('Hour').reset_index(
    name='counts').sort_values(by=['Hour'], ascending=True)
df_hour = df_hour.set_index(["Hour"])
fig = go.Figure(data=go.Scatter(x=df_hour.index.astype(dtype=str),
                                y=df_hour['counts'],
                                marker_color='green', text="counts"))
fig.update_layout({"xaxis": {"title": "Time"},
                   "yaxis": {"title": "Total Executions"},
                   "showlegend": False})

# top_dates = df_hour.sort_values(by=['counts'], ascending=False).head(3)
# vals = []
# for tgl, tot in zip(top_dates["Hour"], top_dates["counts"]):
#     tgl = tgl.strftime('%H hr')
#     val = "%d (%s)" % (tot, tgl)
#     vals.append(val)
# top_dates['tgl'] = vals
# print(top_dates)

# fig.add_traces(go.Scatter(x=top_dates['Hour'], y=top_dates['counts'],
#                         textposition='top center',
#                         textfont=dict(color='#233a77'),
#                         mode='markers+text',
#                         marker=dict(color='red', size=6),
#                         visible="legendonly",
#                         text=top_dates["tgl"]))
# fig.add_traces(go.Bar(x=df_hour['Hour'].astype(dtype=str),
#                     y=df_hour['counts'],
#                     visible="legendonly",
#                     marker_color='lightyellow', text=df_hour["counts"]))
# fig.update_layout(showlegend=False)
# fig.show()



# predict_df = df_hour

# width = 350
# height = 350

# predict_df = (
#     predict_df.groupby(["Hour"])
#     .size()
#     .reset_index(name="#status")
#     .sort_values("#status", ascending=False)
# )
# if len(predict_df.index) > 1:
#     predict_df = predict_df.rename(
#         columns={"Hour": "ds", "#status": "y"}
#     )
#     predict_df["cap"] = int(predict_df["y"].max()) * 2
#     predict_df["floor"] = 0
#     from prophet import Prophet

#     with suppress_stdout_stderr():
#         m = Prophet(
#             weekly_seasonality=False,
#             daily_seasonality=True,
#             yearly_seasonality=False,
#         ).fit(predict_df, algorithm="Newton")
#     future = m.make_future_dataframe(periods=1, freq='d')
#     future["cap"] = int(predict_df["y"].max()) * 1.6
#     floor = 0
#     if (int(predict_df["y"].min()) / 2) > 0:
#         floor = int(predict_df["y"].min())
#     future["floor"] = floor
#     forecast = m.predict(future)
#     forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(5)
#     fig = plot_plotly(
#         m, forecast, figsize=([height, width]))
#     fig.show()
#     fig = update_fig(fig, "prediction", job, duration)
#     encoded = b64encode(io.to_image(fig))
#     print('<div>'
#           + '<img src="data:image/png;base64, {}"'.format(
#               encoded.decode("ascii")
#           )
#           + " alt='prediction of "
#           + job
#           + "' id='reportDiv'> </img></div><br>"
#           )

train = df_hour[0:3]
test=df_hour[3:]
y_hat_avg = test.copy()
fit1 = sm.tsa.statespace.SARIMAX(train.counts).fit()
y_hat_avg['SARIMA'] = fit1.predict(start="2024-01-01", end="2024-01-02", dynamic=True)
plt.figure(figsize=(16,8))
plt.plot( train['counts'], label='Train')
plt.plot(df_hour['counts'], label='Test')
plt.plot(y_hat_avg['SARIMA'], label='SARIMA')
plt.legend(loc='best')
plt.show()
print("hi")