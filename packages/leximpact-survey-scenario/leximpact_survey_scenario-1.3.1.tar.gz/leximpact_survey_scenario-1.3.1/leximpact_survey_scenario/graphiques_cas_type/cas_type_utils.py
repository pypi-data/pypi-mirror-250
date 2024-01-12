# coding: utf-8

import copy
import logging
import numpy
import pandas as pd

from numpy import logical_or as or_, logical_and as and_

from openfisca_core import periods
from openfisca_core.rates import marginal_rate, average_rate
from openfisca_france_data.erfs_fpr.input_data_builder.step_03_variables_individuelles import (
    smic_annuel_net_by_year,
    smic_annuel_brut_by_year,
)
from taxipp.utils.general_utils import to_percent_round_formatter
from taxipp.utils.test_case import base
from taxipp.utils.test_case.utils import (
    calculate,
    create_scenario_actif,
    create_scenario_rentier,
)


log = logging.getLogger(__name__)


def create_test_case_dataframe(
    variables,
    input_variable="salaire_de_base",
    baseline_tax_benefit_system=None,
    tax_benefit_system=None,
    difference=False,
    graph_options={},
    test_case_options={},
    period=None,
):
    """
    Produit les données d'un cas-type (individu, ménage, famille ou foyer dont les caractéristiques sont définis dans
    le dictionnaire test_case_options en argument) pour différent niveau d'une variable d'input.
    """
    assert period is not None
    assert tax_benefit_system is not None
    assert not ((difference is True) and (baseline_tax_benefit_system is None))

    # Création des scenarios kwargs définissant le cas-types
    year = int(str(periods.period(period).this_year))
    if input_variable == "salaire_net" or input_variable == "salaire_de_base":
        scenario_actif = create_scenario_actif(
            year=year,
            test_case_options=test_case_options,
            graph_options=graph_options,
        )
        scenarios_kwargs = scenario_actif
    else:
        scenario_rentier = create_scenario_rentier(
            revenu=input_variable,
            year=year,
            test_case_options=test_case_options,
            graph_options=graph_options,
        )
        scenarios_kwargs = scenario_rentier

    # Compute RSA first : necessary for RSA computation to be right (due to existing OF-Core bug)
    variables_to_calculate = copy.deepcopy(variables)
    if "rsa" in variables:
        variables_to_calculate.remove("rsa")
        variables_to_calculate.insert(0, "rsa")

    # Simulation du cas-types
    variables = set([input_variable] + variables_to_calculate)

    df = calculate(
        period=period,
        scenarios_kwargs=scenarios_kwargs,
        tax_benefit_system=tax_benefit_system,
        reform=None,
        variables=variables,
    )

    if baseline_tax_benefit_system is not None:
        df_baseline = calculate(
            period=period,
            scenarios_kwargs=scenarios_kwargs,
            tax_benefit_system=baseline_tax_benefit_system,
            reform=None,
            variables=variables,
        )
        if difference:
            df = df - df_baseline
        else:
            df = df.merge(df_baseline, on=input_variable, suffixes=["", "_baseline"])

    return df


