
import folium
# import pandas as pd
from branca.colormap import LinearColormap
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors


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


def plot_carte_statique(df_candidat, departement_borders, candidat_nom):

    gdf = departement_borders.merge(
        df_candidat[['code_departement', 'surrepresentation']],
        left_on='INSEE_DEP',
        right_on='code_departement',
        how='left'
    )

    gdf['surrepresentation'] = gdf['surrepresentation'].fillna(0)

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    vmax = gdf['surrepresentation'].abs().max()

    gdf.plot(
        column='surrepresentation',
        cmap='RdBu_r',
        vmin=-vmax,
        vmax=vmax,
        linewidth=0.5,
        edgecolor='black',
        legend=True,
        legend_kwds={
            'label': "% par rapport à la moyenne nationale",
            'shrink': 0.3,
            'aspect': 60
        },
        ax=ax
    )
    ax.axis('off')

    return fig


def plot_carte_dym(df_candidat, departement_borders, candidat_nom):

    gdf = departement_borders.merge(
        df_candidat[['code_departement', 'surrepresentation']],
        left_on='INSEE_DEP',
        right_on='code_departement',
        how='left'
    )

    gdf['surrepresentation'] = gdf['surrepresentation'].fillna(0)
    cmap = cm.get_cmap('RdBu_r', 256)
    colors = [mcolors.rgb2hex(cmap(i)) for i in range(cmap.N)]

    valeur_max = gdf['surrepresentation'].abs().max()

    colormap = LinearColormap(
        colors=colors,
        vmin=-valeur_max,
        vmax=valeur_max,
        caption=f'Surreprésentation (%) par rapport à la moyenne nationale — {candidat_nom}'
    )

    m = folium.Map(location=[46.5, 2.5], zoom_start=6, tiles='CartoDB positron')
    folium.GeoJson(
        gdf,
        style_function=lambda feature: {
            'fillColor': colormap(feature['properties']['surrepresentation']),
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.7,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['INSEE_DEP', 'LIBELLE_DEPARTEMENT', 'surrepresentation'],
            aliases=['Département', 'Libellé', 'Surreprésentation (%)'],
        )
    ).add_to(m)

    colormap.add_to(m)

    return m
