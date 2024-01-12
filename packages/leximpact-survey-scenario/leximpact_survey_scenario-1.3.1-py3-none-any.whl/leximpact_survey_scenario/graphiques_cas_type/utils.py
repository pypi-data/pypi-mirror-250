# coding: utf-8

import logging
from datetime import date
import pandas as pd
import numpy as np
from numpy import logical_not as not_, logical_or as or_

from openfisca_france.scenarios import init_single_entity
from openfisca_france.model.base import (
    TypesStatutMarital,
    TypesActivite,
    TypesCategorieSalarie,
    TypesStatutOccupationLogement,
)
from openfisca_france.model.revenus.activite.salarie import (
    TypesContratDeTravail,
)
from openfisca_france.model.prestations.aides_logement import TypesZoneApl
from openfisca_france import FranceTaxBenefitSystem

tax_and_benefit_system = FranceTaxBenefitSystem()

TAUX_DE_PRIME = 0.2

log = logging.getLogger(__name__)


def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def create_adulte(
    age=40,
    temps_partiel=False,
    union_legale=False,
    year=None,
    actif=False,
    cadre=False,
    salaire_de_base=None,
):
    assert year is not None

    parent = dict(
        date_naissance=date(year - age, 1, 1),
        age=age,
        statut_marital=TypesStatutMarital.marie.name
        if union_legale
        else TypesStatutMarital.celibataire.name,
    )

    if actif:
        activite = dict(
            activite=TypesActivite.actif.name,
            categorie_salarie=TypesCategorieSalarie.prive_cadre.name
            if cadre
            else TypesCategorieSalarie.prive_non_cadre.name,
            contrat_de_travail=TypesContratDeTravail.temps_partiel.name
            if temps_partiel
            else TypesContratDeTravail.temps_plein.name,  # CDI
            depcom_entreprise="75007",
            effectif_entreprise=25,
        )
        if salaire_de_base is not None:
            activite["salaire_de_base"]: salaire_de_base
        return merge_dicts(parent, activite)

    else:
        return parent


def create_logement(
    loyer_mensuel=None, statut_occupation_logement="locataire", zone_apl=2
):
    if loyer_mensuel or zone_apl or statut_occupation_logement:
        assert loyer_mensuel and zone_apl and statut_occupation_logement
        if statut_occupation_logement == "proprietaire":
            statut = TypesStatutOccupationLogement.proprietaire.name
        elif statut_occupation_logement == "locataire":
            statut = TypesStatutOccupationLogement.locataire_vide.name
        else:
            statut = None
        menage = dict(
            loyer=loyer_mensuel * 12 if loyer_mensuel else None,
            statut_occupation_logement=statut,
            zone_apl=zone_apl if zone_apl else None,
        )
        return menage
    else:
        return None


def create_architecture_cas_type(
    biactif=False,
    couple=False,
    loyer_mensuel=None,
    nb_enfants=0,
    parent1_age=40,
    parent2_age=None,
    enfants_age=range(0),
    statut_occupation_logement=None,
    temps_partiel=False,
    union_legale=False,
    year=None,
    zone_apl=2,
    salaire_parent2=None,
):
    assert year is not None

    menage = create_logement(
        loyer_mensuel=loyer_mensuel,
        statut_occupation_logement=statut_occupation_logement,
        zone_apl=zone_apl,
    )

    parent1 = create_adulte(
        actif=True,
        age=parent1_age,
        temps_partiel=temps_partiel,
        union_legale=union_legale & couple,
        year=year,
    )
    assert (couple and (parent2_age is not None)) or (
        (not couple) and (parent2_age is None)
    ), "Le paramètrage du conjoint n'est pas bien fait"

    parent2 = (
        create_adulte(
            actif=biactif,
            age=parent2_age,
            temps_partiel=temps_partiel,
            union_legale=union_legale & couple,
            year=year,
            salaire_de_base=salaire_parent2,
        )
        if couple
        else None
    )

    if len(enfants_age) > 0:
        assert (
            len(enfants_age) == nb_enfants
        ), "La liste des âges des enfants ne correspond pas au nombre d'enfants déclarés."
    else:
        enfants_age = range(1, nb_enfants + 1)
    enfants = [
        dict(date_naissance=date(year - age, 1, 1), age=age) for age in enfants_age
    ]
    # age = 4
    # enfants = [dict(date_naissance=date(year - age, 1, 1),
    #               age = age)]

    return dict(
        parent1=parent1,
        parent2=parent2,
        enfants=enfants,
        menage=menage,
    )


