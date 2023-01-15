import base64
import pandas as pd
import numpy as np
from scipy.stats import mode
import io
from dash import dcc, html, dash_table
from data_viz import show_bar_plot, show_line_plot, show_box_plot
from server import app

def flatten(list_of_lists):
    r"""Utility function used to flatten a list of list into a single list.

    Parameters
    ----------
    l: list
        A list of lists.

    Returns
    -------
    pd.DataFrame


    Examples
    --------
    >>> from jmspack.utils import flatten
    >>> list_of_lists = [[f"p_{x}" for x in range(10)],
    ...                 [f"p_{x}" for x in range(10, 20)],
    ...                 [f"p_{x}" for x in range(20, 30)]]
    >>> flatten(list_of_lists)

    """
    return [item for sublist in list_of_lists for item in sublist]

def get_mode(col):
    return mode(col)[0][0]


def parse_input(contents, filename, bank_string):
    if "csv" not in filename:
        return html.Div([html.H2("There was an error processing this file."),
                         html.H6("check that the file is a '.csv' and that the export is from one of the banks listed in the sidebar.")]), "", "", "", "", ""

    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), sep=",")

            return df
        else:
            return html.Div(["Currently only .csv files are accepted in this dashboard"])
    except Exception as e:
        print(e)
        return html.Div([html.H6("There was an error processing this file.")])


def parse_descriptives(contents, filename, bank_string):
    df = parse_input(
        contents, filename, bank_string)
    
    # columns_list = "\n".join(df.columns.tolist())
    columns_list = flatten([[html.Code(x), html.Br()] for x in df.columns])

    descriptives_df = (
        df
        .agg(["count", "mean", "median", "std", "min", "max"])
        .sort_index()
        .reset_index()
        .round(2)
    )

    head_df = df.round(2)

    return html.Div(
        [
            html.H5(f"Dataset name: {filename}"),
            html.Div([
                html.H6("General Descriptives"),
                html.Div([html.P("Columns included in the dataset:")] + columns_list),
                html.Br(),
                html.P(f"""Row amount: {df.shape[0]}, column amount: {df.shape[1]}"""),
            ], id="general"
            ),
            html.H6("Data Frame Head"),
            dash_table.DataTable(
                data=head_df.to_dict("records"),
                columns=[{"name": i, "id": i} for i in head_df.columns],
                style_header={"backgroundColor": "#5f4a89"},
                sort_action="native",
                filter_action="native",
                row_deletable=False,
                export_format="csv",
                export_headers="display",
                merge_duplicate_headers=True,
                page_size=5,
            ),
            html.H6("Descriptive Statistics:"),
            dash_table.DataTable(
                descriptives_df.to_dict("records"),
                [{"name": i, "id": i} for i in descriptives_df.columns],
                style_header={"backgroundColor": "#5f4a89"},
            ),
        ]
    )


def parse_bar_plots(contents, filename, bank_string):
    df, amount_column, groupby_column, date_column, name_column, _ = parse_input(
        contents, filename, bank_string
    )

    df = df.sort_values(by=["Year-Month", "Amount (EUR)"])

    in_out_bar_fig = show_bar_plot(
        data=df,
        amount_column="in_out_amount",
        date_column=date_column,
        color_column=groupby_column,
        hover_columns=[name_column, groupby_column],
    )

    bar_in_fig = show_bar_plot(
        data=df[df["Debit/credit"] == "Credit"],
        amount_column=amount_column,
        date_column=date_column,
        color_column=groupby_column,
        hover_columns=[name_column, groupby_column],
    )
    bar_out_fig = show_bar_plot(
        data=df[df["Debit/credit"] == "Debit"],
        amount_column=amount_column,
        date_column=date_column,
        color_column=groupby_column,
        hover_columns=[name_column, groupby_column],
    )
    return html.Div(
        [
            html.H5(filename),
            html.H6(
                "Barplot of all incoming as positive and outgoing as negative transactions"),
            dcc.Graph(figure=in_out_bar_fig),
            # html.H6("Barplot of all incoming and outgoing transactions"),
            # dcc.Graph(figure=bar_fig),
            html.H6("Barplot of all outgoing transactions"),
            dcc.Graph(figure=bar_out_fig),
            html.H6("Barplot of all incoming transactions"),
            dcc.Graph(figure=bar_in_fig),
        ]
    )


def parse_time_plots(contents, filename, bank_string):
    df, amount_column, groupby_column, date_column, name_column, sum_column = parse_input(
        contents, filename, bank_string
    )

    color_column = "Debit/credit"

    box_fig = show_box_plot(
        data=df,
        amount_column=amount_column,
        date_column=date_column,
        color_column=color_column,
        hover_columns=[name_column, groupby_column],
    )

    feature_list = [name_column, groupby_column, amount_column, sum_column,
                    date_column, color_column]

    ts_df = df[feature_list].groupby(date_column).agg(
        dict(zip(feature_list, [get_mode, get_mode, "sum", "mean", get_mode, get_mode])))

    line_fig = show_line_plot(
        data=ts_df,
        amount_column=amount_column,
        date_column=date_column,
        color_column=color_column,
        hover_columns=[name_column, groupby_column],
    )

    sum_line_fig = show_line_plot(
        data=ts_df,
        amount_column=sum_column,
        date_column=date_column,
        color_column=None,
        hover_columns=[name_column, groupby_column],
    )
    return html.Div(
        [
            html.H5(filename),
            html.H6("Boxplot of all incoming and outgoing transactions"),
            dcc.Graph(figure=box_fig),
            html.H6("Lineplot of the sum of all incoming and outgoing transactions"),
            dcc.Graph(figure=line_fig),
            html.H6(
                "Lineplot of the daily mean of all incoming and outgoing transactions"),
            dcc.Graph(figure=sum_line_fig),
        ]
    )
