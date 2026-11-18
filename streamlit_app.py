import streamlit as st
from itertools import product
from fractions import Fraction

st.set_page_config(page_title="Misture di urne di Pólya", page_icon="🎲", layout="centered")

st.title("🎲 Misture di urne di Pólya")
st.link_button("Apri la versione online", "https://polyags.streamlit.app")
with st.container(border=True):
    st.subheader("Testo dell'esercizio")
    st.markdown("Imposta la composizione delle urne $U_1$ e $U_2$, la probabilità $P(H)$ di scegliere $U_1$ e il numero $r$ di palline dello stesso colore da aggiungere dopo ogni estrazione. Effettua $3$ estrazioni dall'urna scelta.")
    st.markdown(r"""
    **Consegne**

    1. Calcola $P(E_1)$, $P(E_2)$ e $P(E_3)$, dove $E_i$ indica che la i-esima pallina è bianca.
    2. Verifica se le tre probabilità sono uguali.
    3. Calcola $P(E_1\wedge E_2)$, $P(E_2\wedge E_3)$ e $P(E_1\wedge E_3)$.
    4. Scomponi le probabilità usando gli eventi $H$ e $H^c$, quindi determina $P(H\mid E_1)$ e $P(H\mid E_1\wedge E_2)$.
    5. Considera $X$, il numero di palline bianche estratte, e calcola $P(X=k)$ per $k=0,1,2,3$.
    6. Confronta i risultati numerici con la formula generale della mistura di urne di Pólya.
    """)
st.write(
    "Un'urna viene scelta tra U₁ e U₂ secondo la probabilità P(H). Dopo ogni estrazione, "
    "si effettuano 3 estrazioni e la pallina viene reinserita insieme a r palline dello stesso colore, "
    "dove r è il valore scelto sotto."
)

st.header("Imposta l'esercizio")
with st.container(border=True):
    st.write("Scegli la composizione delle urne, la probabilità P(H) e il numero r di palline dello stesso colore da inserire dopo ogni estrazione.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**U₁**")
        u1_white = st.number_input("Palline bianche in U₁", min_value=0, value=2, step=1, key="u1w")
        u1_black = st.number_input("Palline nere in U₁", min_value=0, value=1, step=1, key="u1b")
    with c2:
        st.markdown("**U₂**")
        u2_white = st.number_input("Palline bianche in U₂", min_value=0, value=1, step=1, key="u2w")
        u2_black = st.number_input("Palline nere in U₂", min_value=0, value=2, step=1, key="u2b")
    p_h = st.slider("P(H) = probabilità di scegliere U₁", 0.0, 1.0, 0.5, 0.05)
    reinforcement = st.number_input(
        "Palline dello stesso colore da aggiungere dopo ogni estrazione",
        min_value=-1,
        max_value=10,
        value=1,
        step=1,
    )

st.subheader("Rappresentazione delle urne")
st.caption("⚪ = pallina bianca · ⚫ = pallina nera")
visual_cols = st.columns(2)
for column, label, white, black in [
    (visual_cols[0], "U₁", u1_white, u1_black),
    (visual_cols[1], "U₂", u2_white, u2_black),
]:
    visible_white = "⚪ " * min(white, 20)
    visible_black = "⚫ " * min(black, 20)
    extra = (white + black) - min(white, 20) - min(black, 20)
    column.markdown(f"**{label}**")
    column.markdown(f"{visible_white}{visible_black}" + (f" + {extra} palline" if extra > 0 else ""))


def sequence_probability(white: int, black: int, sequence: tuple[str, ...]) -> float:
    """Probability of a colour sequence in a Pólya urn."""
    probability = 1.0
    for colour in sequence:
        total = white + black
        if total == 0:
            return 0.0
        if colour == "W":
            probability *= white / total
            white += reinforcement
        else:
            probability *= black / total
            black += reinforcement
    return probability


def sequence_factors(white: int, black: int, sequence: tuple[str, ...]) -> list[float]:
    factors = []
    for colour in sequence:
        total = white + black
        factor = white / total if colour == "W" else black / total
        factors.append(factor)
        if colour == "W":
            white += reinforcement
        else:
            black += reinforcement
    return factors


