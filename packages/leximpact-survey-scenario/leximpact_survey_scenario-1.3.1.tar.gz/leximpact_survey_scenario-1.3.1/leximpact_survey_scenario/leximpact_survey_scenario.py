import logging
from pathlib import Path
from typing import List, Any, Optional, Union

import numpy as np
import pandas as pd
import shutil

from openfisca_core import periods
from openfisca_core.taxbenefitsystems import TaxBenefitSystem
from openfisca_core.tools.simulation_dumper import dump_simulation, restore_simulation

from openfisca_survey_manager.calibration import Calibration
from openfisca_survey_manager.simulations import SecretViolationError
from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_survey_manager import default_config_files_directory
from openfisca_survey_manager.scenarios.abstract_scenario import AbstractSurveyScenario

from leximpact_survey_scenario.scenario_tools.inflation_calibration_values import (
    inflation_coefs,
)
from leximpact_survey_scenario.leximpact_tax_and_benefit_system import leximpact_tbs
from leximpact_survey_scenario.scenario_tools.input_variables_list import (
    leximpact_used_as_input_variables,
)

pd.set_option("display.max_columns", None)
log = logging.getLogger(__name__)


admissible_simulation_prefix = [
    "baseline",
    "plf",
    "amendement",
]  # baseline should be first to properly custom initialize


computed_variables_to_dump = [
    "decile_rfr",
    "decile_rfr_par_part",
    "rfr",
    "rfr_par_part",
    "impot_revenu_restant_a_payer",
    "csg_deductible_retraite_foyer_fiscal",
    "csg_imposable_retraite_foyer_fiscal",
    "csg_deductible_salaire_foyer_fiscal",
    "csg_imposable_salaire_foyer_fiscal",
]


