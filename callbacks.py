# Lavado Sanitario
# Lavado webApp - Callback function

# ----------------------------------------------------------------------------------------------------------------------
# Library
import plotly.express as px
from dash import Input, Output


# ----------------------------------------------------------------------------------------------------------------------
# Callback
# ----------------------------------------------------------------------------------------------------------------------
# Main callback situation
def register_callbacks(app, df, gdf, df_climate, df_climate_country):
    """
    Function that contain all the callback of the app
    :param app: dash app
    :param df: panda dataframe containing the disasters
    :param gdf: Geo dataframe containing the Continent
    :param df_climate: Temperature by year and lat & lon
    :param df_climate_country: Temperature by year, month in every countries
    :return:
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Callback for changing the type of analisis (Time-series or Geoplot)
    @app.callback(
        Output('disaster-content', 'children'),
        Input('analisis_type', 'value'))
    def geo_timeseries_content(analisis_type):
        return disaster_analisis(analisis_type)

    # ------------------------------------------------------------------------------------------------------------------
    # Callback for changing the type of filter (Time-series or Geoplot)
    @app.callback(
        Output('disaster-content_selector', 'children'),
        Input('analisis_type', 'value'))
    def geo_timeseries_selector(analisis_type):
        return disaster_analisis_selector(analisis_type)

    # ------------------------------------------------------------------------------------------------------------------
    # Callback for changing the type of filter (Time-series or Geoplot)
    @app.callback(
        Output('agg_function_selector', 'style'),
        Input('radio_items_format', 'value'))
    def timeseries_aggfunction_selector(selection):
        if selection == 'Frequency':
            return {'display': 'None'}
        if selection == 'Economical Impact':
            return {'display': 'block'}

    # ------------------------------------------------------------------------------------------------------------------
    # Callback for changing the type of filter (Time-series or Geoplot)
    @app.callback(
        Output('agg_function_selector_climat', 'style'),
        Input('radio_items_format_climat', 'value'))
    def timeseries_aggfunction_selector_climat(selection):
        if selection == 'Year':
            return {'display': 'None'}
        if selection == 'Month':
            return {'display': 'block'}

    # ------------------------------------------------------------------------------------------------------------------
    # Callback for changing the type of filter (Time-series or Geoplot)
    @app.callback(
        Output('year_range_climat', 'style'),
        Input('radio_items_time_climat', 'value'),
        Input('radio_items_measure_climat', 'value'),
        Input('radio_items_format_climat', 'value'))
    def timeseries_aggfunction_selector_climat_static(visual, selection, formato):
        if visual == 'Continents' or formato == 'Year':
            return {'display': 'None'}
        elif formato == 'Month':
            if selection == 'Animation':
                return {'display': 'None'}
            if selection == 'Static':
                return {'display': 'block'}

    # ------------------------------------------------------------------------------------------------------------------
    # Callback for changing the type of analisis (Time-series or Geoplot)
    @app.callback(
        Output('climate-content', 'children'),
        Input('analisis_type_Climat', 'value'))
    def geo_timeseries_content_climat(analisis_type):
        return climate_analisis(analisis_type)

    # ------------------------------------------------------------------------------------------------------------------
    # Callback for changing the type of filter (Time-series or Geoplot)
    @app.callback(
        Output('climate-content_selector', 'children'),
        Input('analisis_type_Climat', 'value'))
    def geo_timeseries_selector(analisis_type):
        return climate_analisis_selector(analisis_type)

    # ------------------------------------------------------------------------------------------------------------------
    # callback iteraction
    @app.callback(
        Output('Total_disaster', 'figure'),
        Input('radio_items_time', 'value'),
        Input('radio_items_format', 'value'),
        Input('radio_items_measure', 'value'))
    def update_figure_time(select_type, select_format, agg_type='Sum'):
        # filtering by type of disaster
        if select_type == 'All disasters':
            if select_format == 'Frequency':
                disasters_by_year = df["Year"].value_counts().to_frame().reset_index()
                disasters_by_year.columns = ["Year", "Count"]
                disasters_by_year = disasters_by_year.sort_values(by="Year", ascending=False)

                # Plotly
                fig = px.line(disasters_by_year, x="Year", y="Count", title='Total Disasters by Year')

            elif select_format == 'Economical Impact':
                # Sum total cost
                if agg_type == 'Sum':
                    total_damage_sum_year = df.groupby(by="Year")["Total Damages, Adjusted ('000 US$)"] \
                        .sum().reset_index()
                    total_damage_sum_year.columns = ["Year", "Total Damages, Adjusted ('000 US$) SUM"]

                    # Plotly
                    fig = px.bar(total_damage_sum_year, x="Year", y="Total Damages, Adjusted ('000 US$) SUM",
                                 title='Total Cost of Disasters by Year')

                # Average total cost by year
                elif agg_type == 'Mean':
                    total_damage_sum_year = df.groupby(by="Year")["Total Damages, Adjusted ('000 US$)"] \
                        .mean().reset_index()
                    total_damage_sum_year.columns = ["Year", "Total Damages, Adjusted ('000 US$) MEAN"]

                    # Plotly
                    fig = px.bar(total_damage_sum_year, x="Year", y="Total Damages, Adjusted ('000 US$) MEAN",
                                 title='Mean Cost of Disasters by Year')

        elif select_type == 'By type':
            if select_format == 'Frequency':
                # Disaster by subgroup
                disasters_by_year_subgroup = df.groupby(by=["Year", "Disaster Subgroup"]).size().reset_index()
                disasters_by_year_subgroup.columns = ["Year", "Disaster Type", "Count"]

                # plotly
                fig = px.line(disasters_by_year_subgroup, x="Year", y="Count", color='Disaster Type',
                              title='Total Disasters by Year for every Disaster Type')

            elif select_format == 'Economical Impact':
                # Sum total cost

                if agg_type == 'Sum':
                    total_damage_sum_year = df.groupby(by=["Year"
                        , "Disaster Subgroup"])["Total Damages, Adjusted ('000 US$)"].sum().reset_index()
                    total_damage_sum_year.columns = ["Year", "Disaster Type", "Total Damages, Adjusted ('000 US$) SUM"]

                    # Plotly
                    fig = px.bar(total_damage_sum_year, x="Year", y="Total Damages, Adjusted ('000 US$) SUM",
                                 color="Disaster Type", title='Total Cost of Disasters by Year and Type')

                # Average total cost by year
                elif agg_type == 'Mean':
                    total_damage_sum_year = df.groupby(by=["Year"
                        , "Disaster Subgroup"])["Total Damages, Adjusted ('000 US$)"].mean().reset_index()
                    total_damage_sum_year.columns = ["Year", "Disaster Type", "Total Damages, Adjusted ('000 US$) MEAN"]

                    # Plotly
                    fig = px.bar(total_damage_sum_year, x="Year", y="Total Damages, Adjusted ('000 US$) MEAN",
                                 color="Disaster Type", title='Mean Cost of Disasters by Year and Type')

        fig.update_layout(modebar_add=["v1hovermode", "toggleSpikeLines"], template='seaborn')

        return fig

