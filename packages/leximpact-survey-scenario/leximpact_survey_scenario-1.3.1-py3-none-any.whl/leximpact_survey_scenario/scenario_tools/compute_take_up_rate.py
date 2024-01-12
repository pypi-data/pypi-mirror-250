from leximpact_survey_scenario.leximpact_survey_scenario import (
    LeximpactErfsSurveyScenario,
)
from leximpact_survey_scenario.leximpact_tax_and_benefit_system import leximpact_tbs
from leximpact_survey_scenario import root_path
import json
import os
from pathlib import Path
import pkg_resources
import pandas as pd
import asyncio

output_path = os.path.join(
    root_path, "leximpact_survey_scenario", "scenario_tools", "assets"
)


async def compute_take_up_rate(year, annee_donnees, save_result=True):
    cibles_aggregates_file = Path(
        pkg_resources.get_distribution("openfisca-france_data").location,
        "openfisca_france_data",
        "assets",
        "aggregats",
        "france_entiere",
        f"france_entiere_{year}.json",
    )

    with open(cibles_aggregates_file, "r") as f:
        cibles = json.load(f)

    cibles = pd.DataFrame(cibles["data"])[["variable", "actual_amount"]]

    leximpact_survey_scenario = LeximpactErfsSurveyScenario(
        annee_donnees=annee_donnees,
        period=year,
        baseline_tax_benefit_system=leximpact_tbs,
        survey_name=f"leximpact_{annee_donnees}",
    )

    rsa = cibles.loc[
        cibles["variable"] == "rsa"
    ].actual_amount / await leximpact_survey_scenario.compute_aggregate(
        "rsa", period=year
    )
    aah = cibles.loc[
        cibles["variable"] == "aah"
    ].actual_amount / await leximpact_survey_scenario.compute_aggregate(
        "aah", period=year
    )
    asf = cibles.loc[
        cibles["variable"] == "asf"
    ].actual_amount / await leximpact_survey_scenario.compute_aggregate(
        "asf", period=year
    )
    ppa = cibles.loc[
        cibles["variable"] == "ppa"
    ].actual_amount / await leximpact_survey_scenario.compute_aggregate(
        "ppa", period=year
    )
    aspa = cibles.loc[
        cibles["variable"] == "aspa"
    ].actual_amount / await leximpact_survey_scenario.compute_aggregate(
        "aspa", period=year
    )

    taux = {
        "rsa": min(float(rsa), 1),
        "aah": min(float(aah), 1),
        "aspa": min(float(aspa), 1),
        "ppa": min(float(ppa), 1),
        "asf": min(float(asf), 1),
    }

    if save_result:
        taux_non_recours = json.dumps(taux)
        with open(f"{output_path}/take_up_rate_{year}.json", "w") as outfile:
            outfile.write(taux_non_recours)

    return taux


taux = asyncio.run(compute_take_up_rate(year=2021, annee_donnees=2021))
print(taux)
