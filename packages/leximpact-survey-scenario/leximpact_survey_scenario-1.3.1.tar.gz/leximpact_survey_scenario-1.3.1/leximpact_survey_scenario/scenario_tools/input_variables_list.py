erfs_used_as_input_variables = [
    "activite",
    "autonomie_financiere",
    "categorie_salarie",
    "categorie_non_salarie",
    "chomage_brut",
    "contrat_de_travail",
    "date_naissance",
    "effectif_entreprise",
    "heures_remunerees_volume",
    "logement_conventionne",
    "loyer",
    "pensions_alimentaires_percues",
    "pensions_invalidite",
    "primes_fonction_publique",
    "retraite_brute",
    "rpns_imposables",
    "salaire_de_base",
    "statut_marital",
    "statut_occupation_logement",
    "traitement_indiciaire_brut",
    "zone_apl",
]

weights = [
    "weight_familles",
    "weight_foyers",
    "weight_individus",
    "weight_menages",
    "wprm",
]

ids = [
    # TODO Choisir une clef d'identification unique entre openfisca-survey-manager et openfisca-france-data ? :'-D
    # sachant que les valeurs existent dans openfisca-core.populations.group_population.GroupPopulation.members_entity_id
    # openfisca-france-data :
    "idfoy",
    "idfam",
    "idmen",
    "idmen_original",
]
roles = [
    # TODO comme ci dessus pour les variables d'indentifiant
    # "noindiv",  # source : ERFS-FPR
    # Removed because creates a bug with dump/restore (it is an object and not an int or a float)
    "quifoy",
    "quifam",
    "quimen",
]

variables_imputation_erfs = [
    "caseP",
    "caseT",
]

# Liste des variables qui sont injectées par Monte-Carlo et ajoutée en input variable du survey_scenario
## sous liste en fonction de la variable primaire par laquelle on impute
variables_by_revenu_individuels_100 = [
    "revenu_categoriel_foncier",
    "rente_viagere_titre_onereux_net",
    "revenus_capitaux_prelevement_bareme",
    "revenus_capitaux_prelevement_forfaitaire_unique_ir",
    "revenus_capitaux_prelevement_liberatoire",
]
variables_by_revenus_individuels_20 = [
    "assiette_csg_plus_values",
]

variables_by_revkire_par_part = ["reductions", "credits_impot", "charges_deduc"]
future_monte_carlo_variables = (
    variables_by_revenu_individuels_100
    + variables_by_revenus_individuels_20
    + variables_by_revkire_par_part
)

leximpact_used_as_input_variables = (
    erfs_used_as_input_variables
    + weights
    + ids
    + roles
    + future_monte_carlo_variables
    + variables_imputation_erfs
)
