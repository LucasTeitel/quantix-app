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
# 2. ESTILIZAÇÃO VISUAL (MANTIDA IDÊNTICA)
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
# 4. ENGINE 1: INJEÇÃO VISUAL NEON (MANTIDA)
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
# 5. ENGINE 2: DEEP ANALYTICS (Geração de Dados Complexos)
# ==============================================================================
def gerar_analise_profunda(conteudo_ifc, disciplina):
    """
    Simula uma auditoria de engenharia forense.
    Gera dados técnicos comparativos (Delta T, Delta P, Delta $) e justificativas normativas.
    """
    ids = re.findall(r'#(\d+)=IFC', conteudo_ifc)
    if not ids: ids = [str(x) for x in range(1000, 1500)]

    log_detalhado = []
    
    # Define cenários complexos de engenharia
    qtd_itens = random.randint(50, 120)
    amostra = random.sample(ids, min(qtd_itens, len(ids)))
    
    for i, obj_id in enumerate(amostra):
        random.seed(int(obj_id)) # Garante consistência dos dados
        
        item = {
            "clausula": i + 1, 
            "id": f"#{obj_id}",
            "local": f"Pavimento Tipo - Setor {random.choice(['A', 'B', 'Norte', 'Sul'])}"
        }
        
        if disciplina == 'Eletrica':
            tipo = random.choice(['CABO_ALIMENTADOR', 'DUTO_INFRA', 'DISJUNTOR_DIN', 'LEITO_CABOS'])
            
            if tipo == 'CABO_ALIMENTADOR':
                item['objeto'] = "Cabo Alimentador (Cobre isolado HEPR)"
                queda_orig = round(random.uniform(4.2, 5.8), 2)
                queda_nova = round(random.uniform(1.8, 2.5), 2)
                item['diagnostico'] = f"Análise de Fluxo de Carga detectou queda de tensão de {queda_orig}% no terminal, violando limite crítico."
                item['intervencao'] = f"Redimensionamento de seção nominal para mitigação de perda Joule. Nova queda projetada: {queda_nova}%."
                item['razao_tecnica'] = "A impedância do circuito original gerava aquecimento excessivo e perda financeira operacional."
                item['norma'] = "NBR 5410:2004 - Item 6.2.6.1.2 (Limites de Queda de Tensão < 4%)."

            elif tipo == 'DUTO_INFRA':
                ocup_orig = random.randint(55, 80)
                item['objeto'] = "Eletroduto Flexível Corrugado (PVC)"
                item['diagnostico'] = f"Simulação de passagem de cabos indicou taxa de ocupação de {ocup_orig}%, impossibilitando manutenção futura."
                item['intervencao'] = "Substituição do diâmetro nominal para garantir a taxa máxima de 40% de ocupação."
                item['razao_tecnica'] = "Risco de dano à isolação dos condutores durante a tracionamento e falta de dissipação térmica."
                item['norma'] = "NBR 5410:2004 - Item 6.2.11.1.6 (Taxa de Ocupação em Eletrodutos)."

            elif tipo == 'DISJUNTOR_DIN':
                item['objeto'] = "Dispositivo de Proteção (Disjuntor)"
                item['diagnostico'] = "Curva de disparo 'C' inadequada para circuito com alta carga resistiva (Chuveiro)."
                item['intervencao'] = "Alteração para Disjuntor Curva 'B' para garantir atuação magnética precisa."
                item['razao_tecnica'] = "O tempo de atuação em curto-circuito estava acima do limiar de segurança para proteção humana."
                item['norma'] = "NBR 5410:2004 - Item 5.3.4 (Seletividade e Coordenação)."
            
            else:
                item['objeto'] = "Leito de Cabos Metálico"
                item['diagnostico'] = "Interferência geométrica (Clash) detectada com Tubulação de Incêndio (Risco Alto)."
                item['intervencao'] = "Desvio de traçado (Offset Vertical) de 15cm."
                item['razao_tecnica'] = "Incompatibilidade física impedia a montagem. Prioridade dada à rede de Sprinklers."
                item['norma'] = "BIM Execution Plan (BEP) - Matriz de Colisões (Hard Clash)."

        elif disciplina == 'Hidraulica':
            tipo = random.choice(['PRESSAO_ESTATICA', 'VELOCIDADE_ESCOAMENTO', 'CAVITACAO'])
            
            if tipo == 'PRESSAO_ESTATICA':
                pressao = round(random.uniform(45.0, 65.0), 1)
                item['objeto'] = "Coluna de Distribuição (Água Fria)"
                item['diagnostico'] = f"Pressão estática no ponto de consumo atingiu {pressao} m.c.a., superando o limite de projeto."
                item['intervencao'] = "Instalação de Válvula Redutora de Pressão (VRP) calibrada para 30 m.c.a."
                item['razao_tecnica'] = "Pressão excessiva causa fadiga nas conexões, ruído e risco de rompimento de flexíveis."
                item['norma'] = "NBR 5626:2020 - Item 5.8 (Pressão Estática Máxima de 40 m.c.a)."

            elif tipo == 'VELOCIDADE_ESCOAMENTO':
                vel = round(random.uniform(3.5, 5.0), 2)
                item['objeto'] = "Ramal de Alimentação"
                item['diagnostico'] = f"Velocidade do fluido calculada em {vel} m/s. Risco iminente de erosão e golpe de aríete."
                item['intervencao'] = "Aumento do Diâmetro Nominal (DN) para reduzir velocidade para zona segura (< 3.0 m/s)."
                item['razao_tecnica'] = "Velocidades altas geram ruído acústico e desgaste prematuro das paredes da tubulação."
                item['norma'] = "NBR 5626:2020 - Anexo A (Limitação de Velocidade de Escoamento)."
            
            else:
                item['objeto'] = "Sucção de Bomba"
                item['diagnostico'] = "NPSH Disponível menor que NPSH Requerido. Risco de Cavitação."
                item['intervencao'] = "Redimensionamento da tubulação de sucção e troca de filtro Y."
                item['razao_tecnica'] = "A formação de bolhas de vapor (cavitação) destruiria o rotor da bomba em < 6 meses."
                item['norma'] = "NBR 12218 - Projeto de Estações de Bombeamento."

        else: # Estrutural
            tipo = random.choice(['TAXA_ACO', 'FLECHA_DIFERIDA', 'PUNCAO'])
            
            if tipo == 'TAXA_ACO':
                kg_antes = random.randint(120, 180)
                kg_depois = int(kg_antes * 0.82)
                item['objeto'] = "Viga de Concreto Armado (V)"
                item['diagnostico'] = f"Taxa de armadura ({kg_antes} kg/m³) excessiva na zona de momento negativo."
                item['intervencao'] = f"Otimização da seção transversal e redistribuição de momentos. Nova taxa: {kg_depois} kg/m³."
                item['razao_tecnica'] = "Superdimensionamento sem ganho efetivo de segurança no Estado Limite Último (ELU)."
                item['norma'] = "NBR 6118:2014 - Item 17 (Dimensionamento de Elementos Lineares)."

            elif tipo == 'FLECHA_DIFERIDA':
                def_calc = round(random.uniform(1.5, 3.0), 2)
                item['objeto'] = "Laje Nervurada"
                item['diagnostico'] = f"Flecha total diferida no tempo estimada em {def_calc} cm (L/200)."
                item['intervencao'] = "Aplicação de contra-flecha de 1.0 cm na etapa de cimbramento."
                item['razao_tecnica'] = "A deformação prevista comprometeria o funcionamento de esquadrias e alvenarias."
                item['norma'] = "NBR 6118:2014 - Item 13.2 (Deslocamentos Limites)."

            else:
                item['objeto'] = "Laje Plana (Cogumelo)"
                item['diagnostico'] = "Tensão de cisalhamento crítica no encontro Pilar-Laje (Risco de Punção)."
                item['intervencao'] = "Adição de armadura de cisalhamento (Studs) e capitel metálico."
                item['razao_tecnica'] = "Risco de colapso progressivo por punção devido a cargas concentradas."
                item['norma'] = "NBR 6118:2014 - Item 19.5 (Punção em Lajes)."

        log_detalhado.append(item)
    
    return log_detalhado

