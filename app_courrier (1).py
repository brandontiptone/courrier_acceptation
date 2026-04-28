"""
Application Streamlit — Générateur de Courrier d'Acceptation
Panneau photovoltaïque — Bureau Technique Énergétique
"""

import io
import streamlit as st
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER

# ─────────────────────────────────────────────
# CONFIG PAGE
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Courrier d'Acceptation",
    page_icon="☀️",
    layout="centered"
)

st.markdown("""
<style>
    .stApp { background-color: #1e1e2e; color: #cdd6f4; }
    h1, h2, h3 { color: #89b4fa; }
    .stButton > button {
        background-color: #89b4fa; color: #1e1e2e;
        font-weight: bold; border-radius: 8px;
        border: none; padding: 0.5rem 2rem;
        width: 100%;
    }
    .stButton > button:hover { background-color: #74c7ec; }
    .stDownloadButton > button {
        background-color: #a6e3a1; color: #1e1e2e;
        font-weight: bold; border-radius: 8px;
        border: none; width: 100%;
        font-size: 1.1rem; padding: 0.6rem;
    }
    label { color: #cdd6f4 !important; }
    .stTextInput input, .stNumberInput input {
        background-color: #181825 !important;
        color: #cdd6f4 !important;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TITRE
# ─────────────────────────────────────────────

st.title("☀️ Générateur de Courrier d'Acceptation")
st.markdown("**Bureau Technique Énergétique — Installation photovoltaïque**")
st.divider()

# ─────────────────────────────────────────────
# FORMULAIRE
# ─────────────────────────────────────────────

st.header("📝 Informations du dossier")

col1, col2 = st.columns(2)
with col1:
    date_dossier = st.date_input("Date de création du dossier", value=datetime.today())
    prime = st.number_input("Prime à l'investissement (€)", min_value=0, value=0, step=100)
with col2:
    adresse = st.text_input("Adresse complète", placeholder="Ex : 12 rue des Lilas, 87000 Limoges")
    tva = st.number_input("Récupération de TVA (€)", min_value=0, value=0, step=100)

subvention = prime + tva
st.info(f"💰 Subvention globale calculée automatiquement : **{subvention:,.0f} €** (Prime + TVA)".replace(",", " "))

st.divider()

# ─────────────────────────────────────────────
# GÉNÉRATION PDF
# ─────────────────────────────────────────────

def generer_pdf(date_dossier, adresse, subvention, prime, tva):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2.5*cm,
        leftMargin=2.5*cm,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm
    )

    styles = getSampleStyleSheet()
    bleu = colors.HexColor("#1F4E79")

    style_normal = ParagraphStyle(
        "normal_fr",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=16,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        textColor=colors.HexColor("#1a1a1a")
    )
    style_titre = ParagraphStyle(
        "titre",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=bleu,
        spaceBefore=14,
        spaceAfter=6
    )
    style_entete = ParagraphStyle(
        "entete",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=bleu,
        alignment=TA_CENTER,
        spaceAfter=6
    )
    style_sous_entete = ParagraphStyle(
        "sous_entete",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        textColor=colors.HexColor("#555555"),
        alignment=TA_CENTER,
        spaceAfter=4
    )
    style_salutation = ParagraphStyle(
        "salutation",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=16,
        alignment=TA_LEFT,
        spaceAfter=8,
        textColor=colors.HexColor("#1a1a1a")
    )

    # Formatage des valeurs
    import locale
    MOIS_FR = {
        1: "janvier", 2: "février", 3: "mars", 4: "avril",
        5: "mai", 6: "juin", 7: "juillet", 8: "août",
        9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre"
    }
    date_str = date_dossier.strftime("%d/%m/%Y")
    mois_str = f"{MOIS_FR[date_dossier.month]} {date_dossier.year}"
    today = datetime.today()
    date_generation = f"{today.day} {MOIS_FR[today.month]} {today.year}"
    sub_str  = f"{subvention:,.0f}".replace(",", " ")
    prime_str = f"{prime:,.0f}".replace(",", " ")
    tva_str  = f"{tva:,.0f}".replace(",", " ")

    story = []

    # En-tête
    story.append(Paragraph("BUREAU TECHNIQUE ÉNERGÉTIQUE", style_entete))
    story.append(Paragraph("Installation Photovoltaïque — Courrier d'Acceptation", style_sous_entete))
    story.append(Paragraph(f"Généré le {date_generation}", style_sous_entete))
    story.append(Spacer(1, 0.4*cm))

    # Ligne de séparation visuelle
    from reportlab.platypus import HRFlowable
    story.append(HRFlowable(width="100%", thickness=1.5, color=bleu))
    story.append(Spacer(1, 0.5*cm))

    # Date et destinataire
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Monsieur, Madame,", style_salutation))
    story.append(Spacer(1, 0.4*cm))

    # Corps du courrier
    story.append(Paragraph(
        f"Nous avons le plaisir de vous informer que votre dossier, créé le {mois_str} dernier, "
        f"a été accepté pour l'installation de votre centrale photovoltaïque avec un système de "
        f"micro-onduleurs à votre domicile situé au <b>{adresse}</b>.",
        style_normal
    ))

    story.append(Paragraph(
        "Sachez que votre habitation devient ainsi l'une de nos maisons partenaires, vous donnant droit "
        "à une collaboration privilégiée. Nous sommes ravis de vous offrir cette opportunité et de vous "
        "compter parmi nos clients les plus estimés.",
        style_normal
    ))

    story.append(Paragraph(
        "Une étude de faisabilité a été minutieusement menée par nos différents services et partenaires. "
        "Cette étude approfondie nous a permis d'apporter et de valider l'ensemble des éléments techniques "
        "et financiers nécessaires à la réalisation de ce projet ambitieux. Elle a inclus une analyse détaillée "
        "de l'ensoleillement de votre emplacement, l'évaluation de la structure de votre toit, et une étude "
        "de l'impact financier sur votre consommation d'énergie actuelle et future.",
        style_normal
    ))

    # Étapes
    story.append(Paragraph("Détails de l'Installation :", style_titre))

    story.append(Paragraph("Étape 1 : Pré-Installation Technique", style_titre))
    story.append(Paragraph(
        "Avant de débuter l'installation de votre centrale photovoltaïque, une pré-visite technique sera "
        "effectuée par nos techniciens pour s'assurer que toutes les conditions sont réunies pour une "
        "installation optimale.",
        style_normal
    ))
    story.append(Paragraph("<b>1. Pré-Visite Technique :</b>", style_normal))
    story.append(Paragraph(
        "Nos techniciens se rendront à votre domicile pour effectuer une pré-visite technique d'une durée "
        "de 45 minutes approximatives. Cette visite permettra de vérifier une dernière fois les conditions "
        "du site et de s'assurer que tout est prêt pour l'installation.",
        style_normal
    ))
    story.append(Paragraph(
        "Les techniciens évalueront l'accessibilité du toit, la solidité de la structure, et s'assureront "
        "qu'aucun obstacle ne pourrait gêner l'installation des panneaux solaires. Ils vérifieront également "
        "l'emplacement des équipements électriques et des connexions nécessaires pour garantir une intégration "
        "harmonieuse avec votre système électrique existant.",
        style_normal
    ))
    story.append(Paragraph("<b>2. Esthétique de l'Installation :</b>", style_normal))
    story.append(Paragraph(
        "Un aspect crucial de la pré-visite technique est de garantir l'esthétique de l'installation. "
        "Nos techniciens s'assureront que les panneaux solaires sont installés de manière à minimiser leur "
        "impact visuel et à s'intégrer harmonieusement avec le design de votre maison. Les câbles et autres "
        "équipements seront soigneusement dissimulés ou intégrés de manière discrète pour préserver "
        "l'apparence de votre domicile.",
        style_normal
    ))

    story.append(Paragraph("Étape 2 : Garanties et Visite Préventive", style_titre))
    story.append(Paragraph("<b>1. Garantie de performance linéaire de 80% pendant 25 ans :</b>", style_normal))
    story.append(Paragraph(
        "Incluant les pièces, la main-d'œuvre et les déplacements. Cette garantie vous offre une tranquillité "
        "d'esprit et assure le bon fonctionnement de votre installation sur le long terme. En cas de panne ou "
        "de dysfonctionnement, notre équipe interviendra rapidement pour résoudre le problème sans frais "
        "supplémentaires pour vous.",
        style_normal
    ))
    story.append(Paragraph("<b>2. Visite préventive (pendant 20 ans) :</b>", style_normal))
    story.append(Paragraph(
        "Vous bénéficierez d'une visite préventive effectuée par nos techniciens, prise en charge par notre "
        "entreprise pendant 20 ans, comprenant : inspection visuelle des modules, nettoyage des modules, "
        "vérification des micro-onduleurs, inspection du coffret AC et de la passerelle de communication, "
        "tests électriques, signalétique et relevé des données de production.",
        style_normal
    ))

    story.append(Paragraph("Étape 3 : Raccordement au Réseau ENEDIS", style_titre))
    story.append(Paragraph(
        "Une fois l'installation terminée, nous procéderons au raccordement de votre système au réseau ENEDIS, "
        "incluant la pose des compteurs de production, le raccordement au réseau et la mise en service complète "
        "de votre installation. Conformément à notre contrat, l'intégralité des frais de raccordement est prise "
        "en charge par notre groupe.",
        style_normal
    ))

    story.append(Paragraph("Étape 4 : Avantages Financiers et Subventions", style_titre))
    story.append(Paragraph(
        "Après ces étapes, vous recevrez votre contrat d'obligation de rachat d'électricité ENEDIS, "
        "d'une durée de 20 ans, concernant la revente de votre surplus d'électricité. "
        "Voici les détails des avantages financiers auxquels vous aurez droit :",
        style_normal
    ))
    story.append(Paragraph(
        f"<b>1. Subvention globale :</b> Votre installation vous permettra de percevoir une enveloppe globale "
        f"à hauteur de <b>{sub_str} euros</b> pour soutenir la transition énergétique.",
        style_normal
    ))
    story.append(Paragraph(
        f"<b>2. Prime à l'investissement :</b> Grâce à votre mode de production en autoconsommation avec "
        f"revente du surplus, vous percevrez une prime à l'investissement de <b>{prime_str} euros</b>, "
        f"versée en 1 fois.",
        style_normal
    ))
    story.append(Paragraph(
        f"<b>3. Récupération de TVA :</b> La récupération de TVA à hauteur de <b>{tva_str} euros</b> "
        f"allègera davantage le coût total de votre projet.",
        style_normal
    ))

    # Conclusion
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph(
        "Nous vous remercions pour la confiance que vous nous accordez et espérons que notre collaboration "
        "vous apportera entière satisfaction. Nous restons à votre disposition pour toute question ou "
        "information complémentaire concernant votre projet.",
        style_normal
    ))
    story.append(Spacer(1, 0.6*cm))
    story.append(Paragraph(
        "Veuillez agréer, Monsieur, Madame, l'expression de nos salutations distinguées.",
        style_normal
    ))
    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph("<b>Cordialement,</b>", style_salutation))
    story.append(Paragraph("<b>Bureau Technique Énergétique.</b>", style_salutation))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()


# ─────────────────────────────────────────────
# BOUTON GÉNÉRATION
# ─────────────────────────────────────────────

if st.button("📄 Générer le courrier"):
    if not adresse.strip():
        st.error("❌ Veuillez saisir l'adresse complète.")
    else:
        with st.spinner("Génération du PDF en cours..."):
            pdf_bytes = generer_pdf(date_dossier, adresse, subvention, prime, tva)

        st.success("✅ Courrier généré avec succès !")

        nom_fichier = f"Courrier_acceptation_{date_dossier.strftime('%d-%m-%Y')}.pdf"
        st.download_button(
            label="⬇️ Télécharger le Courrier d'Acceptation",
            data=pdf_bytes,
            file_name=nom_fichier,
            mime="application/pdf"
        )
