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
    _per_plot_h = total_h / len(_scales)

    base = alt.Chart(data)

    bars = []

    scale_one = data.query(f"{fvar} == 1")

    if scale_one.shape[0] == 1 and scale_one[yvar].item() == 1:
        _scales.remove(1)

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