def plot_test_case(
    baseline_tax_benefit_system=None,
    tax_benefit_system=None,
    period=None,
    return_dataframes=False,
    input_variable="salaire_de_base",
    graph_options={},
    test_case_options={},
    monthly=True,
    impots_directs_positif=False,
):
    """
    Plot the graphs of a given income variable for a test-case scenario :
        - before and after a reform, if baseline_tax_benefit_system and
          tax_benefit_system are both not None
        - of a given tax and benefit system, if tax_benefit_system is not None
          and baseline_tax_benefit_system is None
    Additionally, it can return the dataframes with the figures used to plot these graphs.

    graph_options : {x_variable, y_variable, x_axis_denominator, decomposition_reform, decomposition_reference, count, nb_smic_max, stacked}
    test_case_options : {loyer, loyer_fictif, biactif, categorie_salarie, couple, nb_enfants, recourant_rsa, zone_apl, statut_occupation_logement ...}

    If impots_directs_positif option is True, the variable impots_directs will
    be included as a positive value in the test case, whatever the real
    sign of this variable (whether there is a net tax to pay or a net
    restitution to receive). If this option is True, and if input_variable
    is salaire_de_base, the variable
    revenus_nets_du_travail_net_impots_directs has to be included
    in decomposition_reform (resp. decomposition_reference) if impots_directs
    is in decomposition_reform (resp. decomposition_reference).
    If this option is True and input_variable is not salaire_de_base,
    a variable being the source of income studied, net of impots_directs,
    has to be included in decomposition_reform
    (resp. decomposition_reference) if impots_directs
    is in decomposition_reform (resp. decomposition_reference).

    """

    assert or_(
        and_(baseline_tax_benefit_system is not None, tax_benefit_system is not None),
        and_(baseline_tax_benefit_system is None, tax_benefit_system is not None),
    )
    assert tax_benefit_system is not None
    assert period is not None

    decomposition_reform = copy.deepcopy(
        graph_options.get(
            "decomposition_reform",
            copy.deepcopy(base.default_test_case_graph_decomposition),
        )
    )
    decomposition_reference = copy.deepcopy(
        graph_options.get(
            "decomposition_reference",
            copy.deepcopy(base.default_test_case_graph_decomposition),
        )
    )

    x_variable = graph_options.get("x_variable", input_variable)
    y_variable = graph_options.get("y_variable", None)

    # Get the dataframe to plot test-case (Baseline simulation)
    if baseline_tax_benefit_system is not None:
        baseline_df_variables = [
            input_variable,
            x_variable,
            y_variable,
        ] + decomposition_reference

        for variable in baseline_df_variables:
            assert (
                variable in baseline_tax_benefit_system.variables.keys()
            ), "La variable {} n'est pas dans le baseline tax and benefit system".format(
                variable
            )

        baseline_df = create_test_case_dataframe(
            graph_options=graph_options,
            tax_benefit_system=baseline_tax_benefit_system,
            test_case_options=test_case_options,
            variables=baseline_df_variables,
            input_variable=input_variable,
            period=period,
        )

        if (
            "impots_directs" in baseline_df_variables
            and graph_options.get("stacked", True) is True
        ):
            if impots_directs_positif is False:
                baseline_df["impots_directs_positif"] = baseline_df["impots_directs"]
                baseline_df["impots_directs_positif"].loc[
                    baseline_df["impots_directs"] > 0
                ] = (0 * baseline_df["impots_directs"])
                baseline_df["impots_directs_negatif"] = baseline_df["impots_directs"]
                baseline_df["impots_directs_negatif"].loc[
                    baseline_df["impots_directs"] <= 0
                ] = (0 * baseline_df["impots_directs"])
                baseline_df.drop(columns=["impots_directs"], inplace=True)
                decomposition_reference[
                    decomposition_reference.index("impots_directs")
                ] = "impots_directs_positif"
                i = 1 + decomposition_reference.index("impots_directs_positif")
                decomposition_reference.insert(i, "impots_directs_negatif")
            else:
                log.info(
                    "Veuillez mettre dans les variable à représenter une variable correspondant à la source de revenu étudiée nette d'impôt à payer"
                )
                baseline_df["impots_directs_positif"] = baseline_df["impots_directs"]
                baseline_df.loc[
                    baseline_df["impots_directs"] < 0, "impots_directs_positif"
                ] = -baseline_df["impots_directs"]
                baseline_df.drop(columns=["impots_directs"], inplace=True)
                decomposition_reference[
                    decomposition_reference.index("impots_directs")
                ] = "impots_directs_positif"

        if monthly:
            baseline_df = baseline_df / 12

    # Get the dataframe to plot test-case (Reform simulation)

    reform_df_variables = [
        input_variable,
        x_variable,
        y_variable,
    ] + decomposition_reform

    for variable in reform_df_variables:
        assert (
            variable in tax_benefit_system.variables.keys()
        ), "La variable {} n'est pas dans le tax and benefit system".format(variable)

    reform_df = create_test_case_dataframe(
        graph_options=graph_options,
        tax_benefit_system=tax_benefit_system,
        test_case_options=test_case_options,
        variables=reform_df_variables,
        input_variable=input_variable,
        period=period,
    )

    if (
        "impots_directs" in reform_df_variables
        and graph_options.get("stacked", True) is True
    ):
        if impots_directs_positif is False:
            # TODO use where
            reform_df["impots_directs_positif"] = reform_df["impots_directs"]
            reform_df.loc[
                reform_df["impots_directs"] > 0,
                "impots_directs_positif",
            ] = (
                0 * reform_df["impots_directs"]
            )
            reform_df["impots_directs_negatif"] = reform_df["impots_directs"].copy()
            reform_df.loc[
                reform_df["impots_directs"] <= 0, "impots_directs_negatif"
            ] = (0 * reform_df["impots_directs"])
            decomposition_reform[
                decomposition_reform.index("impots_directs")
            ] = "impots_directs_positif"
            i = 1 + decomposition_reform.index("impots_directs_positif")
            decomposition_reform.insert(i, "impots_directs_negatif")
            reform_df.drop(columns=["impots_directs"], inplace=True)

        else:
            log.info(
                "Veuillez mettre dans les variable à représenter une variable correspondant à la source de revenu étudiée nette d'impôt à payer"
            )
            reform_df["impots_directs_positif"] = reform_df["impots_directs"]
            reform_df["impots_directs_positif"].loc[
                reform_df["impots_directs"] < 0
            ] = -reform_df["impots_directs"]
            reform_df.drop(columns=["impots_directs"], inplace=True)
            decomposition_reform[
                decomposition_reform.index("impots_directs")
            ] = "impots_directs_positif"

    if monthly:
        reform_df = reform_df / 12

    df_list = [reform_df]
    if baseline_tax_benefit_system is not None:
        df_list = [reform_df, baseline_df]

    # Get x_variable as a fraction of a denominator (SMIC net, SMIC brut)

    x_axis_denominator = graph_options.get("x_axis_denominator", None)
    if x_axis_denominator is not None:
        if x_axis_denominator == "smic_net":
            denominator = smic_annuel_net_by_year[int(period)]
        if x_axis_denominator == "smic_brut":
            denominator = smic_annuel_brut_by_year[int(period)]
        if monthly:
            denominator = denominator / 12
        for df in df_list:
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

    for df in df_list:
        df.rename(columns=base.label_by_variable, inplace=True)

    # Reform_figure

    if decomposition_reform == []:
        ax = None
    else:
        ax = reform_df.plot.area(
            x=_(x_variable),
            y=[
                _(variable)
                for variable in decomposition_reform
                if (reform_df[_(variable)] != 0).any()
            ],
            linewidth=0,
            stacked=graph_options.get("stacked", True),
            grid=graph_options.get("grid", False),
            title=graph_options.get("title", None),
        )
    if y_variable is not None:
        label = y_variable
        if baseline_tax_benefit_system is not None:
            label = "{} (réforme)".format(_(y_variable))
        ax2 = reform_df.plot(
            x=_(x_variable),
            y=_(y_variable),
            ax=ax,
            color="black",
            label=label,
        )
        if baseline_tax_benefit_system is not None:
            ax3 = baseline_df.plot(
                x=_(x_variable),
                y=_(y_variable),
                style="--",
                ax=ax2,
                label="{} (initial)".format(_(y_variable)),
                color="black",
            )
        else:
            ax3 = ax2
    else:
        ax3 = ax

    set_color(ax3)
    ax3.legend(
        frameon=False,
        fontsize="medium",
        ncol=graph_options.get("ncol", 1),
        bbox_to_anchor=graph_options.get("bbox_to_anchor", None),
        loc=graph_options.get("loc", "upper left"),
    )
    if graph_options.get("y_axis_lim", None) is not None:
        ax3.set_ylim(graph_options["y_axis_lim"][0], graph_options["y_axis_lim"][1])
    if monthly is True:
        ax3.set_ylabel("Montant mensuel (en euros)")
    else:
        ax3.set_ylabel("Montant annuel (en euros)")
    reform_figure = ax3.get_figure()

    # Baseline_figure

    if baseline_tax_benefit_system is not None:
        if decomposition_reference == []:
            ax = None
        else:
            ax = baseline_df.plot.area(
                x=_(x_variable),
                y=[
                    _(variable)
                    for variable in decomposition_reference
                    if (baseline_df[_(variable)] != 0).any()
                ],
                linewidth=0,
                stacked=graph_options.get("stacked", True),
                grid=graph_options.get("grid", False),
                title=graph_options.get("title", None),
            )
        if y_variable is not None:
            ax2 = baseline_df.plot(
                x=_(x_variable),
                y=_(y_variable),
                ax=ax,
                style="--",
                label="{} (initial)".format(_(y_variable)),
                color="black",
            )
            ax3 = reform_df.plot(
                x=_(x_variable),
                y=_(y_variable),
                ax=ax2,
                label="{} (réforme)".format(_(y_variable)),
                color="black",
            )
        else:
            ax3 = ax

        set_color(ax3)
        ax3.legend(
            frameon=False,
            fontsize="medium",
            ncol=graph_options.get("ncol", 1),
            bbox_to_anchor=graph_options.get("bbox_to_anchor", None),
            loc=graph_options.get("loc", "upper left"),
        )
        if graph_options.get("y_axis_lim", None) is not None:
            ax3.set_ylim(graph_options["y_axis_lim"][0], graph_options["y_axis_lim"][1])
        if monthly is True:
            ax3.set_ylabel("Montant mensuel (en euros)")
        else:
            ax3.set_ylabel("Montant annuel (en euros)")
        baseline_figure = ax3.get_figure()

    # Results

    if return_dataframes:
        if baseline_tax_benefit_system is not None:
            return (reform_df, baseline_df, reform_figure, baseline_figure)
        else:
            return (reform_df, reform_figure)
    else:
        if baseline_tax_benefit_system is not None:
            return reform_figure, baseline_figure
        else:
            return reform_figure