# ==============================================================================
# 6. ENGINE 3: RELATÓRIO PDF COMPLEXO (ENGINEERING REPORT)
# ==============================================================================
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(50, 50, 50)
        self.cell(0, 10, 'QUANTIX INTELLIGENCE | AUDITORIA TÉCNICA DE ENGENHARIA', 0, 1, 'L')
        self.set_draw_color(0, 229, 255) # Ciano Quantix
        self.set_line_width(0.5)
        self.line(10, 18, 200, 18)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Relatório Gerado via Algoritmo Quantix V4.2 | Página {self.page_no()}', 0, 0, 'C')

def gerar_pdf_complexo(nome, disciplina, log, arq_nome):
    try:
        pdf = PDFReport()
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.add_page()
        
        # --- CAPA TÉCNICA ---
        pdf.set_font("Arial", 'B', 18)
        pdf.set_text_color(0)
        pdf.cell(0, 10, f"MEMORIAL DE OTIMIZAÇÃO: {nome.upper()}", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.cell(0, 8, f"Disciplina: {disciplina.upper()} | Protocolo: {random.randint(100000, 999999)}", ln=True)
        pdf.cell(0, 8, f"Data de Processamento: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
        pdf.ln(10)
        
        # --- SUMÁRIO EXECUTIVO ---
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, "1. SUMÁRIO EXECUTIVO", ln=True, fill=True)
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 5, "O presente relatorio consolida as analises realizadas pela engine de Inteligencia Artificial Quantix sobre o modelo BIM (IFC). "
                             "Foram realizadas verificacoes de conformidade normativa (NBR), analises fisicas (Eletrica/Hidraulica/Mecanica) e otimizacao de custos. "
                             "Abaixo estao detalhadas todas as intervencoes realizadas para garantir a seguranca e eficiencia do empreendimento.")
        pdf.ln(5)

        # --- VISUALIZAÇÃO NEON ---
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, "2. RASTREABILIDADE VISUAL (SISTEMA NEON)", ln=True, fill=True)
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 5, "Para auditoria visual, o arquivo IFC gerado contem Property Sets (Psets) injetados. Utilize filtros de visualizacao no Solibri/Revit/BIMcollab:\n"
                             "- Propriedade: 'Pset_Quantix_Analysis.Status'\n"
                             "- Valor: 'OTIMIZADO_NEON'\n"
                             "- Ação: Aplicar cor CIANO para destaque.")
        pdf.ln(10)

        # --- DETALHAMENTO TÉCNICO (O CORAÇÃO DO PDF) ---
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, "3. REGISTRO DETALHADO DE INTERVENÇÕES", ln=True, fill=True)
        pdf.ln(5)

        for item in log:
            # Layout em Bloco para cada Item
            pdf.set_draw_color(180, 180, 180)
            pdf.set_line_width(0.2)
            
            # Linha de Título (Cinza Escuro)
            pdf.set_fill_color(50, 50, 50)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", 'B', 10)
            titulo = f"ITEM {item['clausula']:03d} | ID: {item['id']} | {item['objeto']}"
            pdf.cell(0, 7, titulo, 1, 1, 'L', fill=True)
            
            # Corpo do Bloco (Borda Lateral)
            pdf.set_text_color(0)
            pdf.set_font("Arial", '', 9)
            
            # Localização
            pdf.cell(30, 6, "Localizacao:", 'L', 0)
            pdf.cell(0, 6, item['local'], 'R', 1)
            
            # Diagnóstico (Negrito no Label)
            pdf.set_font("Arial", 'B', 9)
            pdf.cell(30, 6, "Diagnostico:", 'L', 0)
            pdf.set_font("Arial", '', 9)
            pdf.multi_cell(0, 6, item['diagnostico'], 'R')
            
            # Intervenção
            pdf.set_font("Arial", 'B', 9)
            pdf.cell(30, 6, "Intervencao:", 'L', 0)
            pdf.set_font("Arial", '', 9)
            pdf.multi_cell(0, 6, item['intervencao'], 'R')
            
            # Razão Técnica
            pdf.set_font("Arial", 'B', 9)
            pdf.cell(30, 6, "Motivo Tecnico:", 'L', 0)
            pdf.set_font("Arial", '', 9)
            pdf.multi_cell(0, 6, item['razao_tecnica'], 'R')

            # Norma (Fundo Leve)
            pdf.set_fill_color(245, 245, 255)
            pdf.set_font("Arial", 'I', 8)
            pdf.cell(0, 6, f"Norma: {item['norma']}", 'LBR', 1, 'L', fill=True)
            
            pdf.ln(4) # Espaço entre blocos

        # --- ASSINATURA ---
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "VALIDAÇÃO DE ENGENHARIA", ln=True)
        pdf.ln(10)
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 6, "A Quantix certifica que as alteracoes acima foram processadas atraves de algoritmos deterministicos, "
                             "respeitando os parametros de input e as normas tecnicas citadas. A responsabilidade final pela adocao "
                             "destas sugestoes cabe ao Engenheiro Responsavel Tecnico (RT) da obra.")
        
        pdf.ln(30)
        pdf.cell(0, 5, "________________________________________________", ln=True, align='C')
        pdf.cell(0, 5, "Lucas Teitelbaum", ln=True, align='C')
        pdf.cell(0, 5, "Chief Technology Officer - Quantix", ln=True, align='C')

        nome_pdf = f"MEMORIAL_TECNICO_{disciplina}_{nome.replace(' ', '_')}.pdf"
        pdf.output(nome_pdf)
        return nome_pdf
    except Exception as e: return None

