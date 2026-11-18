# Misture di urne di Pólya — app interattiva

App didattica per studiare le probabilità associate a due urne di Pólya.

## App online

[Apri l'app su Streamlit](https://polyags.streamlit.app)

## Funzionalità

- scelta del numero di palline bianche e nere nelle due urne;
- scelta della probabilità P(H) di selezionare l'urna U_1;
- scelta del numero di palline dello stesso colore da aggiungere dopo ogni estrazione, da -1 a 10;
- verifica interattiva delle risposte;
- calcolo di (P(E_1)), (P(E_2)), (P(E_3));
- calcolo delle probabilità congiunte;
- calcolo di (P(H\mid E_1)) e (P(H\mid E_1\wedge E_2));
- sviluppo dei 16 costituenti elementari;
- distribuzione della variabile aleatoria (X), numero di palline bianche estratte;
- passaggi intermedi espressi con frazioni.

## Avvio locale

```bash
cd /Users/giuseppesanfilippo/Documents/ChatGPT/conditionalscore
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

L'app sarà disponibile all'indirizzo [http://localhost:8501](http://localhost:8501).

## File principali

- `streamlit_app.py` — applicazione Streamlit;
- `x_distribution_app.py` — progetto separato dedicato alla distribuzione di (X) con (n) estrazioni;
- `requirements.txt` — dipendenze Python;
- `index.html`, `styles.css`, `app.js` — prima versione web statica.

Per avviare il progetto dedicato a (X):

```bash
python -m streamlit run x_distribution_app.py
```
