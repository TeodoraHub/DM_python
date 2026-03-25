
import matplotlib.pyplot as plt


def plot_surrepresentation(score_departements, candidat_nom, top_n=5):
    """
    Affiche un graphique en barres horizontales des départements
    avec les plus grandes surreprésentations (en valeur absolue)
    pour un candidat donné.

    Paramètres
    ----------
    score_departements : pd.DataFrame
        DataFrame contenant les colonnes 'candidat', 'code_departement',
        'surrepresentation'.
    candidat_nom : str
        Nom complet du candidat, ex: 'Éric ZEMMOUR'.
    top_n : int
        Nombre de départements à afficher (défaut : 5).
    """
    df_candidat = score_departements[
        score_departements['candidat'] == candidat_nom
    ].copy()

    df_top = (
        df_candidat
        .assign(abs_surr=lambda x: x['surrepresentation'].abs())
        .nlargest(top_n, 'abs_surr')
        .sort_values('surrepresentation')
    )

    colors = df_top['surrepresentation'].apply(
        lambda v: 'steelblue' if v >= 0 else 'lightcoral'
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(
        df_top['code_departement'],
        df_top['surrepresentation'],
        color=colors
    )
    ax.axvline(0, color='black', linewidth=0.8)
    ax.set_xlabel('Surreprésentation')
    ax.set_ylabel('Département')

    nom = candidat_nom.split()[-1]
    ax.set_title(f'Top {top_n} des surreprésentations de {nom}')

    plt.tight_layout()
    plt.show()