def fmt_fraction(value: float) -> str:
    fraction = Fraction(value).limit_denominator(10000)
    if fraction.denominator == 1:
        return str(fraction.numerator)
    sign = "-" if fraction.numerator < 0 else ""
    return rf"{sign}\frac{{{abs(fraction.numerator)}}}{{{fraction.denominator}}}"


def event_probability(white: int, black: int, white_positions: set[int]) -> float:
    return sum(
        sequence_probability(white, black, sequence)
        for sequence in product(("W", "B"), repeat=3)
        if all(colour == "W" for index, colour in enumerate(sequence) if index + 1 in white_positions)
    )


def mixed_event(white_positions: set[int]) -> float:
    return p_h * event_probability(u1_white, u1_black, white_positions) + (1 - p_h) * event_probability(u2_white, u2_black, white_positions)


def mixed_sequence(sequence: tuple[str, ...]) -> float:
    return p_h * sequence_probability(u1_white, u1_black, sequence) + (1 - p_h) * sequence_probability(u2_white, u2_black, sequence)


def valid_reinforcement(white: int, black: int) -> bool:
    for sequence in product(("W", "B"), repeat=3):
        current_white, current_black = white, black
        for colour in sequence:
            if current_white < 0 or current_black < 0 or current_white + current_black <= 0:
                return False
            if colour == "W":
                current_white += reinforcement
            else:
                current_black += reinforcement
    return True


if u1_white + u1_black == 0 or u2_white + u2_black == 0:
    st.error("Ogni urna deve contenere almeno una pallina.")
    st.stop()
if not valid_reinforcement(u1_white, u1_black) or not valid_reinforcement(u2_white, u2_black):
    st.error("Con questo valore di rinforzo, una delle urne potrebbe avere un numero non valido di palline. Scegli una composizione compatibile.")
    st.stop()

p_e1 = mixed_event({1})
p_e2 = mixed_event({2})
p_e3 = mixed_event({3})
p_e1e2 = mixed_event({1, 2})
p_e2e3 = mixed_event({2, 3})
p_e1e3 = mixed_event({1, 3})
p_e3e2e1 = mixed_sequence(("W", "W", "W"))
p_e3e2e1c = mixed_sequence(("B", "W", "W"))
p_e3e2ce1 = mixed_sequence(("W", "B", "W"))
p_e3e2ce1c = mixed_sequence(("B", "B", "W"))
p_e3e2e1_h = p_h * sequence_probability(u1_white, u1_black, ("W", "W", "W"))
p_e3e2e1_hc = (1 - p_h) * sequence_probability(u2_white, u2_black, ("W", "W", "W"))
p_e3e2e1c_h = p_h * sequence_probability(u1_white, u1_black, ("B", "W", "W"))
p_e3e2e1c_hc = (1 - p_h) * sequence_probability(u2_white, u2_black, ("B", "W", "W"))
p_e3e2ce1_h = p_h * sequence_probability(u1_white, u1_black, ("W", "B", "W"))
p_e3e2ce1_hc = (1 - p_h) * sequence_probability(u2_white, u2_black, ("W", "B", "W"))
p_e3e2ce1c_h = p_h * sequence_probability(u1_white, u1_black, ("B", "B", "W"))
p_e3e2ce1c_hc = (1 - p_h) * sequence_probability(u2_white, u2_black, ("B", "B", "W"))
p_h_given_e1 = p_h * event_probability(u1_white, u1_black, {1}) / p_e1 if p_e1 else 0.0
p_h_given_e1e2 = p_h * event_probability(u1_white, u1_black, {1, 2}) / p_e1e2 if p_e1e2 else 0.0
x_distribution = {
    count: sum(
        urn_probability * sequence_probability(white, black, sequence)
        for urn_probability, white, black in [
            (p_h, u1_white, u1_black),
            (1 - p_h, u2_white, u2_black),
        ]
        for sequence in product(("W", "B"), repeat=3)
        if sequence.count("W") == count
    )
    for count in range(4)
}

