# app.py

import streamlit as st
import math

class Caixa:
    def __init__(self, altura: int, largura: int, profundidade: int):
        self.altura = altura
        self.largura = largura
        self.profundidade = profundidade
        self.altura_real = altura + (2 * profundidade)
        self.largura_real = largura + (2 * profundidade)

    def medida_real(self):
        return (self.altura_real, self.largura_real)

class Papelão:
    def __init__(self, altura: int = 100, largura: int = 80):
        self.altura = altura
        self.largura = largura

def calcular_caixas_por_papelao(caixa: Caixa, papelao: Papelão):
    base = caixa.medida_real()
    
    if base[0] == base[1]:
        alt = papelao.altura // base[0]
        larg = papelao.largura // base[1]
        total = alt * larg
        sobra_alt = papelao.altura - (alt * base[0])
        sobra_larg = papelao.largura - (larg * base[1])
        orientacao = f"{base[0]} x {base[1]}"
    else:
        # vertical
        v_alt = papelao.altura // base[0]
        v_larg = papelao.largura // base[1]
        total_v = v_alt * v_larg
        sobra_v_alt = papelao.altura - (v_alt * base[0])
        sobra_v_larg = papelao.largura - (v_larg * base[1])

        # horizontal
        h_alt = papelao.altura // base[1]
        h_larg = papelao.largura // base[0]
        total_h = h_alt * h_larg
        sobra_h_alt = papelao.altura - (h_alt * base[1])
        sobra_h_larg = papelao.largura - (h_larg * base[0])

        if total_v >= total_h:
            alt, larg, total = v_alt, v_larg, total_v
            sobra_alt, sobra_larg = sobra_v_alt, sobra_v_larg
            orientacao = f"{base[0]} x {base[1]} (Vertical)"
        else:
            alt, larg, total = h_alt, h_larg, total_h
            sobra_alt, sobra_larg = sobra_h_alt, sobra_h_larg
            orientacao = f"{base[1]} x {base[0]} (Horizontal)"

    return alt, larg, total, orientacao, sobra_alt, sobra_larg

def calcular_lombadas_fundos_e_tampas_por_papelao(caixa: Caixa, papelao: Papelão):
    lombada = [caixa.profundidade, caixa.largura + 1 ]
    tampa = [caixa.altura + 0.5, caixa.largura + 1]
    fundo = tampa.copy()

    if lombada[1] > tampa[1]:
        largura_maior = lombada[1]
    else:
        largura_maior = tampa[1]

    # Cada caixa precisa ter uma lombada, uma tampa e um fundo
    medidas_total_por_caixa = [lombada[0] + tampa[0] + fundo[0],
                                 largura_maior]
    
    # Calcular quantas caixas cabem no papelão
    if medidas_total_por_caixa[0] == medidas_total_por_caixa[1]:
        alt = papelao.altura // medidas_total_por_caixa[0]
        larg = papelao.largura // medidas_total_por_caixa[1]
        total = alt * larg
        sobra_alt = papelao.altura - (alt * medidas_total_por_caixa[0])
        sobra_larg = papelao.largura - (larg * medidas_total_por_caixa[1])
        orientacao = f"{medidas_total_por_caixa[0]} x {medidas_total_por_caixa[1]}"
    else:
        # vertical
        v_alt = papelao.altura // medidas_total_por_caixa[0]
        v_larg = papelao.largura // medidas_total_por_caixa[1]
        total_v = v_alt * v_larg
        sobra_v_larg = papelao.altura - (v_alt * medidas_total_por_caixa[0])
        sobra_v_alt = papelao.largura - (v_larg * medidas_total_por_caixa[1])

        # horizontal
        h_alt = papelao.altura // medidas_total_por_caixa[1]
        h_larg = papelao.largura // medidas_total_por_caixa[0]
        total_h = h_alt * h_larg
        sobra_h_alt = papelao.altura - (h_alt * medidas_total_por_caixa[1])
        sobra_h_larg = papelao.largura - (h_larg * medidas_total_por_caixa[0])

        if total_v >= total_h:
            alt, larg, total = v_alt, v_larg, total_v
            sobra_alt, sobra_larg = sobra_v_alt, sobra_v_larg
            orientacao = f"{medidas_total_por_caixa[0]} x {medidas_total_por_caixa[1]} (Vertical)"
        else:
            alt, larg, total = h_alt, h_larg, total_h
            sobra_alt, sobra_larg = sobra_h_alt, sobra_h_larg
            orientacao = f"{medidas_total_por_caixa[1]} x {medidas_total_por_caixa[0]} (Horizontal)"

    return alt, larg, total, orientacao, sobra_alt, sobra_larg
    


