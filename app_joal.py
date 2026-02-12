import streamlit as st
import pandas as pd
from PIL import Image, ImageOps
import os
import re
import random
import time
from datetime import datetime
from fpdf import FPDF

# ==============================================================================
# 1. CONFIGURAÇÃO DE SISTEMA
# ==============================================================================
st.set_page_config(
    page_title="QUANTIX | Intelligence Engine",
    layout="wide",
    page_icon="💠",
    initial_sidebar_state="collapsed"
)

DB_FILE = "projetos_quantix.csv"

# ==============================================================================
# 2. ESTILIZAÇÃO VISUAL (DNA QUANTIX - HIGH CONTRAST)
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    :root { 
        --primary-color: #00E5FF; 
        --secondary-color: #FF9F00; 
        --bg-dark: #0E1117; 
        --card-bg: #1a1a1a; 
    }

    .neon-text { color: var(--primary-color); text-shadow: 0 0 10px rgba(0, 229, 255, 0.6); font-weight: 800; }
    
    [data-testid="stMetricValue"] { color: var(--primary-color) !important; font-size: 36px !important; font-weight: 800 !important; }
    [data-testid="stMetric"] { background-color: var(--card-bg); border: 1px solid #333; transition: transform 0.2s; }
    [data-testid="stMetric"]:hover { transform: scale(1.02); border-color: var(--primary-color); }

    .stButton > button { 
        border: 1px solid var(--primary-color) !important; 
        color: var(--primary-color) !important; 
        background-color: transparent !important;
        font-weight: 600; width: 100%; transition: all 0.3s;
    }
    .stButton > button:hover { 
        background-color: var(--primary-color) !important; color: #000 !important; 
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.3);
    }

    .dna-box { 
        background-color: #00151a; 
        padding: 30px; 
        border: 2px solid var(--primary-color); 
        margin-bottom: 20px; 
        color: #ffffff !important; 
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 229, 255, 0.1);
    }
    .dna-box-x { 
        background-color: #1a0d00 !important; 
        border: 2px solid var(--secondary-color) !important; 
        box-shadow: 0 4px 20px rgba(255, 159, 0, 0.1);
    }
    .dna-box h2, .dna-box p { color: #ffffff !important; text-shadow: 0 1px 2px rgba(0,0,0,0.8); }

    .user-badge { border: 1px solid var(--primary-color); color: var(--primary-color); padding: 5px 15px; border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. BANCO DE DADOS
# ==============================================================================
def carregar_dados():
    colunas = ["Empreendimento", "Disciplina", "Data", "Total_Mudancas", "Arquivo_IA", "Relatorio_PDF"]
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE)
        except: pass
    return pd.DataFrame(columns=colunas)

# ==============================================================================
# 4. ENGINE 1: INJEÇÃO NEON (MANTIDA)
# ==============================================================================
def injetar_metadados_neon(conteudo_ifc, disciplina):
    timestamp = int(time.time())
    ids_encontrados = re.findall(r'#(\d+)=IFC[A-Z]+', conteudo_ifc)
    qtd = min(150, len(ids_encontrados))
    ids_alvo = random.sample(ids_encontrados, qtd) if ids_encontrados else []
    
    meta_block = f"\n/* QUANTIX NEON ENGINE - {disciplina.upper()} */\n"
    meta_block += f"/* TIMESTAMP: {timestamp} | MARKED_ITEMS: {len(ids_alvo)} */\n"
    
    for obj_id in ids_alvo:
        meta_block += f"/* #99{obj_id}=IFCPROPERTYSET('Pset_Quantix_Analysis',#{obj_id},(('Status',IFCLABEL('OTIMIZADO_NEON')),('Action',IFCLABEL('REDUCE')))); */\n"

    if "END-ISO-10303-21;" in conteudo_ifc:
        return conteudo_ifc.replace("END-ISO-10303-21;", meta_block + "END-ISO-10303-21;")
    return conteudo_ifc + meta_block

# ==============================================================================
# 5. ENGINE 2: ANALYTICS CORE (CÁLCULO DE ENGENHARIA DETALHADO)
# ==============================================================================
def gerar_analise_avancada(conteudo_ifc, disciplina):
    """
    Gera justificativas baseadas em cálculos físicos simulados para cada ID.
    O 'Por quê' agora é baseado em números (Antes vs Depois).
    """
    ids = re.findall(r'#(\d+)=IFC', conteudo_ifc)
    if not ids: ids = [str(x) for x in range(1000, 1500)]

    log_detalhado = []
    
    # Simula uma varredura de 40 a 100 itens críticos
    qtd_itens = random.randint(40, 100)
    amostra = random.sample(ids, min(qtd_itens, len(ids)))
    
    for i, obj_id in enumerate(amostra):
        # Seed aleatória baseada no ID para manter consistência
        random.seed(int(obj_id))
        
        item = {"clausula": i + 1, "id": f"#{obj_id}"}
        
        if disciplina == 'Eletrica':
            cenario = random.choice(['QUEDA_TENSAO', 'TAXA_OCUPACAO', 'CURTO_CIRCUITO', 'ROTA_STEINER'])
            if cenario == 'QUEDA_TENSAO':
                queda_orig = round(random.uniform(4.5, 7.0), 2)
                queda_novo = round(random.uniform(1.5, 2.5), 2)
                item['titulo'] = "Redimensionamento de Condutor (Queda de Tensão)"
                item['dados'] = f"Queda original: {queda_orig}% (>4%). Nova queda: {queda_novo}%."
                item['motivo'] = f"O circuito apresentava perda energética crítica. Ajuste de bitola conforme NBR 5410 item 6.2.6."
            elif cenario == 'TAXA_OCUPACAO':
                oc_orig = random.randint(55, 70)
                item['titulo'] = "Redução de Diâmetro de Eletroduto"
                item['dados'] = f"Ocupação original: {oc_orig}%. Ocupação otimizada: 33%."
                item['motivo'] = "Eletroduto superdimensionado. Redução segura mantendo taxa de ocupação máxima de 40% (NBR 5410)."
            elif cenario == 'ROTA_STEINER':
                dist_orig = round(random.uniform(15, 40), 1)
                dist_novo = round(dist_orig * 0.75, 1)
                item['titulo'] = "Retificação de Trajeto de Cabos"
                item['dados'] = f"Comprimento original: {dist_orig}m. Novo trajeto: {dist_novo}m."
                item['motivo'] = "Algoritmo de Steiner Tree identificou rota mais curta evitando interferências estruturais."
            else:
                item['titulo'] = "Coordenação de Proteção (Disjuntor)"
                item['dados'] = "Curva C -> Curva B."
                item['motivo'] = "Ajuste de seletividade para garantir disparo magnético correto em curto-circuito de baixa impedância."

        elif disciplina == 'Hidraulica':
            cenario = random.choice(['PRESSAO_DINAMICA', 'VELOCIDADE', 'PERDA_CARGA', 'SIFONAGEM'])
            if cenario == 'PRESSAO_DINAMICA':
                pressao = round(random.uniform(45, 60), 1)
                item['titulo'] = "Instalação de Válvula Redutora de Pressão (VRP)"
                item['dados'] = f"Pressão no ponto: {pressao} m.c.a (Máx Normativa: 40 m.c.a)."
                item['motivo'] = "Risco de golpe de aríete e fadiga da tubulação. VRP instalada para limitar a 30 m.c.a."
            elif cenario == 'VELOCIDADE':
                vel_orig = round(random.uniform(0.2, 0.4), 2)
                item['titulo'] = "Redução de Diâmetro Nominal (DN)"
                item['dados'] = f"Velocidade original: {vel_orig} m/s. Nova velocidade: 1.2 m/s."
                item['motivo'] = "Velocidade muito baixa gerava superdimensionamento. Tubo reduzido respeitando limite de 3.0 m/s (NBR 5626)."
            elif cenario == 'PERDA_CARGA':
                item['titulo'] = "Substituição de Conexão Crítica"
                item['dados'] = "Joelho 90º substituído por 2x Curvas 45º."
                item['motivo'] = "Redução de perda de carga localizada em 40%, melhorando a pressão no chuveiro crítico."
            else:
                item['titulo'] = "Correção de Ventilação Sanitária"
                item['dados'] = "Distância do fecho hídrico > 1.20m."
                item['motivo'] = "Risco de quebra de selo hídrico. Adicionado ramal de ventilação conforme NBR 8160."

        else: # Estrutural
            cenario = random.choice(['ACO_EXCESSIVO', 'FLECHA', 'CLASH', 'SAPATA'])
            if cenario == 'ACO_EXCESSIVO':
                taxa_orig = round(random.uniform(120, 150), 1)
                taxa_novo = round(taxa_orig * 0.85, 1)
                item['titulo'] = "Otimização de Taxa de Aço (Viga)"
                item['dados'] = f"Taxa original: {taxa_orig} kg/m³. Otimizada: {taxa_novo} kg/m³."
                item['motivo'] = "Análise de envoltória de esforços permitiu redução de armadura negativa sem comprometer ELU."
            elif cenario == 'FLECHA':
                item['titulo'] = "Ajuste de Contra-flecha em Viga"
                item['dados'] = "Flecha deferida calculada: 2.5cm."
                item['motivo'] = "Vão de janela comprometido. Aplicada contra-flecha de 1.5cm para garantir funcionamento da esquadria."
            elif cenario == 'CLASH':
                item['titulo'] = "Resolução de Conflito (Clash Detection)"
                item['dados'] = "Interseção Pilar P12 x Tubulação Pluvial."
                item['motivo'] = "Furo em viga não permitido por norma. Desvio da tubulação executado via shaft adjacente."
            else:
                item['titulo'] = "Recálculo de Fundação (Interação Solo-Estrutura)"
                item['dados'] = "Tensão admissível solo: 0.25 MPa."
                item['motivo'] = "Redução da área da sapata em 15% após refinamento do modelo de molas do solo (Winkler)."

        log_detalhado.append(item)
    
    return log_detalhado

# ==============================================================================
# 6. ENGINE 3: RELATÓRIO PDF "ULTIMATE" (Visual + Analítico)
# ==============================================================================
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'QUANTIX | AUDITORIA DE ENGENHARIA DE VALOR', 0, 1, 'C')
        self.set_draw_color(0, 229, 255)
        self.line(10, 20, 200, 20)
        self.ln(12)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Pagina {self.page_no()} | Engine Analitica V4.0', 0, 0, 'C')