st.header("Risultati per i dati scelti")
result_cols = st.columns(3)
for column, label, value in zip(result_cols, ["P(E₁)", "P(E₂)", "P(E₃)"], [p_e1, p_e2, p_e3]):
    column.latex(rf"{label} = {fmt_fraction(value)}")
st.latex(rf"P(E_1\wedge E_2)={fmt_fraction(p_e1e2)},\qquad P(E_2\wedge E_3)={fmt_fraction(p_e2e3)},\qquad P(E_1\wedge E_3)={fmt_fraction(p_e1e3)}")
st.latex(rf"P(H\mid E_1)={fmt_fraction(p_h_given_e1)},\qquad P(H\mid E_1\wedge E_2)={fmt_fraction(p_h_given_e1e2)}")
st.write("Sia (X)  il numero di palline bianche estratte nelle tre estrazioni:")
st.latex(rf"P(X=0)={fmt_fraction(x_distribution[0])},\qquad P(X=1)={fmt_fraction(x_distribution[1])}")
st.latex(rf"P(X=2)={fmt_fraction(x_distribution[2])},\qquad P(X=3)={fmt_fraction(x_distribution[3])}")
st.subheader("Distribuzione grafica di X")
st.bar_chart(
    {"P(X=k)": [x_distribution[k] for k in range(4)]},
    x_label="k = numero di palline bianche",
    y_label="P(X = k)",
)
if (u1_white, u1_black, u2_white, u2_black, p_h) != (2, 1, 1, 2, 0.5):
    with st.expander("Formula generale usata dal calcolo"):
        st.latex(r"P(E_1\wedge E_2\wedge H)=P(E_2\mid E_1\wedge H)P(E_1\mid H)P(H)")
        st.latex(r"P(E_1\wedge E_2)=P(E_1\wedge E_2\wedge H)+P(E_1\wedge E_2\wedge H^{c})")
        st.latex(r"P(H\mid E_1)=\frac{P(E_1\mid H)P(H)}{P(E_1)}")

with st.container(border=True):
    st.subheader("Dati dell'esercizio")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**U₁**")
        st.write(f"{u1_white} palline bianche e {u1_black} nere")
    with col2:
        st.markdown("**U₂**")
        st.write(f"{u2_white} palline bianche e {u2_black} nere")
    st.caption("H = scelta di U₁ · Hᶜ = scelta di U₂ · Eᵢ = i-esima estrazione bianca")

st.header("Le tue risposte")
with st.form("answers"):
    marginali = st.radio(
        "1. P(E₁) = P(E₂) = P(E₃)?",
        ["Sì", "No"],
        horizontal=True,
    )
    congiunte = st.radio(
        "2. P(E₁∩E₂) = P(E₂∩E₃) = P(E₁∩E₃)?",
        ["Sì", "No"],
        horizontal=True,
    )
    col1, col2 = st.columns(2)
    with col1:
        bayes_1 = st.text_input("P(H | E₁)", placeholder="es. 2/3")
    with col2:
        bayes_2 = st.text_input("P(H | E₁∩E₂)", placeholder="es. 3/4")
    submitted = st.form_submit_button("Verifica risposte", type="primary")


def answer_value(value: str) -> float | None:
    try:
        value = value.strip().replace(",", ".")
        if "/" in value:
            n, d = value.split("/", 1)
            return float(n) / float(d)
        return float(value)
    except (ValueError, ZeroDivisionError):
        return None


if submitted:
    answer_1 = answer_value(bayes_1)
    answer_2 = answer_value(bayes_2)
    correct = (
        (marginali == "Sì") == (abs(p_e1 - p_e2) < 1e-9 and abs(p_e2 - p_e3) < 1e-9)
        and (congiunte == "Sì") == (abs(p_e1e2 - p_e2e3) < 1e-9 and abs(p_e2e3 - p_e1e3) < 1e-9)
        and answer_1 is not None and abs(answer_1 - p_h_given_e1) < 1e-9
        and answer_2 is not None and abs(answer_2 - p_h_given_e1e2) < 1e-9
    )
    if correct:
        st.success("Tutto corretto! Ottimo lavoro.")
    else:
        st.error("Alcune risposte non coincidono. Consulta i passaggi qui sotto.")