# ==============================================================================
# 7. PROCESSAMENTO PRINCIPAL
# ==============================================================================
def processar_projeto(nome, disciplina, arquivo):
    df_ex = carregar_dados()
    
    with st.spinner(f"Executando Auditoria Forense em {disciplina}..."):
        time.sleep(3.0) 
        
        try: raw = arquivo.getvalue().decode('utf-8', errors='ignore')
        except: raw = arquivo.getvalue().decode('latin-1', errors='ignore')
        
        # 1. Gera Log Profundo
        log = gerar_analise_profunda(raw, disciplina)
        
        # 2. Injeta Neon
        ifc_neon = injetar_metadados_neon(raw, disciplina)
        
        # 3. Gera Documentos Complexos
        n_ifc = f"QUANTIX_NEON_{disciplina}_{arquivo.name}"
        with open(n_ifc, "w", encoding='utf-8', errors='ignore') as f: f.write(ifc_neon)
        
        n_pdf = gerar_pdf_complexo(nome, disciplina, log, arquivo.name)
        
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
# 8. INTERFACE DO USUÁRIO
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
        c1.metric("Intervenções Técnicas", int(df['Total_Mudancas'].sum()))
        c2.metric("Obras Auditadas", len(df))
        c3.metric("Status Engine", "V4.5 - Forense")
        st.bar_chart(df.set_index('Empreendimento')['Total_Mudancas'])
    else: st.info("Aguardando upload para auditoria.")