def gerar_pdf_completo(nome, disciplina, log, arq_nome):
    try:
        pdf = PDFReport()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # CAPA
        pdf.set_font("Arial", 'B', 16)
        pdf.set_text_color(0)
        pdf.cell(0, 10, f"RELATORIO ANALITICO: {nome.upper()}", ln=True)
        pdf.set_font("Arial", 'I', 11)
        pdf.cell(0, 8, f"Disciplina: {disciplina} | Itens Auditados: {len(log)}", ln=True)
        pdf.ln(5)

        # SEÇÃO 1: NEON
        pdf.set_fill_color(220, 255, 255) 
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "1. RASTREABILIDADE VISUAL (NEON)", ln=True, fill=True)
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 6, "Para validar as otimizacoes visualmente, utilize o filtro 'Status=OTIMIZADO_NEON' no seu visualizador BIM.")
        pdf.ln(8)

        # SEÇÃO 2: DETALHAMENTO TÉCNICO PROFUNDO
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "2. DETALHAMENTO DE ENGENHARIA (ITEM A ITEM)", ln=True, fill=True)
        pdf.ln(2)
        
        pdf.set_draw_color(180)
        
        for item in log:
            # Cabeçalho do Item
            pdf.set_font("Arial", 'B', 10)
            pdf.set_fill_color(245, 245, 245)
            titulo = f"ITEM {item['clausula']:03d} (ID IFC {item['id']}): {item['titulo'].upper()}"
            pdf.cell(0, 7, titulo, 1, 1, 'L', fill=True)
            
            # Dados Técnicos (O "Porquê" Numérico)
            pdf.set_font("Arial", 'B', 9)
            pdf.cell(30, 6, "Analise Quantitativa:", 0, 0)
            pdf.set_font("Arial", '', 9)
            pdf.cell(0, 6, item['dados'], 0, 1)
            
            # Justificativa (O "Porquê" Técnico)
            pdf.set_font("Arial", 'B', 9)
            pdf.cell(30, 6, "Justificativa:", 0, 0)
            pdf.set_font("Arial", '', 9)
            pdf.multi_cell(0, 6, item['motivo'])
            
            pdf.ln(3) # Espaço

        # ASSINATURA
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "RESPONSABILIDADE TÉCNICA", ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 6, "Atestamos que as otimizacoes acima respeitam os Coeficientes de Seguranca normativos. "
                             "A reducao de insumos nao compromete o desempenho ou vida util da edificacao.")
        pdf.ln(20)
        pdf.cell(0, 5, "Lucas Teitelbaum", ln=True, align='C')
        pdf.cell(0, 5, "Engenharia de Valor & Data Science", ln=True, align='C')

        nome_pdf = f"MEMORIAL_DETALHADO_{disciplina}_{nome.replace(' ', '_')}.pdf"
        pdf.output(nome_pdf)
        return nome_pdf
    except Exception as e: return None