st.divider()
st.header("Soluzione passo-passo per i dati scelti")

u1_total = u1_white + u1_black
u2_total = u2_white + u2_black
u1_e1 = u1_white / u1_total
u2_e1 = u2_white / u2_total
u1_e2_after_e1 = (u1_white + reinforcement) / (u1_total + reinforcement)
u2_e2_after_e1 = (u2_white + reinforcement) / (u2_total + reinforcement)
u1_e2_after_e1c = u1_white / (u1_total + reinforcement)
u2_e2_after_e1c = u2_white / (u2_total + reinforcement)
u1_e1e2h = p_h * u1_e1 * u1_e2_after_e1
u2_e1e2hc = (1 - p_h) * u2_e1 * u2_e2_after_e1
u1_e1c_e2h = p_h * (1 - u1_e1) * u1_e2_after_e1c
u2_e1c_e2hc = (1 - p_h) * (1 - u2_e1) * u2_e2_after_e1c
u1_e1e2_cond_h = event_probability(u1_white, u1_black, {1, 2})

with st.expander("1. Probabilità delle singole estrazioni", expanded=True):
    st.write("La scelta dell'urna ha probabilità impostata dall'utente:")
    st.latex(r"P(H)=p(H),\qquad P(H^{c})=1-p(H)")
    st.latex(fr"P(H)={fmt_fraction(p_h)},\qquad P(H^c)={fmt_fraction(1-p_h)}")
    st.write("Per la prima estrazione:")
    st.latex(fr"P(E_1)=P(E_1\mid H)P(H)+P(E_1\mid H^c)P(H^c)={fmt_fraction(u1_e1)}\cdot{fmt_fraction(p_h)}+{fmt_fraction(u2_e1)}\cdot{fmt_fraction(1-p_h)}={fmt_fraction(p_e1)}")
    st.write("Per la seconda estrazione, scomponendo rispetto a (E_1):")
    st.latex(r"P(E_2)=P(E_2\wedge E_1)+P(E_2\wedge E_1^c)")
    st.latex(fr"P(E_2\wedge E_1\wedge H)=P(E_2\mid E_1\wedge H)P(E_1\mid H)P(H)={fmt_fraction(u1_e2_after_e1)}\cdot{fmt_fraction(u1_e1)}\cdot{fmt_fraction(p_h)}={fmt_fraction(u1_e1e2h)}")
    st.latex(fr"P(E_2\wedge E_1\wedge H^c)=P(E_2\mid E_1\wedge H^c)P(E_1\mid H^c)P(H^c)={fmt_fraction(u2_e2_after_e1)}\cdot{fmt_fraction(u2_e1)}\cdot{fmt_fraction(1-p_h)}={fmt_fraction(u2_e1e2hc)}")
    st.latex(fr"P(E_2\wedge E_1)={fmt_fraction(u1_e1e2h)}+{fmt_fraction(u2_e1e2hc)}={fmt_fraction(p_e1e2)}")
    st.latex(fr"P(E_2\wedge E_1^c\wedge H)=P(E_2\mid E_1^c\wedge H)P(E_1^c\mid H)P(H)={fmt_fraction(u1_e2_after_e1c)}\cdot{fmt_fraction(1-u1_e1)}\cdot{fmt_fraction(p_h)}={fmt_fraction(u1_e1c_e2h)}")
    st.latex(fr"P(E_2\wedge E_1^c\wedge H^c)=P(E_2\mid E_1^c\wedge H^c)P(E_1^c\mid H^c)P(H^c)={fmt_fraction(u2_e2_after_e1c)}\cdot{fmt_fraction(1-u2_e1)}\cdot{fmt_fraction(1-p_h)}={fmt_fraction(u2_e1c_e2hc)}")
    st.latex(fr"P(E_2\wedge E_1^c)={fmt_fraction(u1_e1c_e2h)}+{fmt_fraction(u2_e1c_e2hc)}={fmt_fraction(p_e2-p_e1e2)}")
    st.latex(fr"P(E_2)={fmt_fraction(p_e1e2)}+{fmt_fraction(p_e2-p_e1e2)}={fmt_fraction(p_e2)}")
    st.write("Per la terza estrazione, scomponiamo rispetto ai risultati delle prime due estrazioni:")
    st.latex(r"P(E_3)=P(E_3\wedge E_2\wedge E_1)+P(E_3\wedge E_2\wedge E_1^c)+P(E_3\wedge E_2^c\wedge E_1)+P(E_3\wedge E_2^c\wedge E_1^c)")
    st.latex(fr"P(E_3\wedge E_2\wedge E_1)=P(E_3\wedge E_2\wedge E_1\wedge H)+P(E_3\wedge E_2\wedge E_1\wedge H^c)")
    st.latex(fr"P(E_3\wedge E_2\wedge E_1\wedge H)={fmt_fraction(p_e3e2e1_h)},\qquad P(E_3\wedge E_2\wedge E_1\wedge H^c)={fmt_fraction(p_e3e2e1_hc)}")
    st.latex(fr"P(E_3\wedge E_2\wedge E_1)={fmt_fraction(p_e3e2e1_h)}+{fmt_fraction(p_e3e2e1_hc)}={fmt_fraction(p_e3e2e1)}")
    st.latex(r"P(E_3\wedge E_2\wedge E_1^c)=P(E_3\wedge E_2\wedge E_1^c\wedge H)+P(E_3\wedge E_2\wedge E_1^c\wedge H^c)")
    st.latex(fr"P(E_3\wedge E_2\wedge E_1^c\wedge H)={fmt_fraction(p_e3e2e1c_h)},\qquad P(E_3\wedge E_2\wedge E_1^c\wedge H^c)={fmt_fraction(p_e3e2e1c_hc)}")
    st.latex(fr"P(E_3\wedge E_2\wedge E_1^c)={fmt_fraction(p_e3e2e1c_h)}+{fmt_fraction(p_e3e2e1c_hc)}={fmt_fraction(p_e3e2e1c)}")
    st.latex(r"P(E_3\wedge E_2^c\wedge E_1)=P(E_3\wedge E_2^c\wedge E_1\wedge H)+P(E_3\wedge E_2^c\wedge E_1\wedge H^c)")
    st.latex(fr"P(E_3\wedge E_2^c\wedge E_1\wedge H)={fmt_fraction(p_e3e2ce1_h)},\qquad P(E_3\wedge E_2^c\wedge E_1\wedge H^c)={fmt_fraction(p_e3e2ce1_hc)}")
    st.latex(fr"P(E_3\wedge E_2^c\wedge E_1)={fmt_fraction(p_e3e2ce1_h)}+{fmt_fraction(p_e3e2ce1_hc)}={fmt_fraction(p_e3e2ce1)}")
    st.latex(r"P(E_3\wedge E_2^c\wedge E_1^c)=P(E_3\wedge E_2^c\wedge E_1^c\wedge H)+P(E_3\wedge E_2^c\wedge E_1^c\wedge H^c)")
    st.latex(fr"P(E_3\wedge E_2^c\wedge E_1^c\wedge H)={fmt_fraction(p_e3e2ce1c_h)},\qquad P(E_3\wedge E_2^c\wedge E_1^c\wedge H^c)={fmt_fraction(p_e3e2ce1c_hc)}")
    st.latex(fr"P(E_3\wedge E_2^c\wedge E_1^c)={fmt_fraction(p_e3e2ce1c_h)}+{fmt_fraction(p_e3e2ce1c_hc)}={fmt_fraction(p_e3e2ce1c)}")
    st.latex(fr"P(E_3)={fmt_fraction(p_e3e2e1)}+{fmt_fraction(p_e3e2e1c)}+{fmt_fraction(p_e3e2ce1)}+{fmt_fraction(p_e3e2ce1c)}={fmt_fraction(p_e3)}")
    st.latex(fr"P(E_1)={fmt_fraction(p_e1)},\qquad P(E_2)={fmt_fraction(p_e2)},\qquad P(E_3)={fmt_fraction(p_e3)}")
    st.info("L'uguaglianza delle tre probabilità è " + ("vera." if abs(p_e1-p_e2)<1e-9 and abs(p_e2-p_e3)<1e-9 else "falsa."))

