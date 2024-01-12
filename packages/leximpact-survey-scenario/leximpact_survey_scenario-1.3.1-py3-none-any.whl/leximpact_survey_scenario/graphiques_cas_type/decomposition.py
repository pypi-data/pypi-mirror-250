from leximpact_survey_scenario.leximpact_tax_and_benefit_system import leximpact_tbs

from leximpact_survey_scenario.graphiques_cas_type.cas_type_utils import (
    calculate,
    create_scenario_inferieur_smic,
    create_scenario_superieur_smic,
    #    smic_annuel_brut_by_year,
)

decompo_revenu_disponible = [
    "revenu_disponible",
    "prestations_sociales",
    "impots_directs",
    "revenus_nets_du_travail",
    "pensions_nettes",
    "revenus_nets_du_capital",
    "csg",
    "crds",
    "cotisations_salariales",
]

decompo_ir = [
    "irpp",
    "contribution_exceptionnelle_hauts_revenus",
    "ip_net",
    "decote",
    "ir_plaf_qf",
    "avantage_qf",
    "ir_ss_qf",
    "rni",
]

decompo_prestations = [
    "prestations_familiales",
    "minima_sociaux",
    "aides_logement",  ## que faire de la reduction de loyer de solidarite ?? Car va aux menages mais pas aide de l Etat en soi
]

decompo_minima_sociaux = [
    "aah",
    "caah",
    "aefa",
    "minimum_vieillesse",
    "rsa",
    "ppa",
    "garantie_jeunes",
]

decompo_prestations_familiales = [
    "af",
    "cf",
    "ars",
    "aeeh",
    "aes",
    "paje",
    "asf",
    "crds_pfam",
    "age",
]


def decomposition_data(
    year=2023,
    count=100,
    nb_smic_max=2,
    categorie_salarie="prive_non_cadre",
    biactif=False,
    couple=False,
    loyer_mensuel=None,
    nb_enfants=0,
    parent1_age=40,
    parent2_age=None,
    enfants_age=range(0),
    statut_occupation_logement=None,
    union_legale=False,
    zone_apl=None,
    salaire_parent2=None,
    variables=(
        decompo_revenu_disponible
        + decompo_ir
        + decompo_prestations
        + decompo_minima_sociaux
        + decompo_prestations_familiales
    ),
):
    scenario_inferieur_smic = create_scenario_inferieur_smic(
        year=year,
        count=count,
        # categorie_salarie=categorie_salarie,
        biactif=biactif,
        couple=couple,
        loyer_mensuel=loyer_mensuel,
        nb_enfants=nb_enfants,
        parent1_age=parent1_age,
        parent2_age=parent2_age,
        enfants_age=enfants_age,
        statut_occupation_logement=statut_occupation_logement,
        union_legale=union_legale,
        zone_apl=zone_apl,
        salaire_parent2=salaire_parent2,
    )

    scenario_superieur_smic = create_scenario_superieur_smic(
        year=year,
        count=count,
        nb_smic_max=nb_smic_max,
        categorie_salarie=categorie_salarie,
        biactif=biactif,
        couple=couple,
        loyer_mensuel=loyer_mensuel,
        nb_enfants=nb_enfants,
        parent1_age=parent1_age,
        parent2_age=parent2_age,
        enfants_age=enfants_age,
        statut_occupation_logement=statut_occupation_logement,
        union_legale=union_legale,
        zone_apl=zone_apl,
        salaire_parent2=salaire_parent2,
    )
    scenarios_kwargs = [scenario_inferieur_smic, scenario_superieur_smic]

    variables_to_compute = ["salaire_de_base"] + variables

    df = calculate(
        variables=variables_to_compute,
        scenarios_kwargs=scenarios_kwargs,
        period=year,
        tax_benefit_system=leximpact_tbs,
    )

    return df


def create_data_prestations_familiales(
    year=2023,
    nombre_enfants=1,
    ecart_age=1,
    age_max=25,
    variables=decompo_prestations_familiales,
    nombre_smic=4,
    monoactif=True,
    monoparental=True,
):
    datas_biactif = dict()
    datas_monoactif = dict()
    datas_monoparental = dict()
    for age in range(0, (age_max + 1)):
        enfants_age = [age + ecart_age * i for i in range(nombre_enfants)]
        donnees_biactif = decomposition_data(
            year=year,
            count=500,
            nb_smic_max=nombre_smic,
            categorie_salarie="prive_non_cadre",
            parent1_age=40,
            couple=True,
            union_legale=True,
            biactif=True,
            parent2_age=38,
            nb_enfants=nombre_enfants,
            enfants_age=enfants_age,
            loyer_mensuel=1600,
            statut_occupation_logement="locataire",
            zone_apl=2,
            variables=variables,
            #   salaire_parent2 = 30000,
        )
        datas_biactif[f"{enfants_age} ans"] = donnees_biactif
        if monoactif:
            donnees_monoactif = decomposition_data(
                year=year,
                count=500,
                nb_smic_max=nombre_smic,
                categorie_salarie="prive_non_cadre",
                parent1_age=40,
                couple=True,
                union_legale=True,
                biactif=False,
                parent2_age=38,
                nb_enfants=nombre_enfants,
                enfants_age=enfants_age,
                loyer_mensuel=1600,
                statut_occupation_logement="locataire",
                zone_apl=2,
                variables=variables,
            )
            datas_monoactif[f"{enfants_age} ans"] = donnees_monoactif
        if monoparental:
            donnees_monoparental = decomposition_data(
                year=year,
                count=500,
                nb_smic_max=nombre_smic,
                categorie_salarie="prive_non_cadre",
                parent1_age=40,
                couple=False,
                union_legale=True,
                biactif=False,
                nb_enfants=nombre_enfants,
                enfants_age=enfants_age,
                loyer_mensuel=1600,
                statut_occupation_logement="locataire",
                zone_apl=2,
                variables=variables,
            )
            datas_monoparental[f"{enfants_age} ans"] = donnees_monoparental
    return datas_biactif, datas_monoactif, datas_monoparental