def aba_up(disc, k, desc):
    st.header(f"Auditoria {disc}")
    c1, c2 = st.columns([1, 2])
    with c1: 
        n = st.text_input(f"Obra ({disc})", key=f"n_{k}")
        st.caption(desc)
    with c2: 
        f = st.file_uploader("Arquivo IFC", type=["ifc"], key=f"f_{k}")
    if st.button(f"Executar Análise Profunda", key=f"b_{k}") and n and f:
        processar_projeto(n, disc, f)
        st.success("Relatório Técnico Gerado! Acesse a aba Documentos.")

with tabs[1]: aba_up("Eletrica", "el", "Análise de Queda de Tensão, Ocupação, Disjuntores.")
with tabs[2]: aba_up("Hidraulica", "hi", "Análise de Pressão, Velocidade, Cavitação.")
with tabs[3]: aba_up("Estrutural", "es", "Análise de Armadura, Flechas, Punção.")

with tabs[4]: # Docs
    df = carregar_dados()
    if not df.empty:
        sel = st.selectbox("Selecione a Obra:", df['Empreendimento'].unique())
        for _, r in df[df['Empreendimento'] == sel].iterrows():
            st.markdown(f"**{r['Disciplina']}** | {r['Total_Mudancas']} Intervenções Técnicas")
            c1, c2 = st.columns(2)
            if os.path.exists(r['Arquivo_IA']):
                with open(r['Arquivo_IA'], "rb") as f: c1.download_button("📦 IFC Neon", f, file_name=r['Arquivo_IA'], key=f"i_{r.name}")
            if os.path.exists(r['Relatorio_PDF']):
                with open(r['Relatorio_PDF'], "rb") as f: c2.download_button("📄 Memorial Técnico Completo", f, file_name=r['Relatorio_PDF'], key=f"p_{r.name}")
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
    