class LeximpactErfsSurveyScenario(AbstractSurveyScenario):
    """Survey scenario spécialisé pour l'ERFS-FPR utilisée par Leximpact."""

    used_as_input_variables = leximpact_used_as_input_variables
    id_variable_by_entity_key = dict(
        famille="idfam",
        foyer_fiscal="idfoy",
        menage="idmen",
    )

    role_variable_by_entity_key = dict(
        famille="quifam",
        foyer_fiscal="quifoy",
        menage="quimen",
    )

    weight_variable_by_entity = dict(
        menage="wprm",
        famille="weight_familles",
        foyer_fiscal="weight_foyers",
        individu="weight_individus",
    )

    def __init__(
        self,
        config_files_directory: str = default_config_files_directory,
        annee_donnees: int = 2021,
        period: int = 2024,
        rebuild_input_data: bool = False,
        # rebuild_input_data est un paramètre hérité de survey_manager.
        init_from_data: bool = True,
        baseline_tax_benefit_system: Optional[TaxBenefitSystem] = None,
        plf_tax_benefit_system: Optional[TaxBenefitSystem] = None,
        amendement_tax_benefit_system: Optional[TaxBenefitSystem] = None,
        data: Any = None,
        collection: str = "leximpact",
        survey_name: str = None,
        restore=False,
        dump=False,
        dump_directory=None,
        memory_config=None,
    ):
        """
        Create a `LeximpactErfsSurveyScenario`

        Args:
            annee_donnees (int, optional): Year of input data. Defaults to 2021.
            config_files_directory (str, optional): Configuration directory. Defaults to default_config_files_directory.
            annee_donnees (int, optional): Input data year. Defaults to 2021.
            period (int, optional): simulation year. Defaults to 2024.
            rebuild_input_data (bool, optional): Whether to rebuild input_data. Defaults to False.
            init_from_data (bool, optional): Wether to initalize. Defaults to True.
            baseline_tax_benefit_system (Optional[TaxBenefitSystem], optional): Baseline tax-nenefit-system. Defaults to None.
            plf_tax_benefit_system (Optional[TaxBenefitSystem], optional): PLF tax-nenefit-system. Defaults to None.
            amendement_tax_benefit_system (Optional[TaxBenefitSystem], optional): Amendement tax-benefit-system. Defaults to None.
            data (Any, optional): Initialization data. Defaults to None.
            collection (str, optional): Survey data collection. Defaults to "leximpact".
            survey_name (str, optional): Survey name. Defaults to None.
        """

        self.collection = collection
        self.annee_donnees = annee_donnees
        self.period = period

        if dump or restore:
            assert dump_directory is not None
            self.dump_directory = Path(dump_directory)

        # ## Initialisation des TaxBenefitSystems
        if baseline_tax_benefit_system is None:
            baseline_tax_benefit_system = leximpact_tbs

        self.set_tax_benefit_systems(
            baseline_tax_benefit_system=baseline_tax_benefit_system,
            plf_tax_benefit_system=plf_tax_benefit_system,
            amendement_tax_benefit_system=amendement_tax_benefit_system,
        )

        if survey_name is None:
            survey_name = f"{collection}_{annee_donnees}"

        # Création de la base de données sur les périodes voulues
        # S'il n'y a pas de données, on sait où les trouver.
        if data is None:
            # List of years available
            years_available = []
            log.info(
                f"LeximpactErfsSurveyScenario : Using {config_files_directory} as config_files_directory"
            )
            survey_collection = SurveyCollection.load(
                collection=collection, config_files_directory=config_files_directory
            )
            survey = survey_collection.get_survey(survey_name)

            for table_name, _ in survey.tables.items():
                if table_name[-4:].isnumeric():
                    years_available.append(int(table_name[-4:]))
            years_available = list(set(years_available))

            # List of years to create
            years = [self.period]

            log.info(f"{years_available=} vs {years=}")

            data = {"input_data_table_by_entity_by_period": {}, "survey": survey_name}
            data["config_files_directory"] = config_files_directory
            current_year = None

            for year in years:
                if data["input_data_table_by_entity_by_period"].get(year) is None:
                    data["input_data_table_by_entity_by_period"][year] = {}
                if year in years_available:
                    data_year = year
                else:
                    data_year = self.annee_donnees
                    print(f"WARNING: no data for {year}, will took {data_year}")
                for table_name, _ in survey.tables.items():
                    current_year = table_name[-4:]
                    if current_year.isnumeric():
                        current_year = int(current_year)
                        entity = table_name[:-5]
                        if current_year == data_year:
                            data["input_data_table_by_entity_by_period"][year][
                                entity
                            ] = table_name
                    else:
                        print(
                            f"WARNING {table_name} will be ignored because it has no year !!!"
                        )

        self.data = data
        print("Données du scénario : \n", data)
        if init_from_data:
            self.init_from_data(
                data=data,
                rebuild_input_data=rebuild_input_data,
                config_files_directory=data["config_files_directory"],
                restore=restore,
                dump=dump,
                memory_config=memory_config,
            )

    def calibrate(
        self,
        period: int = None,
        target_margins_by_variable: dict = None,
        parameters: dict = None,
        target_entity_count: float = None,
        inplace: bool = True,
    ):
        """Calibrate the scenario data.

        Args:
            period (int, optionnal): Period of calibration. Defaults to scenario.year
            target_margins_by_variable (dict, optional): Variable targets margins. Defaults to None.
            parameters (dict, optional): Calibration parameters. Defaults to None.
            total_population (float, optional): Total population target. Defaults to None.
        """

        survey_scenario = self

        if period is None:
            assert survey_scenario.period is not None
            period = survey_scenario.period

        if parameters is not None:
            assert parameters["method"] in [
                "linear",
                "raking ratio",
                "logit",
            ], "Incorect parameter value: method should be 'linear', 'raking ratio' or 'logit'"
            if parameters["method"] == "logit":
                assert parameters["invlo"] is not None
                assert parameters["up"] is not None
        else:
            parameters = dict(method="logit", up=3, invlo=3)

        # TODO: filtering using filtering_variable_by_entity
        for prefix in admissible_simulation_prefix:
            simulation = self.simulations[prefix]
            if simulation is None:
                continue
            calibration = Calibration(
                simulation,
                target_margins_by_variable,
                period,
                target_entity_count=target_entity_count,
                parameters=parameters,
                # filter_by = self.filter_by,
            )
            calibration.calibrate(inplace=inplace)
            simulation.calibration = calibration

    def custom_initialize(self, simulation):
        years = [self.period - 2, self.period - 1, self.period]
        inflator_by_variable = {}
        for inflation_year in years:
            inflator_by_variable.update(
                {
                    inflation_year: inflation_coefs(
                        self.used_as_input_variables,
                        str(self.annee_donnees),
                        str(inflation_year),
                    )
                }
            )
        for var in self.used_as_input_variables:
            if var in simulation.tax_benefit_system.variables:
                array_var = simulation.adaptative_calculate_variable(
                    var,
                    period=self.period,
                )

                if var == "date_naissance":
                    array_var = [
                        np.datetime64(date)
                        + np.timedelta64(365 * (self.period - self.annee_donnees), "D")
                        for date in array_var
                    ]

            for inflation_year in years:
                if var in inflator_by_variable[inflation_year].keys():
                    inflated_array = (
                        array_var.copy() * inflator_by_variable[inflation_year][var]
                    )
                else:
                    inflated_array = array_var.copy()
                try:
                    simulation.set_input(var, inflation_year, inflated_array)
                except ValueError:
                    simulation.delete_arrays(var, inflation_year)
                    simulation.set_input(var, inflation_year, inflated_array)

    def _handle_dump_restore(
        self,
        prefix,
        tax_benefit_system,
        memory_config,
        restore,
        dump,
        debug,
        trace,
        data,
    ):
        """
        Private methode to handle dump and restore of simulations on disk.
        """
        if restore:
            if prefix == "amendement":
                simulation = restore_simulation(
                    self.dump_directory / "initialisation", tax_benefit_system
                )
            else:
                simulation = restore_simulation(
                    self.dump_directory / prefix, tax_benefit_system
                )
            simulation.weight_variable_by_entity = self.weight_variable_by_entity
            simulation.id_variable_by_entity_key = self.id_variable_by_entity_key
            self.simulations[prefix] = simulation
        else:
            period = periods.period(self.annee_donnees)
            simulation = self.new_simulation(
                simulation_name=prefix,
                debug=debug,
                trace=trace,
                data=data,
                memory_config=memory_config,
            )
            if dump and prefix != "amendement":
                log.info(f"Dumping {prefix} simulation")

                # Dumping only initialisation variables
                if prefix == "baseline":
                    dump_directory = self.dump_directory / "initialisation"
                    if dump_directory.exists() and dump_directory.is_dir():
                        shutil.rmtree(dump_directory)
                    dump_simulation(simulation, dump_directory)

                # Dump full baseline and plf simulations
                period = periods.period(self.period)
                for computed_variable_to_dump in computed_variables_to_dump:
                    simulation.calculate(computed_variable_to_dump, period)

                dump_directory = self.dump_directory / prefix
                if dump_directory.exists() and dump_directory.is_dir():
                    shutil.rmtree(dump_directory)
                dump_simulation(simulation, dump_directory)

    def init_from_data(
        self,
        rebuild_input_data=False,
        data=None,
        memory_config=None,
        config_files_directory=default_config_files_directory,
        restore=False,
        dump=False,
    ):
        """Initialise a survey scenario from data.

        Args:
          rebuild_input_data(bool):  Whether or not to clean, format and save data. Take a look at :func:`build_input_data`
          data(dict): Contains the data, or metadata needed to know where to find it.
          memory_config : Experimental OpenFisca feature to store data on disk.
          config_files_directory:  Directory where to find the configuration files (Default value = default_config_files_directory)
          restore: Will variables data from self.dump_directory (Default value = False)
          dump: Will calculate variables then save them in self.dump_directory (Default value = False)
        """
        # When not ``None``, it'll try to get the data for *year*.
        if data is not None:
            data_year = data.get("data_year", self.annee_donnees)

        # When ``True`` it'll assume it is raw data and do all that described supra.
        # When ``False``, it'll assume data is ready for consumption.
        if rebuild_input_data:
            self.build_input_data(year=data_year)

        debug = self.debug
        trace = self.trace
        self.simulations = dict()

        for prefix, tax_benefit_system in self.tax_benefit_systems.items():
            self._handle_dump_restore(
                prefix,
                tax_benefit_system,
                memory_config,
                restore,
                dump,
                debug,
                trace,
                data,
            )

    def set_tax_benefit_system(self, tax_benefit_system, name):
        if (tax_benefit_system and name) is not None:
            if self.cache_blacklist is not None:
                tax_benefit_system.cache_blacklist = self.cache_blacklist
            if self.tax_benefit_systems:
                self.tax_benefit_systems[name] = tax_benefit_system
            else:
                self.tax_benefit_systems = {name: tax_benefit_system}

    def set_tax_benefit_systems(
        self,
        baseline_tax_benefit_system: TaxBenefitSystem,
        plf_tax_benefit_system: Optional[TaxBenefitSystem] = None,
        amendement_tax_benefit_system: Optional[TaxBenefitSystem] = None,
    ):
        """
        Sets the baseline tax and benefit system (TBS) and eventually the PLF TBS and the amendement TBS.

        Args:
          amendement_tax_benefit_system: The amendement tax benefit system (Default value = None)
          baseline_tax_benefit_system: The baseline tax benefit system (Default value = None)
          plf_tax_benefit_system: The PLF tax benefit system (Default value = None)
        """
        assert baseline_tax_benefit_system is not None
        self.set_tax_benefit_system(baseline_tax_benefit_system, "baseline")
        if plf_tax_benefit_system is not None:
            self.set_tax_benefit_system(plf_tax_benefit_system, "plf")
        if amendement_tax_benefit_system is not None:
            self.set_tax_benefit_system(amendement_tax_benefit_system, "amendement")

    async def compute_aggregate(
        self,
        variable: str,
        aggfunc: str = "sum",
        filter_by: Optional[str] = None,
        period: Optional[Union[str, int]] = None,
        simulation: Optional[str] = None,
        baseline_simulation: Optional[str] = None,
        missing_variable_default_value=np.nan,
        weighted: bool = True,
        alternative_weights=None,
    ):
        """
        Compute aggregate of a variable in an asynchronic way
        """
        assert simulation in admissible_simulation_prefix

        return super(LeximpactErfsSurveyScenario, self).compute_aggregate(
            variable=variable,
            aggfunc=aggfunc,
            filter_by=filter_by,
            period=period,
            simulation=simulation,
            baseline_simulation=baseline_simulation,
            missing_variable_default_value=missing_variable_default_value,
            weighted=weighted,
            alternative_weights=alternative_weights,
        )

    def summarize_by_quantile(
        self,
        variables: List = None,
        by: str = None,
        period: Any = None,
        simulation: str = None,
        baseline_simulation: str = None,
        filter_by=None,  # not used yet
        weighted: bool = True,  # not used yet
        alternative_weights=None,  # not used yet
        missing_variable_default_value: float = 0,
        format: str = None,
        observations_threshold: int = None,
        share_threshold: float = None,
    ):
        """
        Compute summary statistics by quantile.
        Args:
            variables (list): List of variables to compute quantiles on
            by (str): Variable to use for splitting the quantiles
            period (str): Open-Fisca period
            simulation (str): Simulation prefix
            baseline_simulation (str): Baseline simulation prefix
            filter_by (str): Variable to filter by (not used yet)
            weighted (bool): Whether to weight the statistics (not used yet)
            alternative_weights (dict): Alternative weights (not used yet)
            missing_variable_default_value (float): Missing variable default value
            format (str): Output format
            observations_threshold (int): Observations threshold, for fiscal data : 11, means that the minimum number of observations in a decile must be 11.
            share_threshold (float): Share threshold, for fiscal data : 0.85, means that the maximum value of a decile cannot exceed 85% of the sum of all decile values.
        Returns:
            dict: Summary statistics by quantile
            Sample for the fith quantile:
            {
                'csg_imposable_salaire_max': 0.0,
                'csg_imposable_salaire_mean': -340,
                'csg_imposable_salaire_min': -1_200,
                'csg_imposable_salaire_sum': -1_143_000_000,
                'rfr_max': 25_000,
                'rfr_mean': 22_000,
                'rfr_min': 20_000,
                'rfr_sum': 76_474_000_000,
                'count': 3_339_000,
                'quantile_num': 5.0,
                'fraction': 0.5
            }
        """
        assert simulation

        if not baseline_simulation:
            use_baseline_for_columns = False
        else:
            use_baseline_for_columns = True

        aggfuncs = ["max", "mean", "min", "sum", "count", "sum_abs"]
        summary = dict()

        # Compute the unweighted stats to test statistical secret violation
        if (observations_threshold is not None) or (share_threshold is not None):
            variables_sum = dict()
            for variable in variables:
                for aggfunc in aggfuncs:
                    summary[f"{variable}_{aggfunc}"] = self.compute_pivot_table(
                        simulation=simulation,
                        baseline_simulation=baseline_simulation,
                        aggfunc=aggfunc,
                        columns=[by],
                        values=[variable],
                        period=period,
                        weighted=False,
                        use_baseline_for_columns=use_baseline_for_columns,
                        missing_variable_default_value=missing_variable_default_value,
                    )
                    if aggfunc == "sum_abs":
                        variables_sum[variable] = (
                            summary[f"{variable}_{aggfunc}"].sum().sum()
                        )
            summary = pd.concat(summary).droplevel(1)
            summary.index.name = "variable_statistics"
            summary = summary.unstack().unstack()

            summary = summary.reset_index().to_dict(orient="records")
            nquantiles = max([decile[by] for decile in summary])

            secret_violation_variables = dict()
            for quantile_index, decile in enumerate(summary):
                variable = variables[0]
                decile["count"] = decile[f"{variable}_count"]
                secret_violation_variables[quantile_index + 1] = list()
                for variable in variables:
                    if observations_threshold and (
                        0 < decile[f"{variable}_count"] < observations_threshold
                    ):
                        error_msg = f'summarize_by_quantile : Not enough observations involved {decile[f"{variable}_count"]=} < {observations_threshold=} in {quantile_index+1=}'
                        log.warning(error_msg)
                        raise SecretViolationError(error_msg)
                    if share_threshold:
                        """
                        We check that the statistical secret is not violated.
                        1. We iterate over all variables and deciles.
                        2. We create a new variable called `share` which is a ratio of the maximum of the absolute value of the decile over the sum of all decile absolute values.
                        3. We check if the `share_threshold` is set, and if so, we check that the share is within the threshold. If not, we raise an error.
                        """
                        if decile[f"{variable}_sum_abs"] != 0:
                            abs_max = max(
                                decile[f"{variable}_max"], -decile[f"{variable}_min"]
                            )
                            share = abs_max / decile[f"{variable}_sum_abs"]
                            if abs_max == 0:
                                share = None
                            if share and not (0 < abs(share) < share_threshold):
                                if abs_max / variables_sum[variable] < 0.01:
                                    # arbitraire : si le max a un poid inferieur à 1% on le supprime et on continue le calcul
                                    secret_violation_variables[quantile_index + 1] += [
                                        variable
                                    ]
                                else:
                                    log.warning(
                                        f'summarize_by_quantile : SecretViolationError : {decile[f"{variable}_min"]=} {decile[f"{variable}_max"]=} {decile[f"{variable}_sum"]=} {quantile_index+1=}, {decile=}'
                                    )
                                    raise SecretViolationError(
                                        f"summarize_by_quantile : One observation exceeds {share_threshold=} ({share=}) for variable {variable}"
                                    )
                    del decile[f"{variable}_count"]

        # Compute the weighted stats
        summary = dict()
        variables_sum_before = dict()
        for variable in variables:
            for aggfunc in aggfuncs:
                summary[f"{variable}_{aggfunc}"] = self.compute_pivot_table(
                    simulation=simulation,
                    baseline_simulation=baseline_simulation,
                    aggfunc=aggfunc,
                    columns=[by],
                    values=[variable],
                    period=period,
                    weighted=True,
                    use_baseline_for_columns=use_baseline_for_columns,
                    missing_variable_default_value=missing_variable_default_value,
                )
                if aggfunc == "sum":
                    variables_sum_before[variable] = (
                        summary[f"{variable}_{aggfunc}"].sum().sum()
                    )

        summary = pd.concat(summary).droplevel(1)
        summary.index.name = "variable_statistics"
        summary = summary.unstack().unstack()

        if format != "dict":
            return summary

        summary = summary.reset_index().to_dict(orient="records")
        nquantiles = max([decile[by] for decile in summary])

        variables_sum_after = dict()
        for variable in variables:
            variables_sum_after[variable] = 0
        for decile in summary:
            variable = variables[0]
            decile["count"] = decile[f"{variable}_count"]
            decile["quantile_num"] = decile.pop(by)
            decile["fraction"] = float(decile["quantile_num"]) / float(nquantiles)
            num = decile["quantile_num"]
            if share_threshold:
                # TODO: fix technique rapide BCO, mais est-ce que ça a du sens ?
                if (
                    secret_violation_variables.get(num)
                    and len(secret_violation_variables[num]) > 0
                ):
                    for var in secret_violation_variables[decile["quantile_num"]]:
                        log.debug(
                            "{var} a été mis à zero dans le quantile {num} pour des raisons de secrets statistique"
                        )
                        for aggfunc in ["max", "mean", "min", "sum", "sum_abs"]:
                            decile[f"{var}_{aggfunc}"] = 0
            for variable in variables:
                variables_sum_after[variable] = (
                    variables_sum_after[variable] + decile[f"{variable}_sum"]
                )

        for variable in variables:
            if variables_sum_after[variable] / variables_sum_before[variable] < 0.99:
                # arbitraire, on dit que si on perd plus de 1% de la masse à cause du secret stat on renvoit une erreur
                raise SecretViolationError(
                    f"summarize_by_quantile : Too much observations delete for variable {variable}"
                )
        return summary

    def update_amendement(self, amendement_tax_benefit_system, memory_config=None):
        self.set_tax_benefit_system(amendement_tax_benefit_system, "amendement")

        debug = self.debug
        trace = self.trace
        data = self.data

        self.new_simulation(
            simulation_name="amendement",
            debug=debug,
            trace=trace,
            data=data,
            memory_config=memory_config,
        )

    def calculate_target_ratios(
        self,
        variables: list = None,
        targets_by_variable: dict = None,
        period: Any = None,
        simulation: str = None,
    ):
        assert variables is not None
        assert targets_by_variable is not None
        assert simulation is not None
        ratio = dict()

        simulation = self.simulations[simulation]

        for variable in variables:
            if variable in targets_by_variable.keys():
                ratio[variable] = targets_by_variable[
                    variable
                ] / simulation.compute_aggregate(variable, period=period)

        return ratio
