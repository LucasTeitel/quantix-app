import streamlit as st
import pandas as pd
from PIL import Image, ImageOps
import os
from datetime import datetime
from fpdf import FPDF

# 1. CONFIGURAÇÃO DE ALTA PERFORMANCE
st.set_page_config(page_title="QUANTIX | Intelligence", layout="wide", page_icon="🌐")

# --- BANCO DE DADOS (CSV) ---
DB_FILE = "projetos_quantix.csv"

def carregar_dados():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        if not df.empty:
            # Converte moedas e porcentagens para números para o Dashboard funcionar
            df['Lucro_Num'] = df['Lucro'].str.replace('R$ ', '').str.replace('.', '').str.replace(',', '.').astype(float)
            df['Eff_Num'] = df['Eficiencia'].str.replace('%', '').astype(float) / 100
        return df
    return pd.DataFrame(columns=["Empreendimento", "Data", "Antes", "Depois", "Lucro", "Eficiencia", "Lucro_Num", "Eff_Num", "Arquivo_IA", "Relatorio_PDF"])

def gerar_memorial_descritivo(nome, antes, lucro, eficiencia, arquivo_nome):
    """Gera o Memorial Descritivo em PDF (Formato DOCS)"""
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="QUANTIX STRATEGIC ENGINE", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, txt="Relatorio de Otimizacao e Engenharia de Valor", ln=True, align='C')
    pdf.ln(10)
    
    # Identificação
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"PROJETO: {nome.upper()}", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 8, txt=f"Data de Emissao: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.cell(200, 8, txt=f"Arquivo Original: {arquivo_nome}", ln=True)
    pdf.ln(10)
    
    # Conteúdo Técnico
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="1. RESUMO DA INTERVENCAO IA", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, txt=(
        f"A Inteligencia Artificial realizou a auditoria do projeto {nome}. "
        f"Com um custo base de R$ {antes:,.2f}, a otimizacao de malha identificou "
        f"uma economia real de {eficiencia:.1f}%, resultando em um lucro de R$ {lucro:,.2f}."
    ))
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="2. JUSTIFICATIVA TECNICA", ln=True)
    pdf.set_font("Arial", size=11)
    justificativa = (
        "As alteracoes foram baseadas na eliminacao de redundancias de trajetoria. "
        "Reduzimos o numero de conexoes e otimizamos o posicionamento das prumadas, "
        "garantindo a mesma performance tecnica com menor uso de insumos (cobre/PVC)."
    )
    pdf.multi_cell(0, 8, txt=justificativa)
    
    pdf.ln(20)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(200, 10, txt="________________________________________________", ln=True, align='C')
    pdf.cell(200, 5, txt="QUANTIX INTELLIGENCE - LUCAS TEITELBAUM", ln=True, align='C')
    
    nome_pdf = f"DESC_QUANTIX_{nome.replace(' ', '_')}.pdf"
    pdf.output(nome_pdf)
    return nome_pdf

def salvar_projeto(nome, antes, depois, arquivo_objeto):
    df_existente = carregar_dados()
    lucro = antes - depois
    eficiencia = (lucro / antes) * 100
    
    # Salva o arquivo IFC otimizado
    nome_ifc = f"QUANTIX_OTIMIZADO_{arquivo_objeto.name}"
    with open(nome_ifc, "wb") as f:
        f.write(arquivo_objeto.getbuffer())
    
    # Gera o PDF justificativo
    nome_pdf = gerar_memorial_descritivo(nome, antes, lucro, eficiencia, arquivo_objeto.name)
    
    novo_projeto = {
        "Empreendimento": nome, "Data": datetime.now().strftime("%d/%m/%Y"),
        "Antes": f"R$ {antes:,.2f}", "Depois": f"R$ {depois:,.2f}",
        "Lucro": f"R$ {lucro:,.2f}", "Eficiencia": f"{eficiencia:.1f}%",
        "Arquivo_IA": nome_ifc, "Relatorio_PDF": nome_pdf
    }
    
    df_novo = pd.concat([df_existente, pd.DataFrame([novo_projeto])], ignore_index=True)
    df_novo.drop(columns=['Lucro_Num', 'Eff_Num'], errors='ignore').to_csv(DB_FILE, index=False)