with st.expander("2. Probabilità congiunte"):
    st.write("Per le tre probabilità congiunte, esplicitiamo prima la scomposizione degli eventi:")
    st.latex(r"P(E_1\wedge E_2)=P(E_1\wedge E_2\wedge H)+P(E_1\wedge E_2\wedge H^c)")
    st.latex(r"P(E_2\wedge E_3)=P(E_3\wedge E_2\wedge E_1)+P(E_3\wedge E_2\wedge E_1^c)")
    st.latex(r"P(E_1\wedge E_3)=P(E_3\wedge E_2\wedge E_1)+P(E_3\wedge E_2^c\wedge E_1)")
    st.latex(fr"P(E_1\wedge E_2\wedge H)={fmt_fraction(u1_e1e2h)},\qquad P(E_1\wedge E_2\wedge H^c)={fmt_fraction(u2_e1e2hc)}")
    st.latex(fr"P(E_1\wedge E_2)={fmt_fraction(u1_e1e2h)}+{fmt_fraction(u2_e1e2hc)}={fmt_fraction(p_e1e2)}")
    st.latex(fr"P(E_2\wedge E_3)=P(E_3\wedge E_2\wedge E_1)+P(E_3\wedge E_2\wedge E_1^c)")
    st.latex(fr"P(E_3\wedge E_2\wedge E_1)={fmt_fraction(p_e3e2e1_h)}+{fmt_fraction(p_e3e2e1_hc)}={fmt_fraction(p_e3e2e1)}")
    st.latex(fr"P(E_3\wedge E_2\wedge E_1^c)={fmt_fraction(p_e3e2e1c_h)}+{fmt_fraction(p_e3e2e1c_hc)}={fmt_fraction(p_e3e2e1c)}")
    st.latex(fr"P(E_2\wedge E_3)={fmt_fraction(p_e3e2e1)}+{fmt_fraction(p_e3e2e1c)}={fmt_fraction(p_e2e3)}")
    st.latex(fr"P(E_1\wedge E_3)=P(E_3\wedge E_2\wedge E_1)+P(E_3\wedge E_2^c\wedge E_1)")
    st.latex(fr"P(E_3\wedge E_2^c\wedge E_1)={fmt_fraction(p_e3e2ce1_h)}+{fmt_fraction(p_e3e2ce1_hc)}={fmt_fraction(p_e3e2ce1)}")
    st.latex(fr"P(E_1\wedge E_3)={fmt_fraction(p_e3e2e1)}+{fmt_fraction(p_e3e2ce1)}={fmt_fraction(p_e1e3)}")
    st.info("L'uguaglianza delle tre probabilità congiunte è " + ("vera." if abs(p_e1e2-p_e2e3)<1e-9 and abs(p_e2e3-p_e1e3)<1e-9 else "falsa."))