# Interface Streamlit
st.title("🧮 Calculadora de Caixas no Papelão - Meraki")

altura = st.number_input("Altura da caixa (cm):", min_value=1)
largura = st.number_input("Largura da caixa (cm):", min_value=1)
profundidade = st.number_input("Profundidade da caixa (cm):", min_value=0)
qtd_caixas_desejada = st.number_input("Quantas caixas deseja fazer?", min_value=1, step=1)

if st.button("Calcular"):
    caixa = Caixa(altura, largura, profundidade)
    papelao = Papelão()

    base = caixa.medida_real()
    st.write(f"📦 Medida real da base da caixa: `{base[0]} x {base[1]} cm`")
    st.write(f"📏 Papelão disponível: `{papelao.altura} x {papelao.largura} cm`")

    alt, larg, total_por_papelao, orientacao, sobra_altura, sobra_largura = calcular_caixas_por_papelao(caixa, papelao)

    if total_por_papelao == 0:
        st.error("❌ Nenhuma caixa cabe no papelão com essas medidas.")
    else:
        st.success(f"✅ Melhor orientação: {orientacao}")
        st.write(f"➡️ Caixas por papelão: `{alt} x {larg}` = **{total_por_papelao} caixas**")
        if sobra_altura > 0 and sobra_largura > 0:
            st.write(f"📏 Sobra no papelão: **100 x {sobra_largura} cm** na vertical e **{sobra_altura} x 80 cm** na horizontal")
        elif sobra_altura <= 0 and sobra_largura > 0:
            st.write(f"📏 Sobra no papelão: **100 x {sobra_largura} cm** ")
        elif sobra_altura > 0 and sobra_largura <= 0:
            st.write(f"📏 Sobra no papelão: **{sobra_altura} x 80 cm** ")
        else:
            st.write("📏 Não há sobra no papelão.")

        papelões_necessarios = math.ceil(qtd_caixas_desejada / total_por_papelao)
        st.info(f"📦 Para produzir **{qtd_caixas_desejada} caixas**, serão necessários **{papelões_necessarios} papelões**.")
        """ st.balloons()  # Animação de balões para celebrar o sucesso """

    st.subheader("📚 Lombadas, Fundos e Tampas")

    # Calcular lombadas, fundos e tampas
    alt_lombada, larg_lombada, total_lombadas, orientacao_lombada, sobra_altura_lombada, sobra_largura_lombada = calcular_lombadas_fundos_e_tampas_por_papelao(caixa, papelao)

    if total_lombadas == 0:
        st.error("❌ Nenhuma lombada, fundo ou tampa cabe no papelão com essas medidas.")
    else:
        st.success(f"✅ Melhor orientação para lombadas, fundos e tampas: {orientacao_lombada}")
        st.write(f"➡️ Lombadas, fundos e tampas por papelão: `{int(alt_lombada)} x {int(larg_lombada)}` = **{int(total_lombadas)} conjuntos de 1 lombada + tampa e fundo**")
        if sobra_altura_lombada > 0 and sobra_largura_lombada > 0:
            st.write(f"📏 Sobra no papelão: **100 x {sobra_altura_lombada} cm** na vertical e **{sobra_largura_lombada} x 80 cm** na horizontal")
        elif sobra_altura_lombada <= 0 and sobra_largura_lombada > 0:
            st.write(f"📏 Sobra no papelão: **{sobra_largura_lombada} x 80 cm** na horizontal")
        elif sobra_altura_lombada > 0 and sobra_largura_lombada <= 0:
            st.write(f"📏 Sobra no papelão: **100 x {sobra_altura_lombada} cm** na vertical")
        else:
            st.write("📏 Não há sobra no papelão.")
            
        lombadas_necessarias = math.ceil(qtd_caixas_desejada / total_lombadas)
        st.info(f"📦 Para produzir **{qtd_caixas_desejada} caixas**, serão necessárias **{lombadas_necessarias} Papelões para fazer todos os conjuntos.** {qtd_caixas_desejada} Lombadas e {qtd_caixas_desejada} Fundos e Tampas.")

