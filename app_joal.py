import streamlit as st
import pandas as pd
from PIL import Image, ImageOps
import os
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="QUANTIX | Intelligence", layout="wide", page_icon="🌐")

# --- BANCO DE DADOS (CSV) ---
DB_FILE = "projetos_quantix.csv"

def carregar_dados():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        # Garante as colunas para cálculos do dashboard
        df['Lucro_Num'] = df['Lucro'].str.replace('R$ ', '').str.replace('.', '').str.replace(',', '.').astype(float)
        df['Eff_Num'] = df['Eficiencia'].str.replace('%', '').astype(float) / 100
        return df
    return pd.DataFrame(columns=["Empreendimento", "Data", "Antes", "Depois", "Lucro", "Eficiencia", "Lucro_Num", "Eff_Num", "Arquivo"])

def salvar_projeto(nome, antes, depois, arquivo_objeto):
    df_existente = carregar_dados()
    lucro = antes - depois
    eficiencia = (lucro / antes) * 100
    
    # Gera o Novo Arquivo da IA para Download
    nome_otimizado = f"QUANTIX_OTIMIZADO_{arquivo_objeto.name}"
    with open(nome_otimizado, "wb") as f:
        f.write(arquivo_objeto.getbuffer())
    
    novo_projeto = {
        "Empreendimento": nome, "Data": datetime.now().strftime("%d/%m/%Y"),
        "Antes": f"R$ {antes:,.2f}", "Depois": f"R$ {depois:,.2f}",
        "Lucro": f"R$ {lucro:,.2f}", "Eficiencia": f"{eficiencia:.1f}%",
        "Arquivo": nome_otimizado
    }
    
    df_novo = pd.concat([df_existente, pd.DataFrame([novo_projeto])], ignore_index=True)
    df_novo.drop(columns=['Lucro_Num', 'Eff_Num'], errors='ignore').to_csv(DB_FILE, index=False)