def create_scenario_inferieur_smic(
    biactif=False,
    couple=False,
    loyer_mensuel=None,
    nb_enfants=0,
    parent1_age=40,
    parent2_age=None,
    enfants_age=range(0),
    count=10,
    statut_occupation_logement=None,
    union_legale=False,
    year=None,
    zone_apl=None,
    salaire_parent2=None,
):
    assert year is not None
    temps_plein = 35 * 52

    scenario_kwargs = create_architecture_cas_type(
        biactif=biactif,
        couple=couple,
        nb_enfants=nb_enfants,
        parent1_age=parent1_age,
        parent2_age=parent2_age,
        enfants_age=enfants_age,
        temps_partiel=True,
        union_legale=union_legale,
        year=year,
        loyer_mensuel=loyer_mensuel,
        statut_occupation_logement=statut_occupation_logement,
        zone_apl=zone_apl,
        salaire_parent2=salaire_parent2,
    )

    smic_2 = tax_and_benefit_system.parameters(
        year - 2
    ).marche_travail.salaire_minimum.smic.smic_b_horaire
    smic_1 = tax_and_benefit_system.parameters(
        year - 1
    ).marche_travail.salaire_minimum.smic.smic_b_horaire
    smic = tax_and_benefit_system.parameters(
        year
    ).marche_travail.salaire_minimum.smic.smic_b_horaire

    additionnal_scenario_kwargs = dict(
        axes=[
            [
                dict(
                    count=count,
                    min=0,
                    max=temps_plein,
                    name="heures_remunerees_volume",
                    period=year - 2,
                ),
                dict(
                    count=count,
                    min=0,
                    max=temps_plein,
                    name="heures_remunerees_volume",
                    period=year - 1,
                ),
                dict(
                    count=count,
                    min=0,
                    max=temps_plein,
                    name="heures_remunerees_volume",
                    period=year,
                ),
                dict(
                    count=count,
                    index=1 if biactif else None,
                    min=0,
                    max=temps_plein,
                    name="heures_remunerees_volume",
                    period=year - 2,
                ),
                dict(
                    count=count,
                    index=1 if biactif else None,
                    min=0,
                    max=temps_plein,
                    name="heures_remunerees_volume",
                    period=year - 1,
                ),
                dict(
                    count=count,
                    index=1 if biactif else None,
                    min=0,
                    max=temps_plein,
                    name="heures_remunerees_volume",
                    period=year,
                ),
                dict(
                    count=count,
                    min=0,
                    max=smic_2 * temps_plein,
                    name="salaire_de_base",
                    period=year - 2,
                ),
                dict(
                    count=count,
                    index=1 if biactif else None,
                    min=0 if (salaire_parent2 is None) else salaire_parent2,
                    max=(smic_2 * temps_plein)
                    if (salaire_parent2 is None)
                    else salaire_parent2,
                    name="salaire_de_base",
                    period=year - 2,
                ),
                dict(
                    count=count,
                    min=0,
                    max=smic_1 * temps_plein,
                    name="salaire_de_base",
                    period=year - 1,
                ),
                dict(
                    count=count,
                    index=1 if biactif else None,
                    min=0 if (salaire_parent2 is None) else salaire_parent2,
                    max=(smic_1 * temps_plein)
                    if (salaire_parent2 is None)
                    else salaire_parent2,
                    name="salaire_de_base",
                    period=year - 1,
                ),
                dict(
                    count=count,
                    min=0,
                    max=smic * temps_plein,
                    name="salaire_de_base",
                    period=year,
                ),
                dict(
                    count=count,
                    index=1 if biactif else None,
                    min=0 if (salaire_parent2 is None) else salaire_parent2,
                    max=(smic * temps_plein)
                    if (salaire_parent2 is None)
                    else salaire_parent2,
                    name="salaire_de_base",
                    period=year,
                ),
            ]
        ],
        period="year:{}:3".format(year - 2),
    )

    scenario_kwargs.update(additionnal_scenario_kwargs)
    return scenario_kwargs