with st.expander("3. Probabilità condizionate (teorema di Bayes)"):
    st.latex(fr"P(H\mid E_1)=\frac{{P(E_1\mid H)P(H)}}{{P(E_1)}}=\frac{{{fmt_fraction(u1_e1)}\cdot{fmt_fraction(p_h)}}}{{{fmt_fraction(p_e1)}}}={fmt_fraction(p_h_given_e1)}")
    st.latex(fr"P(H\mid E_1\wedge E_2)=\frac{{P(E_1\wedge E_2\mid H)P(H)}}{{P(E_1\wedge E_2)}}=\frac{{{fmt_fraction(u1_e1e2_cond_h)}\cdot{fmt_fraction(p_h)}}}{{{fmt_fraction(p_e1e2)}}}={fmt_fraction(p_h_given_e1e2)}")

with st.expander("4. I 16 costituenti", expanded=False):
    st.write("Ogni costituente specifica se ciascuna estrazione è bianca (Eᵢ) o nera (Eᵢᶜ), insieme alla scelta dell'urna H o Hᶜ.")
    for urn_event, urn_probability, white, black in [
        ("H", p_h, u1_white, u1_black),
        ("H^c", 1 - p_h, u2_white, u2_black),
    ]:
        st.markdown(f"**Caso {urn_event}**")
        for sequence in product(("W", "B"), repeat=3):
            event_parts = [f"E_{index}" if sequence[index - 1] == "W" else f"E_{index}^c" for index in (3, 2, 1)]
            event_name = r"\wedge ".join(event_parts)
            factors = sequence_factors(white, black, sequence)
            probability = urn_probability * factors[0] * factors[1] * factors[2]
            product_text = r"\cdot ".join([fmt_fraction(urn_probability), *(fmt_fraction(factor) for factor in factors)])
            st.latex(fr"P({event_name}\wedge {urn_event})={product_text}={fmt_fraction(probability)}")