def plot_variation(
    baseline_tax_benefit_system=None,
    tax_benefit_system=None,
    input_variable="salaire_de_base",
    graph_options={},
    test_case_options={},
    variation_relative=False,
    period=None,
    monthly=True,
):
    """

    Compare the variation in a variable value between baseline and reformed tax and benefit system.

    :param y_variable: Variable used to compute the variation.

    """

    assert baseline_tax_benefit_system is not None
    assert tax_benefit_system is not None
    assert period is not None

    x_variable = graph_options.get("x_variable", input_variable)
    y_variable = graph_options.get("y_variable", None)
    assert y_variable is not None

    # Get baseline simulation

    df = create_test_case_dataframe(
        graph_options=graph_options,
        tax_benefit_system=baseline_tax_benefit_system,
        difference=False,
        test_case_options=test_case_options,
        variables=[input_variable, x_variable, y_variable],
        input_variable=input_variable,
        period=period,
    )

    # Get variation in terms of y_variable

    df_diff = create_test_case_dataframe(
        graph_options=graph_options,
        tax_benefit_system=tax_benefit_system,
        baseline_tax_benefit_system=baseline_tax_benefit_system,
        difference=True,
        test_case_options=test_case_options,
        variables=[input_variable, x_variable, y_variable],
        input_variable=input_variable,
        period=period,
    )

    if monthly:
        df = df / 12
        df_diff = df_diff / 12
    if variation_relative:
        df[y_variable] = df_diff[y_variable] / df[y_variable]
    else:
        df[y_variable] = df_diff[y_variable]

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

    ax = df.plot.area(
        x=_(x_variable),
        y=_(y_variable),
        stacked=False,
        linewidth=0,
        legend=False,
        title=graph_options.get("title", None),
    )
    set_color(ax)
    ax.set_ylabel("Variation de {}".format(_(y_variable)))
    figure = ax.get_figure()

    return df, figure