def create_scenario_superieur_smic(
    biactif=False,
    categorie_salarie="prive_non_cadre",
    couple=False,
    loyer_mensuel=None,
    nb_enfants=0,
    nb_smic_max=2,
    parent1_age=40,
    parent2_age=None,
    enfants_age=range(0),
    count=10,
    statut_occupation_logement=None,
    union_legale=False,
    year=None,
    zone_apl=None,
    salaire_parent2=None,
):
    assert year is not None

    if isinstance(categorie_salarie, str):
        categories_salarie = [
            "prive_non_cadre",
            "prive_cadre",
            "public_titulaire_etat",
            "public_titulaire_militaire",
            "public_titulaire_territoriale",
            "public_titulaire_hospitaliere",
            "public_non_titulaire",
        ]
        assert categorie_salarie in categories_salarie

    name_prime = None
    if categorie_salarie in ["prive_non_cadre", "prive_cadre"]:
        name_salaire = "salaire_de_base"
        # name_prime =
    else:
        name_salaire = "traitement_indiciaire_brut"
        name_prime = "primes_fonction_publique"

    scenario_kwargs = create_architecture_cas_type(
        biactif=biactif,
        couple=couple,
        nb_enfants=nb_enfants,
        parent1_age=parent1_age,
        parent2_age=parent2_age,
        enfants_age=enfants_age,
        union_legale=union_legale,
        year=year,
        loyer_mensuel=loyer_mensuel,
        statut_occupation_logement=statut_occupation_logement,
        zone_apl=zone_apl,
        salaire_parent2=salaire_parent2,
    )

    additionnal_kwargs = dict(
        categorie_salarie=categorie_salarie,
    )
    scenario_kwargs["parent1"].update(additionnal_kwargs)
    if biactif:
        scenario_kwargs["parent2"].update(additionnal_kwargs)

    axes = list()
    for axe_year in range(year - 2, year + 1):
        axes.append(
            dict(
                count=count,
                min=tax_and_benefit_system.parameters(
                    axe_year
                ).marche_travail.salaire_minimum.smic.smic_b_mensuel
                * 12,
                max=tax_and_benefit_system.parameters(
                    axe_year
                ).marche_travail.salaire_minimum.smic.smic_b_mensuel
                * 12
                * nb_smic_max,
                name=name_salaire,
                period=axe_year,
            )
        )
        if name_prime:
            axes.append(
                dict(
                    count=count,
                    min=tax_and_benefit_system.parameters(
                        axe_year
                    ).marche_travail.salaire_minimum.smic.smic_b_mensuel
                    * 12
                    * TAUX_DE_PRIME,
                    max=tax_and_benefit_system.parameters(
                        axe_year
                    ).marche_travail.salaire_minimum.smic.smic_b_mensuel
                    * 12
                    * nb_smic_max
                    * TAUX_DE_PRIME,
                    name=name_prime,
                    period=axe_year,
                )
            )
        if biactif:
            axes.append(
                dict(
                    count=count,
                    index=1,
                    min=(
                        tax_and_benefit_system.parameters(
                            axe_year
                        ).marche_travail.salaire_minimum.smic.smic_b_mensuel
                        * 12
                    )
                    if (salaire_parent2 is None)
                    else salaire_parent2,
                    max=(
                        tax_and_benefit_system.parameters(
                            axe_year
                        ).marche_travail.salaire_minimum.smic.smic_b_mensuel
                        * 12
                        * nb_smic_max
                    )
                    if (salaire_parent2 is None)
                    else salaire_parent2,
                    name=name_salaire,
                    period=axe_year,
                )
            )

    additionnal_scenario_kwargs = dict(
        axes=[axes],
        period="year:{}:3".format(year - 2),
    )
    scenario_kwargs.update(additionnal_scenario_kwargs)
    return scenario_kwargs