with st.expander("5. Distribuzione di X", expanded=False):
    st.write("Sia X il numero di palline bianche nelle tre estrazioni. Usiamo i 16 costituenti della sezione precedente.")
    for white_count in range(4):
        terms = []
        total_probability = 0.0
        for urn_event, urn_probability, white, black in [
            ("H", p_h, u1_white, u1_black),
            ("H^c", 1 - p_h, u2_white, u2_black),
        ]:
            for sequence in product(("W", "B"), repeat=3):
                if sequence.count("W") != white_count:
                    continue
                probability = urn_probability * sequence_probability(white, black, sequence)
                event_parts = [f"E_{index}" if sequence[index - 1] == "W" else f"E_{index}^c" for index in (3, 2, 1)]
                event_name = r"\wedge ".join(event_parts)
                terms.append((event_name, urn_event, probability))
                total_probability += probability
        st.markdown(f"**X = {white_count}**")
        st.latex(fr"P(X={white_count})=" + "+".join(fr"P({event}\wedge {urn})" for event, urn, _ in terms))
        st.latex("+".join(fmt_fraction(probability) for _, _, probability in terms) + fr"={fmt_fraction(total_probability)}")

with st.expander("6. Formula generale della distribuzione di Pólya", expanded=False):
    st.write("Indichiamo con B il numero iniziale di palline bianche, con N il numero iniziale di palline nere, con n il numero di estrazioni e con r il numero di palline dello stesso colore aggiunte dopo ogni estrazione.")
    st.latex(r"X=\text{numero di palline bianche estratte in }n\text{ estrazioni}")
    st.latex(r"(a)_{k,r}=a(a+r)(a+2r)\cdots(a+(k-1)r),\qquad (a)_{0,r}=1")
    st.latex(r"P(X=k\mid H)=\binom{n}{k}\frac{(B_1)_{k,r}(N_1)_{n-k,r}}{(B_1+N_1)_{n,r}}")
    st.latex(r"P(X=k\mid H^c)=\binom{n}{k}\frac{(B_2)_{k,r}(N_2)_{n-k,r}}{(B_2+N_2)_{n,r}}")
    st.latex(r"P(X=k)=P(H)P(X=k\mid H)+[1-P(H)]P(X=k\mid H^c),\qquad k=0,1,\ldots,n")
    st.write("Nel caso r = 0, la formula si riduce alla mistura di due distribuzioni binomiali:")
    st.latex(r"P(X=k\mid H)=\binom{n}{k}\left(\frac{B_1}{B_1+N_1}\right)^k\left(\frac{N_1}{B_1+N_1}\right)^{n-k}")
    st.latex(r"P(X=k\mid H^c)=\binom{n}{k}\left(\frac{B_2}{B_2+N_2}\right)^k\left(\frac{N_2}{B_2+N_2}\right)^{n-k}")
    st.write("Nel caso r = -1, dopo ogni estrazione si rimuove una pallina dello stesso colore: si ottiene una mistura di distribuzioni ipergeometriche.")
    st.latex(r"P(X=k\mid H)=\frac{\binom{B_1}{k}\binom{N_1}{n-k}}{\binom{B_1+N_1}{n}},\qquad P(X=k\mid H^c)=\frac{\binom{B_2}{k}\binom{N_2}{n-k}}{\binom{B_2+N_2}{n}}")
    st.latex(r"P(X=k)=P(H)P(X=k\mid H)+[1-P(H)]P(X=k\mid H^c)")

st.caption("Puoi eseguire l'app con: streamlit run streamlit_app.py")
st.divider()
st.caption("Autore: Giuseppe Sanfilippo")
