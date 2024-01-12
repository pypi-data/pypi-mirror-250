# -*- coding: utf-8 -*-


from openfisca_france_data.erfs_fpr.input_data_builder.step_03_variables_individuelles import (
    smic_annuel_net_by_year,
    smic_annuel_brut_by_year,
)
from taxipp.utils.test_case import base
from taxipp.utils.test_case.test_case_utils import (
    create_test_case_dataframe,
    set_color,
    _,
)


def gain_enfants(
    input_variable="salaire_de_base",
    decomposition=[],
    tax_benefit_system=None,
    graph_options={},
    test_case_options_initial={},
    test_case_options_final={},
    nb_enfants_initial=0,
    nb_enfants_final=1,
    variation_relative=False,
    period=None,
    monthly=True,
):
    """

    Compare test-case scenarios of couples with different number of children by
    computing the variation of taxes and benefits.

    :param decomposition: List of variables (taxes and benefits) for which to compute the variation.
    :param variation_relative: If True, compute variation divided by initial 'y_variable' value.

    """
    assert tax_benefit_system is not None
    assert period is not None

    x_variable = graph_options.get("x_variable", input_variable)
    y_variable = graph_options.get("y_variable", None)

    # Get simulation for each test-case scenarios (depends on number of children)

    df = dict()
    for nb_enfants in [nb_enfants_initial, nb_enfants_final]:
        if nb_enfants == nb_enfants_initial:
            test_case_options = test_case_options_initial
        else:
            test_case_options = test_case_options_final
        df["{}_enfants".format(nb_enfants)] = create_test_case_dataframe(
            graph_options=graph_options,
            tax_benefit_system=tax_benefit_system,
            difference=False,
            test_case_options=test_case_options,
            variables=[input_variable, x_variable, y_variable] + decomposition,
            input_variable=input_variable,
            period=period,
        )
        if monthly:
            df["{}_enfants".format(nb_enfants)] = (
                df["{}_enfants".format(nb_enfants)] / 12
            )

    df["difference"] = (
        df["{}_enfants".format(nb_enfants_final)]
        - df["{}_enfants".format(nb_enfants_initial)]
    )

    if variation_relative and y_variable:
        for column in df["difference"].columns:
            df["difference"][column] = (
                df["difference"][column]
                / df["{}_enfants".format(nb_enfants_initial)][y_variable]
            )

    df["difference"][x_variable] = df["{}_enfants".format(nb_enfants_initial)][
        x_variable
    ]
    df = df["difference"]
    for column in df.columns:
        df[column] = df[column].round()

    # Get x_variable as a fraction of a denominator (SMIC net, SMIC brut)

    x_axis_denominator = graph_options.get("x_axis_denominator", None)
    if x_axis_denominator is not None:
        if x_axis_denominator == "smic_net":
            denominator = smic_annuel_net_by_year[int(period)]
        if x_axis_denominator == "smic_brut":
            denominator = smic_annuel_brut_by_year[int(period)]
        if monthly:
            denominator = denominator / 12
        df[x_variable + "_en_part_de_{}".format(x_axis_denominator)] = (
            df[x_variable] / denominator
        )
        if x_variable in base.label_by_variable.keys():
            base.label_by_variable[
                x_variable + "_en_part_de_{}".format(x_axis_denominator)
            ] = (
                base.label_by_variable[x_variable]
                + " en part de "
                + base.label_by_denominator[x_axis_denominator]
            )
        x_variable = x_variable + "_en_part_de_{}".format(x_axis_denominator)

    df.rename(columns=base.label_by_variable, inplace=True)

    # Plot variation

    ax = None
    if decomposition:
        ax = df.plot.area(
            x=_(x_variable),
            y=[
                _(variable)
                for variable in decomposition
                if (df[_(variable)] != 0).any()
            ],
            linewidth=0,
            stacked=graph_options.get("stacked", True),
            grid=graph_options.get("grid", False),
            title=graph_options.get("title", None),
        )
    ax2 = ax
    if y_variable is not None:
        ax2 = df.plot(
            x=_(x_variable),
            y=_(y_variable),
            ax=ax,
            color="black",
            style="--",
        )
    set_color(ax2)
    ax2.set_title(
        graph_options.get(
            "title",
            "Gain du passage de {} à {} enfants".format(
                nb_enfants_initial, nb_enfants_final
            ),
        )
    )
    ax2.ticklabel_format(useOffset=False)
    ax2.legend(loc="upper right", frameon=False)
    ax.set_ylabel("Variation absolue (en euros)")
    if variation_relative and y_variable:
        ax.set_ylabel(
            "Variation relative" "\n" "(en termes de {})".format(_(y_variable))
        )
    figure = ax2.get_figure()

    return df, figure