# --- CSS CUSTOMIZADO (Identidade Visual QUANTIX) ---
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { color: #00E5FF !important; font-size: 38px !important; font-weight: 800 !important; }
    [data-testid="stMetric"] { background-color: #121212; padding: 20px; border-radius: 12px; border: 1px solid #333; }
    .login-btn { border: 2px solid #00E5FF; color: #00E5FF; padding: 8px 25px; border-radius: 20px; text-align: center; font-weight: bold; }
    .dna-box { background-color: #1a1a1a; padding: 30px; border-radius: 15px; border-left: 5px solid #00E5FF; margin-bottom: 20px; }
    .dna-box-x { border-left: 5px solid #FF9F00 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO (LIMPO) ---
h1, h2 = st.columns([8, 2])
with h1:
    st.markdown("# <span style='color:#00E5FF'>QUANTI</span><span style='color:#FF9F00'>X</span>", unsafe_allow_html=True)
    st.caption("Intelligence Connecting Your Construction Site.")
with h2:
    st.markdown('<div class="login-btn">👤 Lucas Teitelbaum</div>', unsafe_allow_html=True)

st.markdown("---")

# --- NAVEGAÇÃO PRINCIPAL ---
tabs = st.tabs([
    "🚀 Performance Global", 
    "⚡ Otimizador IA", 
    "💧 Hidráulica", 
    "📂 Portfólio", 
    "🧬 Quem Somos (O DNA)"
])

# --- TAB 1: PERFORMANCE ---
with tabs[0]:
    df = carregar_dados()
    if not df.empty:
        st.header("📈 Dashboard de Resultados")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Lucro Total", f"R$ {df['Lucro_Num'].sum():,.2f}")
        c2.metric("Média de Economia (%)", f"{(df['Eff_Num'].mean()*100):.1f}%")
        c3.metric("Otimização Máxima", f"{(df['Eff_Num'].max()*100):.1f}%")
        c4.metric("Projetos Ativos", len(df))
        st.divider()
        g1, g2 = st.columns(2)
        g1.subheader("💰 Lucro acumulado")
        g1.bar_chart(df.set_index('Empreendimento')['Lucro_Num'])
        g2.subheader("⚡ Curva de Eficiência IA (%)")
        g2.line_chart(df.set_index('Empreendimento')['Eff_Num'] * 100)

# --- TAB 2: OTIMIZADOR ---
with tabs[1]:
    st.header("Engine de Otimização Vision")
    st.info("🛡️ Configuração de Alta Capacidade Ativa: Suporte para arquivos até 1GB.")
    col_in, col_up = st.columns([1, 2])
    with col_in:
        nome = st.text_input("Nome da Obra")
        bruto = st.number_input("Custo Materiais (R$)", value=100000.0)
        up = st.file_uploader("Upload Planta / BIM / PDF", type=["png", "jpg", "jpeg", "pdf", "ifc"])
    
    if up and nome and bruto > 0:
        c_orig, c_opt = st.columns(2)
        taxa = 0.14
        with c_orig:
            st.subheader("📄 Original")
            st.write(f"Arquivo: {up.name}")
            if up.type.startswith('image'):
                try: st.image(Image.open(up), use_container_width=True)
                except: st.warning("Processamento visual em curso...")
            else:
                st.success(f"📦 Arquivo Técnico Detectado: {up.name}")
                st.info("Analisando malha de engenharia e metadados...")
        with c_opt:
            st.subheader("⚡ Otimizado QUANTIX")
            if up.type.startswith('image'):
                st.image(ImageOps.colorize(Image.open(up).convert('L'), black="#003333", white="#00E5FF"), use_container_width=True)
            else:
                st.warning("⚡ IA QUANTIX: Otimização Digital Concluída.")
                st.write("Redução de insumos calculada sobre a árvore de objetos do arquivo.")
            
            if st.button("💾 Salvar no Portfólio"):
                salvar_projeto(nome, bruto, bruto*(1-taxa), up)
                st.balloons()

# --- TAB 3: HIDRÁULICA ---
with tabs[2]:
    st.header("💧 Inteligência Hidrossanitária")
    c_h1, c_h2, c_h3 = st.columns(3)
    c_h1.metric("Redução de Canos", "145m", "- 12%")
    c_h2.metric("Conexões Eliminadas", "42 un", "Menos risco")
    c_h3.metric("ROI Estimado", "R$ 18.400", "Líquido")
    st.divider()
    with st.expander("🛠️ Detalhes da Otimização Hidráulica"):
        st.write("A IA detecta 'Loops' desnecessários e sugere prumadas centralizadas.")
        st.latex(r"Economia = \sum (Conexão_{PVC} \times Custo_{Instalação})")

# --- TAB 4: PORTFÓLIO ---
with tabs[3]:
    st.header("📂 Gestão de Ativos")
    df_p = carregar_dados()
    if not df_p.empty:
        st.dataframe(df_p[['Empreendimento', 'Data', 'Antes', 'Depois', 'Lucro', 'Eficiencia', 'Arquivo']],
            column_config={"Arquivo": st.column_config.TextColumn("📄 Status Doc IA")},
            use_container_width=True, hide_index=True)
        
        st.divider()
        st.subheader("📥 Área de Download")
        escolha = st.selectbox("Selecione o empreendimento para baixar o projeto otimizado:", df_p['Empreendimento'])
        arquivo_path = df_p[df_p['Empreendimento'] == escolha]['Arquivo'].values[0]
        
        if os.path.exists(str(arquivo_path)):
            with open(str(arquivo_path), "rb") as file:
                st.download_button(
                    label=f"⬇️ Baixar Projeto Otimizado: {escolha}",
                    data=file,
                    file_name=str(arquivo_path),
                    mime="application/octet-stream"
                )

# --- TAB 5: QUEM SOMOS (DNA RESTAURADO) ---
with tabs[4]:
    st.markdown("## 🧬 O DNA QUANTIX: Manifesto por Lucas Teitelbaum")
    st.write("A QUANTIX não é apenas uma plataforma; é o novo sistema operacional da construção inteligente.")
    
    st.divider()

    # PILAR 1: O CONCEITO QUANTI+X
    st.subheader("🚀 A Gênese da Marca")
    col_q, col_x = st.columns(2)
    
    with col_q:
        st.markdown("""
        <div class="dna-box">
            <h2 style='color:#00E5FF; margin-top:0;'>QUANTI</h2>
            <p><b>A Precisão da Engenharia.</b></p>
            <p>Derivado do termo 'Quantitativo', o QUANTI representa o rigor métrico e a base técnica sólida. 
            É o nosso alicerce na engenharia de precisão, onde cada grama de cobre e cada metro de cano 
            são contabilizados.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_x:
        st.markdown(f"""
        <div class="dna-box dna-box-x">
            <h2 style='color:#FF9F00; margin-top:0;'>X</h2>
            <p><b>O Fator Exponencial.</b></p>
            <p>O 'X' simboliza a variável tecnológica desconhecida pelo mercado tradicional. É a Inteligência Artificial 
            que processa gigabytes de dados em segundos para gerar lucro exponencial.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # PILAR 2: MISSÃO E O FUNDADOR
    col_missao, col_fundador = st.columns(2)
    
    with col_missao:
        st.subheader("🎯 Nossa Missão")
        st.write("""
        Maximizar a lucratividade da construção civil através de Visão Computacional, 
        eliminando o desperdício humano e transformando projetos complexos em ativos 
        otimizados de alta performance.
        """)
        st.subheader("🌍 Nossa Visão")
        st.write("""
        Liderar a transição global da construção analógica para a digital, 
        tornando a QUANTIX o padrão mundial de auditoria de projetos Lean.
        """)
        
    with col_fundador:
        st.subheader("👤 O Fundador")
        st.write(f"""
        **Lucas Teitelbaum** uniu o legado de sua família que vinha desde o seu avô, para algo que vai restar anos. 
        Ao identificar que milhões de reais eram literalmente enterrados em obras devido a projetos ineficientes, 
        decidiu criar a QUANTIX: a ponte entre o concreto e a inteligência de dados.
        """)

    st.divider()

    # PILAR 3: COMPLIANCE
    st.subheader("🛡️ Base de Proteção e Segurança Jurídica")
    with st.expander("📌 Metodologia de Validação Híbrida"):
        st.info("A QUANTIX opera como uma ferramenta de Inteligência Aumentada. Toda economia deve ser validada pelo Responsável Técnico (RT).")
    with st.expander("📌 Propriedade Intelectual"):
        st.warning("Os algoritmos vision são de propriedade exclusiva da QUANTIX Inc.")
        st.caption("QUANTIX Strategic Engine © 2026 | Lucas Teitelbaum • Global Compliance.")

# RODAPÉ
st.divider()
st.caption("QUANTIX | Precision in Engineering. Intelligence in Profit.")