def create_scenario_actif(
    graph_options={},
    test_case_options={},
    union_legale=True,
    year=None,
    zone_apl=None,
):
    assert year is not None

    proprietaire = or_(
        test_case_options.get("statut_occupation_logement")
        == TypesStatutOccupationLogement.proprietaire.name,
        test_case_options.get("statut_occupation_logement")
        == TypesStatutOccupationLogement.primo_accedant.name,
    )

    # Fais en sorte que les observations soient également espacées
    nb_smic_max = graph_options.get("nb_smic_max", 2)
    count = graph_options.get("count", 100)
    count_inferieur = int(count / nb_smic_max)
    count_superieur = count - count_inferieur

    scenario_inferieur_smic = create_scenario_inferieur_smic(
        year=year,
        biactif=test_case_options.get("biactif", False),
        couple=test_case_options.get("couple", False),
        count=count_inferieur,
        loyer_mensuel=test_case_options.get("loyer", 500 if not_(proprietaire) else 0),
        nb_enfants=test_case_options.get("nb_enfants", 0),
        parent1_age=test_case_options.get("parent1_age", 40),
        parent2_age=test_case_options.get("parent2_age", 40),
        enfants_age=test_case_options.get("enfants_age", range(0)),
        statut_occupation_logement=test_case_options.get(
            "statut_occupation_logement",
            TypesStatutOccupationLogement.locataire_vide.name,
        ),
        zone_apl=test_case_options.get("zone_apl", TypesZoneApl.zone_2.name),
    )

    count = graph_options.get("count", 100)

    count_sup = 1 + (nb_smic_max - 1) * (count - 1) * 35 / (35 - 1)
    count_sup = int(np.ceil(count_sup))
    adjusted_nb_smic_max = 1 + (count_sup - 1) * (35 - 1) / 35 / (count - 1)

    scenario_superieur_smic = create_scenario_superieur_smic(
        year=year,
        biactif=test_case_options.get("biactif", False),
        couple=test_case_options.get("couple", False),
        count=count_superieur,
        loyer_mensuel=test_case_options.get("loyer", 500 if not_(proprietaire) else 0),
        nb_enfants=test_case_options.get("nb_enfants", 0),
        nb_smic_max=adjusted_nb_smic_max,
        parent1_age=test_case_options.get("parent1_age", 40),
        parent2_age=test_case_options.get("parent2_age", 40),
        enfants_age=test_case_options.get("enfants_age", range(0)),
        statut_occupation_logement=test_case_options.get(
            "statut_occupation_logement",
            TypesStatutOccupationLogement.locataire_vide.name,
        ),
        zone_apl=test_case_options.get("zone_apl", TypesZoneApl.zone_2.name),
    )

    return [scenario_inferieur_smic, scenario_superieur_smic]


def calculate(
    variables=None,
    scenarios_kwargs=None,
    period=None,
    tax_benefit_system=None,
    reform=None,
):
    assert variables is not None
    assert period is not None
    assert isinstance(scenarios_kwargs, list)
    assert tax_benefit_system is not None
    if reform is not None:
        tax_benefit_system = reform(tax_benefit_system)

    data_frames = list()
    for scenario_kwargs in scenarios_kwargs:
        data_frame = pd.DataFrame()

        tax_benefit_system_variables = set(tax_benefit_system.variables.keys())

        assert len(scenario_kwargs["axes"]) == 1
        axe_variables = set(axe["name"] for axe in scenario_kwargs["axes"][0])
        assert axe_variables.issubset(tax_benefit_system_variables)

        simulation = init_single_entity(
            tax_benefit_system.new_scenario(), **scenario_kwargs
        ).new_simulation()
        for variable in variables:
            count = scenario_kwargs["axes"][0][0]["count"]
            if tax_benefit_system.get_variable(variable) is None:
                log.info(
                    "La variable {} n'est pas définie dans le tax benefit system considéré. Elle n'est pas calculée.".format(
                        variable
                    )
                )
                continue
            array = simulation.calculate_add(variable, period=period)
            nb_person = int(array.shape[0] / count)
            if nb_person != 1:
                data_frame[variable] = sum(
                    array[i::nb_person] for i in range(0, nb_person)
                )
                if variable == "salaire_de_base":
                    for i in range(0, nb_person):
                        data_frame[f"salaire_de_base_{i}"] = array[i::nb_person]
            else:
                data_frame[variable] = simulation.calculate_add(variable, period=period)

        data_frames.append(data_frame)

    return pd.concat(data_frames).reset_index(drop=True)