def plot_tax_rates(
    baseline_tax_benefit_system=None,
    tax_benefit_system=None,
    period=None,
    denominator="salaire_de_base",
    numerator="revenu_disponible",
    tax_numerator=False,
    rates="marginal",
    round_unit=2,
    graph_options={},
    test_case_options={},
):
    """
    Plot the graphs comparing the tax rates for a given test-case scenario, before and after a reform.

    :param denominator: Variable used as the denominator in the marginal tax rate computation.
    :param numerator: Variable used as the numerato in the marginal tax rate computation.
    :param rates: Compute 'marginal' tax rates or 'average' tax rates.
    :param tax_numerator: If True, the marginal tax rate formula changes (its the same as when the numerator is an income but minus 1 so that MRT is between 0 and 100%)
    """

    assert tax_benefit_system is not None

    if graph_options is None:
        graph_options = {}
    if test_case_options is None:
        test_case_options = {}
    default_title = "Variying : {}, Target : {}".format(denominator, numerator)

    if baseline_tax_benefit_system:
        baseline_df = create_test_case_dataframe(
            graph_options=graph_options,
            tax_benefit_system=baseline_tax_benefit_system,
            test_case_options=test_case_options,
            variables=[denominator, numerator],
            input_variable=denominator,
            period=period,
        )
    reform_df = create_test_case_dataframe(
        graph_options=graph_options,
        tax_benefit_system=tax_benefit_system,
        test_case_options=test_case_options,
        variables=[denominator, numerator],
        input_variable=denominator,
        period=period,
    )

    # Compute the denominator as a share of another variable (SMIC brut, SMIC net..)

    x_axis_denominator = graph_options.get("x_axis_denominator", "smic_brut")
    if x_axis_denominator == "smic_net":
        denominator_denominator = smic_annuel_net_by_year[int(period)]
    if x_axis_denominator == "smic_brut":
        denominator_denominator = smic_annuel_brut_by_year[int(period)]

    if denominator_denominator is not None:
        if baseline_tax_benefit_system:
            baseline_df[denominator + "_en_part_de_{}".format(x_axis_denominator)] = (
                baseline_df[denominator] / denominator_denominator
            )
            baseline_df[numerator + "_en_part_de_{}".format(x_axis_denominator)] = (
                baseline_df[numerator] / denominator_denominator
            )
        reform_df[denominator + "_en_part_de_{}".format(x_axis_denominator)] = (
            reform_df[denominator] / denominator_denominator
        )
        reform_df[numerator + "_en_part_de_{}".format(x_axis_denominator)] = (
            reform_df[numerator] / denominator_denominator
        )
        if denominator in base.label_by_variable.keys():
            base.label_by_variable[
                denominator + "_en_part_de_{}".format(x_axis_denominator)
            ] = (
                base.label_by_variable[denominator]
                + " en part de "
                + base.label_by_denominator[x_axis_denominator]
            )
        denominator = denominator + "_en_part_de_{}".format(x_axis_denominator)
        numerator = numerator + "_en_part_de_{}".format(x_axis_denominator)

    # Compute tax rates

    rates_df = pd.DataFrame()
    if rates == "marginal":
        rate_function = marginal_rate
        if tax_numerator:
            rate_function = marginal_rate_bis
        rates_df[denominator] = reform_df[denominator].values[:-1]
    if rates == "average":
        rate_function = average_rate
        if tax_numerator:
            rate_function = average_rate_bis
        rates_df[denominator] = reform_df[denominator]

    rates_df["reform_{}_tax_rate".format(rates)] = rate_function(
        reform_df[numerator].values,
        reform_df[denominator].values,
        trim=[-0.99, 0.99],
    ).round(round_unit)
    if baseline_tax_benefit_system:
        rates_df["baseline_{}_tax_rate".format(rates)] = rate_function(
            baseline_df[numerator].values,
            baseline_df[denominator].values,
            trim=[-0.99, 0.99],
        ).round(round_unit)

    # Produce a graph

    rates_df.fillna(method="bfill", inplace=True)  # to make graph looks nicer
    ax = rates_df.rename(columns=base.label_by_variable).plot(
        x=_(denominator),
        grid=True,
        color=base.color_by_variable,
        title=graph_options.get("title", default_title),
    )
    set_color(ax)
    ax.yaxis.set_major_formatter(to_percent_round_formatter)
    ax.legend(frameon=True)
    rates_figure = ax.get_figure()

    return rates_figure, rates_df