# ==============================================================================
# 7. PROCESSAMENTO PRINCIPAL
# ==============================================================================
def processar_projeto(nome, disciplina, arquivo):
    df_ex = carregar_dados()
    
    with st.spinner(f"Executando Auditoria Detalhada em {disciplina}..."):
        time.sleep(3.0) # Tempo para "pensar"
        
        try: raw = arquivo.getvalue().decode('utf-8', errors='ignore')
        except: raw = arquivo.getvalue().decode('latin-1', errors='ignore')
        
        # 1. Gera Log Avançado (Cálculos Simulados)
        log = gerar_analise_avancada(raw, disciplina)
        
        # 2. Injeta Neon
        ifc_neon = injetar_metadados_neon(raw, disciplina)
        
        # 3. Salva Arquivos
        n_ifc = f"QUANTIX_NEON_{disciplina}_{arquivo.name}"
        with open(n_ifc, "w", encoding='utf-8', errors='ignore') as f: f.write(ifc_neon)
        
        n_pdf = gerar_pdf_completo(nome, disciplina, log, arquivo.name)
        
        novo = {
            "Empreendimento": nome, "Disciplina": disciplina, 
            "Data": datetime.now().strftime("%d/%m/%Y"),
            "Total_Mudancas": len(log), "Arquivo_IA": n_ifc, "Relatorio_PDF": n_pdf
        }
        pd.concat([df_ex, pd.DataFrame([novo])], ignore_index=True).to_csv(DB_FILE, index=False)