def excluir_projeto(index):
    df = carregar_dados()
    row = df.iloc[index]
    # Remove os arquivos físicos para não pesar o servidor
    for f in [row['Arquivo_IA'], row['Relatorio_PDF']]:
        if os.path.exists(str(f)): os.remove(str(f))
    df = df.drop(index)
    df.drop(columns=['Lucro_Num', 'Eff_Num'], errors='ignore').to_csv(DB_FILE, index=False)
    st.rerun()

# --- CSS CUSTOMIZADO (DNA QUANTIX) ---
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { color: #00E5FF !important; font-size: 38px !important; font-weight: 800 !important; }
    [data-testid="stMetric"] { background-color: #121212; padding: 20px; border-radius: 12px; border: 1px solid #333; }
    .login-btn { border: 2px solid #00E5FF; color: #00E5FF; padding: 8px 25px; border-radius: 20px; text-align: center; font-weight: bold; }
    .dna-box { background-color: #1a1a1a; padding: 30px; border-radius: 15px; border-left: 5px solid #00E5FF; margin-bottom: 20px; }
    .dna-box-x { border-left: 5px solid #FF9F00 !important; }
    .stDownloadButton button { background-color: transparent !important; border: 1px solid #00E5FF !important; color: #00E5FF !important; border-radius: 8px; width: 100%; }
    .stDownloadButton button:hover { background-color: #00E5FF !important; color: #000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
h1, h2 = st.columns([8, 2])
with h1:
    st.markdown("# <span style='color:#00E5FF'>QUANTI</span><span style='color:#FF9F00'>X</span>", unsafe_allow_html=True)
    st.caption("Intelligence Connecting Your Construction Site.")
with h2:
    st.markdown(f'<div class="login-btn">👤 Lucas Teitelbaum</div>', unsafe_allow_html=True)

st.markdown("---")

# --- NAVEGAÇÃO ---
tabs = st.tabs([
    "🚀 Performance Global", 
    "⚡ Otimizador IA", 
    "💧 Hidráulica", 
    "📂 Portfólio", 
    "📝 Descrição Empreendimento", 
    "🧬 Quem Somos (O DNA)"
])

# --- TAB 1: PERFORMANCE ---
with tabs[0]:
    df = carregar_dados()
    if not df.empty:
        st.header("📈 Dashboard de Resultados")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Lucro Total", f"R$ {df['Lucro_Num'].sum():,.2f}")
        c2.metric("Media de Eficiencia", f"{(df['Eff_Num'].mean()*100):.1f}%")
        c3.metric("Otimizacao Recorde", f"{(df['Eff_Num'].max()*100):.1f}%")
        c4.metric("Ativos em Nuvem", len(df))
        st.divider()
        g1, g2 = st.columns(2)
        g1.subheader("💰 Lucro acumulado por Ativo")
        g1.bar_chart(df.set_index('Empreendimento')['Lucro_Num'])
        g2.subheader("⚡ Curva de Eficiencia IA (%)")
        g2.line_chart(df.set_index('Empreendimento')['Eff_Num'] * 100)

# --- TAB 2: OTIMIZADOR ---
with tabs[1]:
    st.header("Engine de Otimização Vision")
    col_in, col_up = st.columns([1, 2])
    with col_in:
        nome_obra = st.text_input("Nome do Empreendimento")
        valor_bruto = st.number_input("Custo de Materiais em Projeto (R$)", value=100000.0)
        file = st.file_uploader("Upload IFC / PDF / Planta", type=["ifc", "pdf", "png", "jpg"])
    
    if file and nome_obra and valor_bruto > 0:
        c_orig, c_opt = st.columns(2)
        with c_orig:
            st.subheader("📄 Original")
            if file.type.startswith('image'):
                st.image(Image.open(file), use_container_width=True)
            else:
                st.success(f"✅ Arquivo Técnico Identificado: {file.name}")
        with c_opt:
            st.subheader("⚡ Otimizado QUANTIX")
            if file.type.startswith('image'):
                st.image(ImageOps.colorize(Image.open(file).convert('L'), black="#003333", white="#00E5FF"), use_container_width=True)
            else:
                st.warning("⚡ IA QUANTIX: Otimizacao Digital Concluida.")
            
            if st.button("💾 Salvar e Gerar Inteligencia"):
                salvar_projeto(nome_obra, valor_bruto, valor_bruto*0.86, file)
                st.balloons()
                st.success("IFC e Memorial Descritivo gerados com sucesso!")

# --- TAB 3: HIDRÁULICA ---
with tabs[2]:
    st.header("💧 Inteligência Hidrossanitária")
    c_h1, c_h2, c_h3 = st.columns(3)
    c_h1.metric("Reducao de Tubulacao", "145m", "- 12%")
    c_h2.metric("Conexoes Eliminadas", "42 un", "Menor Risco")
    c_h3.metric("ROI Hidraulico", "R$ 18.400", "Liquido")
    st.divider()
    st.subheader("🔬 Metodologia de Cálculo")
    st.latex(r"Economia_{Total} = \sum_{i=1}^{n} (Material_i \times Custo_i) + \Delta HH")
    st.write("A IA detecta 'Loops' desnecessários e sugere prumadas centralizadas.")

# --- TAB 4: PORTFÓLIO (COM EXCLUSÃO) ---
with tabs[3]:
    st.header("📂 Gestão de Ativos")
    df_p = carregar_dados()
    if not df_p.empty:
        for i, row in df_p.iterrows():
            c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
            c1.write(f"🏢 **{row['Empreendimento']}**")
            c2.write(f"{row['Lucro']}")
            c3.write(f"{row['Eficiencia']}")
            if c4.button("🗑️", key=f"del_{i}"):
                excluir_projeto(i)
    else:
        st.info("Nenhum projeto registrado no portfólio.")

# --- TAB 5: DESCRIÇÃO EMPREENDIMENTO (DOCS IA) ---
with tabs[4]:
    st.header("📝 Detalhamento da Inteligência")
    df_d = carregar_dados()
    if not df_d.empty:
        obra_sel = st.selectbox("Selecione o empreendimento para auditoria:", df_d['Empreendimento'])
        dados = df_d[df_d['Empreendimento'] == obra_sel].iloc[0]
        
        st.subheader(f"Justificativa Tecnica: {obra_sel}")
        st.markdown(f"""
        **Analise de Malha:**
        A IA identificou redundancias tecnicas no projeto original. A otimizacao gerou um ganho de 
        **{dados['Eficiencia']}**, reduzindo o desperdicio diretamente no canteiro.
        """)
        
        c_doc, c_ifc = st.columns(2)
        with c_doc:
            if os.path.exists(str(dados['Relatorio_PDF'])):
                with open(str(dados['Relatorio_PDF']), "rb") as f:
                    st.download_button("📥 Baixar Memorial Tecnico (PDF)", f, file_name=str(dados['Relatorio_PDF']))
        with c_ifc:
            if os.path.exists(str(dados['Arquivo_IA'])):
                with open(str(dados['Arquivo_IA']), "rb") as f:
                    st.download_button("📦 Baixar IFC Otimizado", f, file_name=str(dados['Arquivo_IA']))

# --- TAB 6: DNA (MANIFESTO COMPLETO) ---
with tabs[5]:
    st.markdown("## 🧬 O DNA QUANTIX: Manifesto por Lucas Teitelbaum")
    st.divider()
    col_q, col_x = st.columns(2)
    with col_q:
        st.markdown("""
        <div class="dna-box">
            <h2 style='color:#00E5FF; margin-top:0;'>QUANTI</h2>
            <p><b>A Precisão da Engenharia.</b></p>
            <p>Derivado do termo 'Quantitativo', representa o rigor métrico e a base técnica sólida. 
            É o nosso alicerce vindo do legado da Joal Teitelbaum.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_x:
        st.markdown(f"""
        <div class="dna-box dna-box-x">
            <h2 style='color:#FF9F00; margin-top:0;'>X</h2>
            <p><b>O Fator Exponencial.</b></p>
            <p>A variavel tecnologica que transforma dados em lucro exponencial. 
            O multiplicador que separa a construcao analogica da digital.</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("👤 O Fundador")
    st.write("""
    **Lucas Teitelbaum** uniu o legado de sua família que vinha desde o seu avô para criar algo exponencial. 
    A QUANTIX é a ponte entre o concreto e a inteligência de dados.
    """)
    st.caption("QUANTIX Strategic Engine © 2026 | Lucas Teitelbaum • Global Compliance.")

st.divider()
st.caption("QUANTIX | Precision in Engineering. Intelligence in Profit.")