# Helpers


def _(variable):
    if variable in base.label_by_variable.keys():
        return base.label_by_variable[variable]
    else:
        return variable


def set_color(ax, color_by_variable=base.color_by_variable):
    handles, labels = ax.get_legend_handles_labels()
    for label, handle in dict(zip(labels, handles)).items():
        if label in list(color_by_variable.keys()):
            handle.set_color(color_by_variable[label])
        ax.legend()


def average_rate_bis(target=None, varying=None, trim=None):
    """
    Computes the average rate of a targeted net income, according to the varying gross income.

    :param target: Targeted net income, numerator
    :param varying: Varying gross income, denominator
    :param trim: Lower and upper bound of average rate to return
    """
    average_rate = -target / varying
    if trim is not None:
        average_rate = numpy.where(average_rate <= max(trim), average_rate, numpy.nan)
        average_rate = numpy.where(average_rate >= min(trim), average_rate, numpy.nan)

    return average_rate


def marginal_rate_bis(target=None, varying=None, trim=None):
    # target: numerator, varying: denominator
    marginal_rate = -(target[:-1] - target[1:]) / (varying[:-1] - varying[1:])
    if trim is not None:
        marginal_rate = numpy.where(
            marginal_rate <= max(trim), marginal_rate, numpy.nan
        )
        marginal_rate = numpy.where(
            marginal_rate >= min(trim), marginal_rate, numpy.nan
        )

    return marginal_rate
