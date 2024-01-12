from openfisca_core.reforms import Reform
from openfisca_core.simulations.helpers import calculate_output_add
from openfisca_core.holders.helpers import set_input_divide_by_period

from openfisca_france_data.model.base import (
    MONTH,
    YEAR,
    Individu,
    FoyerFiscal,
    Famille,
    Variable,
)

variables_modifiees = [
    "impot_revenu_restant_a_payer",
    "csg_salaire",
    "csg_retraite",
    "af",
    "cf",
    "ars",
]
# TODO dealer avec le fait que pour la csg le nom de la variable de ratio et à caler sont différentes


def create_tax_and_benefits_system_with_targets(
    ratios_calage: dict,
    tax_and_benefits_system=None,
    variables_a_caler: list = variables_modifiees,
):
    for variable in variables_modifiees:
        if (variable not in ratios_calage.keys()) or (
            variable not in variables_a_caler
        ):
            ratios_calage[variable] = 1

    class tax_benefits_system_cale(Reform):
        name = ""

        def apply(self):
            baseline_irpp = self.baseline.get_variable("impot_revenu_restant_a_payer")
            formula_irpp = baseline_irpp.get_formula()

            class impot_revenu_restant_a_payer(Variable):
                value_type = float
                entity = FoyerFiscal
                label = "Impôt sur le revenu des personnes physiques restant à payer, après prise en compte des éventuels acomptes"
                reference = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_impot_revenu&espId=1&impot=IR&sfid=50"
                definition_period = YEAR

                def formula(foyer_fiscal, period, parameters):
                    return (
                        formula_irpp(foyer_fiscal, period, parameters)
                        * ratios_calage["impot_revenu_restant_a_payer"]
                    )

            baseline_csg_deductible_salaire = self.baseline.get_variable(
                "csg_deductible_salaire"
            )
            formula_csg_deductible_salaire = (
                baseline_csg_deductible_salaire.get_formula()
            )

            class csg_deductible_salaire(Variable):
                calculate_output = calculate_output_add
                value_type = float
                label = "CSG déductible sur les salaires"
                entity = Individu
                definition_period = MONTH
                set_input = set_input_divide_by_period

                def formula(individu, period, parameters):
                    return (
                        formula_csg_deductible_salaire(individu, period, parameters)
                        * ratios_calage["csg_salaire"]
                    )

            baseline_csg_imposable_salaire = self.baseline.get_variable(
                "csg_imposable_salaire"
            )
            formula_csg_imposable_salaire = baseline_csg_imposable_salaire.get_formula()

            class csg_imposable_salaire(Variable):
                calculate_output = calculate_output_add
                value_type = float
                label = "CSG imposable sur les salaires"
                entity = Individu
                definition_period = MONTH
                set_input = set_input_divide_by_period

                def formula(individu, period, parameters):
                    return (
                        formula_csg_imposable_salaire(individu, period, parameters)
                        * ratios_calage["csg_salaire"]
                    )

            baseline_csg_deductible_retraite = self.baseline.get_variable(
                "csg_deductible_retraite"
            )
            formula_csg_deductible_retraite = (
                baseline_csg_deductible_retraite.get_formula("2019-01-01")
            )

            class csg_deductible_retraite(Variable):
                calculate_output = calculate_output_add
                value_type = float
                label = "CSG déductible sur les retraites"
                entity = Individu
                definition_period = MONTH
                set_input = set_input_divide_by_period

                def formula(individu, period, parameters):
                    return (
                        formula_csg_deductible_retraite(individu, period, parameters)
                        * ratios_calage["csg_retraite"]
                    )

            baseline_csg_imposable_retraite = self.baseline.get_variable(
                "csg_imposable_retraite"
            )
            formula_csg_imposable_retraite = (
                baseline_csg_imposable_retraite.get_formula("2019-01-01")
            )

            class csg_imposable_retraite(Variable):
                calculate_output = calculate_output_add
                value_type = float
                label = "CSG imposable sur les retraites"
                entity = Individu
                definition_period = MONTH
                set_input = set_input_divide_by_period

                def formula(individu, period, parameters):
                    return (
                        formula_csg_imposable_retraite(individu, period, parameters)
                        * ratios_calage["csg_retraite"]
                    )

            baseline_af = self.baseline.get_variable("af")
            formula_af = baseline_af.get_formula("2015-07-01")

            class af(Variable):
                calculate_output = calculate_output_add
                value_type = float
                entity = Famille
                label = "Allocations familiales - total des allocations"
                definition_period = MONTH
                set_input = set_input_divide_by_period

                def formula(famille, period, parameters):
                    return formula_af(famille, period, parameters) * ratios_calage["af"]

            baseline_cf = self.baseline.get_variable("cf")
            formula_cf = baseline_cf.get_formula()

            class cf(Variable):
                calculate_output = calculate_output_add
                value_type = float
                entity = Famille
                label = "Complément familial"
                reference = (
                    "http://vosdroits.service-public.fr/particuliers/F13214.xhtml"
                )
                definition_period = MONTH
                set_input = set_input_divide_by_period

                def formula(famille, period, parameters):
                    return formula_cf(famille, period, parameters) * ratios_calage["cf"]

            baseline_ars = self.baseline.get_variable("ars")
            formula_ars = baseline_ars.get_formula()

            class ars(Variable):
                value_type = float
                entity = Famille
                label = "Allocation de rentrée scolaire"
                reference = (
                    "http://vosdroits.service-public.fr/particuliers/F1878.xhtml"
                )
                definition_period = YEAR

                def formula(famille, period, parameters):
                    return (
                        formula_ars(famille, period, parameters) * ratios_calage["ars"]
                    )

            variables_calees = [
                impot_revenu_restant_a_payer,
                csg_deductible_salaire,
                csg_imposable_salaire,
                csg_deductible_retraite,
                csg_imposable_retraite,
                af,
                cf,
                ars,
            ]

            for variable in variables_calees:
                self.update_variable(variable)

    leximpact_tax_benefits_system_cale = tax_benefits_system_cale(
        tax_and_benefits_system
    )

    return leximpact_tax_benefits_system_cale
