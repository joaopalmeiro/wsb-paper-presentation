import altair as alt
from typing import Dict


COLORS = {"white": "#FFFFFF", "light_gray": "#EBEBEB", "black": "#44475A"}
LOCALE = {"decimal": ".", "thousands": ",", "grouping": [3], "currency": ["", "€"]}


def lcontrast_theme_tooltip():
    from IPython.core.display import HTML

    # More info: https://github.com/vega/vega-tooltip/blob/master/vega-tooltip.scss
    return display(
        HTML(
            f"""
            <style>
                #vg-tooltip-element.vg-tooltip.lcontrast-theme {{
                    color: {COLORS["black"]};
                    border: 1px solid {COLORS["light_gray"]};
                    font-family: Roboto;
                    font-size: 11px;
                }}

                #vg-tooltip-element.vg-tooltip.lcontrast-theme td.key {{
                    color: {COLORS["black"]};
                    font-weight: bold;
                }}
            </style>
            """
        )
    )


def lcontrast_theme() -> Dict[str, Dict[str, object]]:
    font = "Roboto"

    return {
        "config": {
            "title": {"font": font, "color": COLORS["black"]},
            "axisX": {
                "labelFont": font,
                "titleFont": font,
                "gridColor": COLORS["light_gray"],
                "labelColor": COLORS["black"],
                "tickColor": COLORS["black"],
                "titleColor": COLORS["black"],
                "domainColor": COLORS["black"],
                "labelAngle": 0,
            },
            "axisY": {
                "labelFont": font,
                "titleFont": font,
                "gridColor": COLORS["light_gray"],
                "labelColor": COLORS["black"],
                "tickColor": COLORS["black"],
                "titleColor": COLORS["black"],
                "domainColor": COLORS["black"],
            },
            "header": {
                "labelFont": font,
                "titleFont": font,
                "labelColor": COLORS["black"],
                "titleColor": COLORS["black"],
            },
            "legend": {
                "labelFont": font,
                "titleFont": font,
                "labelColor": COLORS["black"],
                "titleColor": COLORS["black"],
            },
            "text": {"color": COLORS["black"]},
            "rule": {"color": COLORS["black"]},
            "background": COLORS["white"],
            "view": {"fill": COLORS["white"]},
        }
    }


def set_alt_tooltip_theme(tooltip_theme_name: str) -> str:
    if tooltip_theme_name in ["light", "dark"]:
        return tooltip_theme_name
    else:
        lcontrast_theme_tooltip()
        return tooltip_theme_name


THEMES = {"lcontrast": lcontrast_theme}


def set_alt_aesthetic(
    theme_name: str = "lcontrast", tooltip_theme_name: str = "lcontrast"
) -> None:
    tooltip_theme = set_alt_tooltip_theme(tooltip_theme_name)

    # More info: https://github.com/vega/vega-embed
    alt.renderers.enable(
        "default",
        embed_options={
            "actions": {
                "export": True,
                "source": False,
                "compiled": False,
                "editor": True,
            },
            "scaleFactor": 5,
            "i18n": {"PNG_ACTION": "Save as PNG", "SVG_ACTION": "Save as SVG"},
            "tooltip": {"theme": tooltip_theme},
            "renderer": "svg",
            "formatLocale": LOCALE,
        },
    )

    alt.themes.register(theme_name, THEMES.get(theme_name))
    alt.themes.enable(theme_name)
