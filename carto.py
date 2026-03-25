
import folium
import pandas as pd
from branca.colormap import LinearColormap


def filtrer_candidat(score_departements, candidat_nom):
    """
    Filtre score_departements pour un candidat donné.

    Paramètres
    ----------
    score_departements : pd.DataFrame
    candidat_nom : str, ex: 'Marine LE PEN'

    Retourne
    --------
    pd.DataFrame filtré sur le candidat
    """
    return score_departements[
        score_departements['candidat'] == candidat_nom
    ].copy()


def plot_carte(df_candidat, departement_borders, candidat_nom):
    """
    Fait la jointure avec le fond de carte et affiche une carte
    choroplèthe de la surreprésentation par département.

    Paramètres
    ----------
    df_candidat : pd.DataFrame
        Résultat de filtrer_candidat().
    departement_borders : GeoDataFrame
        Fond de carte cartiflette.
    candidat_nom : str
        Nom complet du candidat pour le titre.
    """
    # Jointure fond de carte + données
    gdf = departement_borders.merge(
        df_candidat[['code_departement', 'surrepresentation']],
        left_on='INSEE_DEP',
        right_on='code_departement',
        how='left'
    )

    # Palette rouge/blanc/bleu centrée sur 0
    valeur_max = gdf['surrepresentation'].abs().max()
    colormap = LinearColormap(
        colors=['blue', 'white', 'red'],
        vmin=-valeur_max,
        vmax=valeur_max,
        caption=f'Surreprésentation (%) par rapport à la moyenne nationale — {candidat_nom}'
    )

    # Carte centrée sur la France
    m = folium.Map(location=[46.5, 2.5], zoom_start=6, tiles='CartoDB positron')

    # Ajout des départements
    folium.GeoJson(
        gdf,
        style_function=lambda feature: {
            'fillColor': colormap(feature['properties']['surrepresentation'])
                         if feature['properties']['surrepresentation'] is not None
                         else 'grey',
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.7,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['INSEE_DEP', 'LIBELLE_DEPARTEMENT', 'surrepresentation'],
            aliases=['Département', 'Libellé', 'Surreprésentation (%)'],
            localize=True
        )
    ).add_to(m)

    colormap.add_to(m)

    return m