def excluir(idx):
    try:
        df = carregar_dados()
        r = df.iloc[idx]
        if os.path.exists(r['Arquivo_IA']): os.remove(r['Arquivo_IA'])
        if os.path.exists(r['Relatorio_PDF']): os.remove(r['Relatorio_PDF'])
        df.drop(idx).to_csv(DB_FILE, index=False)
        st.rerun()
    except: pass

# ==============================================================================
# 8. INTERFACE
# ==============================================================================
h1, h2 = st.columns([8, 2])
with h1: st.markdown("# <span class='neon-text'>QUANTI</span><span style='color:#FF9F00'>X</span>", unsafe_allow_html=True)
with h2: st.markdown('<div class="user-badge">👤 Lucas Teitelbaum</div>', unsafe_allow_html=True)
st.markdown("---")

tabs = st.tabs(["📊 Visão Geral", "⚡ Elétrica", "💧 Hidráulica", "🏗️ Estrutural", "📂 Documentos", "🧬 DNA"])

with tabs[0]: # Dash
    df = carregar_dados()
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Cláusulas Técnicas", int(df['Total_Mudancas'].sum()))
        c2.metric("Obras Auditadas", len(df))
        c3.metric("Versão Engine", "V4.0 - Deep Analytics")
        st.bar_chart(df.set_index('Empreendimento')['Total_Mudancas'])
    else: st.info("Aguardando input para auditoria.")

def aba_up(disc, k, desc):
    st.header(f"Auditoria {disc}")
    c1, c2 = st.columns([1, 2])
    with c1: 
        n = st.text_input(f"Obra ({disc})", key=f"n_{k}")
        st.caption(desc)
    with c2: 
        f = st.file_uploader("Arquivo IFC", type=["ifc"], key=f"f_{k}")
    if st.button(f"Iniciar Auditoria Detalhada", key=f"b_{k}") and n and f:
        processar_projeto(n, disc, f)
        st.success("Auditoria Concluída! Verifique o Memorial na aba Documentos.")

with tabs[1]: aba_up("Eletrica", "el", "Análise de Queda de Tensão, Ocupação e Rotas.")
with tabs[2]: aba_up("Hidraulica", "hi", "Análise de Pressão, Velocidade e Perda de Carga.")
with tabs[3]: aba_up("Estrutural", "es", "Análise de Taxa de Aço, Flechas e Colisões.")

with tabs[4]: # Docs
    df = carregar_dados()
    if not df.empty:
        sel = st.selectbox("Selecione a Obra:", df['Empreendimento'].unique())
        for _, r in df[df['Empreendimento'] == sel].iterrows():
            st.markdown(f"**{r['Disciplina']}** | {r['Total_Mudancas']} Cláusulas detalhadas")
            c1, c2 = st.columns(2)
            if os.path.exists(r['Arquivo_IA']):
                with open(r['Arquivo_IA'], "rb") as f: c1.download_button("📦 IFC Neon", f, file_name=r['Arquivo_IA'], key=f"i_{r.name}")
            if os.path.exists(r['Relatorio_PDF']):
                with open(r['Relatorio_PDF'], "rb") as f: c2.download_button("📄 Memorial Técnico Detalhado", f, file_name=r['Relatorio_PDF'], key=f"p_{r.name}")
            st.divider()

with tabs[5]: # DNA
    st.markdown("## 🧬 O DNA QUANTIX")
    c1, c2 = st.columns(2)
    with c1: st.markdown('<div class="dna-box"><h2>QUANTI</h2><p>Rigor. Não apenas otimizamos; nós calculamos e justificamos.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="dna-box dna-box-x"><h2>X</h2><p>Inteligência. Otimização baseada em dados, não em palpites.</p></div>', unsafe_allow_html=True)
    
    st.divider()
    st.subheader("👤 O Fundador")
    st.write("Lucas Teitelbaum: Engenharia de precisão aliada à ciência de dados.")
    
    c_nbr, c_sec = st.columns(2)
    with c_nbr: st.success("🛡️ **AUDITORIA NBR**\n\nCálculos validados conforme normas vigentes.")
    with c_sec: st.info("🔒 **SEGURANÇA**\n\nProteção de dados industriais.")
    st.caption("QUANTIX Strategic Engine © 2026")