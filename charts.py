import altair as alt
import pandas as pd


def ssb_chart(
    data: pd.DataFrame,
    xvar: str = "category",
    yvar: str = "value",
    fvar: str = "scale",
    w: int = 400,
    total_h: int = 400,
    bar_color: str = "#FA7051",
    title: str = "Scale-Stack Bar Chart",
) -> alt.VConcatChart:
    _scales = data[fvar].sort_values(ascending=False).unique().tolist()
    _domain = data[xvar].values.tolist()

    base = alt.Chart(data)

    bars = []

    scale_one = data.query(f"{fvar} == 1")

    if scale_one.shape[0] == 1 and scale_one[yvar].item() == 1:
        _scales.remove(1)

    _per_plot_h = total_h / len(_scales)

    for scale in _scales:
        bar = (
            base.mark_bar(color=bar_color)
            .encode(
                x=alt.X(
                    f"{xvar}:N",
                    scale=alt.Scale(domain=_domain),
                    axis=alt.Axis(
                        labels=scale == min(_scales),
                        ticks=scale == min(_scales),
                        title=None if not scale == min(_scales) else xvar.capitalize(),
                        zindex=2,
                    ),
                ),
                y=alt.Y(
                    f"{yvar}:Q",
                    axis=alt.Axis(
                        tickCount=10,
                        ticks=False,
                        labels=False,
                        title=f"[0, {scale})",
                        titleAngle=0,
                        titleAlign="right",
                        titleAnchor="middle",
                        titleBaseline="middle",
                    ),
                    scale=alt.Scale(domain=[0, scale]),
                ),
                tooltip=[
                    alt.Tooltip(xvar, title=xvar.capitalize()),
                    alt.Tooltip(yvar, title=yvar.capitalize()),
                ],
            )
            .transform_filter((alt.datum.value < scale))
            .properties(height=_per_plot_h, width=w)
        )

        vrule = (
            base.mark_rule(xOffset=0.5, strokeDash=[4, 1])
            .encode(x=alt.X(f"{xvar}:N"))
            .transform_filter((alt.datum.value >= scale))
        )

        if scale != max(_scales):
            hrule = base.mark_rule(yOffset=0.5).encode(y=alt.value(0))

            bars.append(bar + vrule + hrule)
        else:
            bars.append(bar + vrule)

    return alt.vconcat(*bars, spacing=0, bounds="flush", title=title)


def omm_chart(
    data,
    xvar="category",
    e_yvar="exponent",
    m_yvar="mantissa",
    v_var="original",
    w=400,
    h=400,
    m_color="#FA7051",
    e_color="#707070",
    title="Order of Magnitude Markers",
):
    _n_bars = len(data[xvar].unique())

    # Default `bandPaddingInner` = 0.1
    # More info: https://altair-viz.github.io/user_guide/configuration.html#scale-configuration
    _e_bar_width = (w / _n_bars) - ((w / _n_bars) * 0.1)
    _m_bar_width = _e_bar_width / 5

    selection = alt.selection_single(fields=["to_color"], bind="legend")

    base = alt.Chart(data)

    e_bar = (
        base.mark_bar(color=e_color, size=_e_bar_width)
        .encode(
            x=alt.X(f"{xvar}:N", axis=alt.Axis(title=xvar.capitalize())),
            y=alt.Y(
                f"{e_yvar}:Q",
                axis=alt.Axis(title=None),
                scale=alt.Scale(domain=[0, 10]),
            ),
            tooltip=[
                alt.Tooltip(f"{xvar}:N", title=xvar.capitalize()),
                alt.Tooltip(f"{e_yvar}:Q", title=e_yvar.capitalize()),
                alt.Tooltip(f"{v_var}:N", title="Value"),
            ],
            color=alt.Color(
                "to_color:N",
                legend=alt.Legend(title="Part"),
                scale=alt.Scale(
                    domain=["Exponent", "Mantissa"], range=[e_color, m_color]
                ),
            ),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        )
        .transform_calculate(to_color="'Exponent'")
    )

    m_bar = (
        base.mark_bar(color=m_color, size=_m_bar_width)
        .encode(
            x=alt.X(f"{xvar}:N"),
            y=alt.Y(f"{m_yvar}:Q"),
            tooltip=[
                alt.Tooltip(f"{xvar}:N", title=xvar.capitalize()),
                alt.Tooltip(f"{m_yvar}:Q", title=m_yvar.capitalize()),
                alt.Tooltip(f"{v_var}:N", title="Value"),
            ],
            color=alt.Color("to_color:N"),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        )
        .transform_calculate(to_color="'Mantissa'")
    )

    # Open issue: https://github.com/altair-viz/altair/issues/2009
    m_bar = m_bar.add_selection(alt.selection_single())

    return (
        alt.layer(e_bar, m_bar, title=alt.TitleParams(title, anchor="start"))
        .properties(width=w, height=h)
        .add_selection(selection)
    )
