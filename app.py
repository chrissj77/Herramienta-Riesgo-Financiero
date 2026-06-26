import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

# Configuración de la página
st.set_page_config(page_title="Gestor de Riesgo MiPyme", layout="wide", page_icon="📊")

st.title("📊 Herramienta Avanzada de Gestión de Riesgo Financiero")
st.markdown("Analizador automático de riesgos corporativos basado exclusivamente en los Estados Financieros Oficiales (Balance General y P&G).")

# Inicializar la memoria de ejecución para que los datos no se borren al interactuar
if "ejecutar_diagnostico" not in st.session_state:
    st.session_state.ejecutar_diagnostico = False

# --- MÓDULO DE ENTRADA DE DATOS (Cuentas Estándar de Contabilidad) ---
with st.expander("📝 Ingrese los Estados Financieros (Periodo Actual)", expanded=True):
    col_bg, col_er = st.columns(2)
    
    with col_bg:
        st.subheader("🏦 1. Balance General")
        activo_corriente = st.number_input("Activo Corriente ($)", value=246704842.0, step=1000000.0, help="Efectivo, cuentas por cobrar, inventarios.")
        inventarios = st.number_input("Inventarios ($)", value=105569493.0, step=1000000.0)
        cuentas_cobrar = st.number_input("Cuentas por Cobrar Comerciales ($)", value=86509838.0, step=1000000.0)
        activo_no_corriente = st.number_input("Activo No Corriente ($)", value=320000000.0, step=1000000.0, help="Propiedad, planta y equipo, intangibles.")
        
        st.write("---")
        pasivo_corriente = st.number_input("Pasivo Corriente ($)", value=220422382.0, step=1000000.0, help="Deudas a pagar en menos de 1 año.")
        pasivo_no_corriente = st.number_input("Pasivo No Corriente ($)", value=160000000.0, step=1000000.0, help="Deudas a largo plazo.")
        patrimonio = st.number_input("Patrimonio Neto ($)", value=186282460.0, step=1000000.0)
        
    with col_er:
        st.subheader("📉 2. Estado de Resultados (P&G)")
        ventas_netas = st.number_input("Ventas / Ingresos Operacionales ($)", value=967863825.0, step=1000000.0)
        utilidad_operacional = st.number_input("Utilidad Operacional (EBIT) ($)", value=56460584.0, step=1000000.0)
        gastos_financieros = st.number_input("Gastos Financieros / Intereses ($)", value=42213737.0, step=1000000.0)
        impuestos = st.number_input("Impuestos sobre la Renta / Gastos Fiscales ($)", value=4165000.0, step=500000.0)
        utilidad_neta = st.number_input("Utilidad Neta del Ejercicio ($)", value=8462793.0, step=1000000.0)

# Botón de activación
if st.button("🚀 Calcular Diagnóstico Integral de Riesgos", use_container_width=True):
    st.session_state.ejecutar_diagnostico = True

# --- BLOQUE DE CÁLCULO Y DISPLAY ---
if st.session_state.ejecutar_diagnostico:
    
    # Procesamiento Matemático Inicial
    activo_total = activo_corriente + activo_no_corriente
    pasivo_total = pasivo_corriente + pasivo_no_corriente
    utilidad_antes_impuestos = utilidad_neta + impuestos
    
    # Ratios Financieros
    prueba_acida = (activo_corriente - inventarios) / pasivo_corriente if pasivo_corriente > 0 else 0
    dias_cartera = (cuentas_cobrar * 365) / ventas_netas if ventas_netas > 0 else 0
    cobertura_intereses = utilidad_operacional / gastos_financieros if gastos_financieros > 0 else 0
    margen_operacional = (utilidad_operacional / ventas_netas) * 100 if ventas_netas > 0 else 0
    endeudamiento_total = (pasivo_total / activo_total) * 100 if activo_total > 0 else 0
    carga_fiscal = (impuestos / utilidad_antes_impuestos) * 100 if utilidad_antes_impuestos > 0 else 0

    riesgos = {
        "Liquidez": {"X": 1.0, "Y": 1.0}, "Crédito": {"X": 1.0, "Y": 1.0},
        "Mercado": {"X": 1.0, "Y": 1.0}, "Operacional": {"X": 1.0, "Y": 1.0},
        "Sistémico": {"X": 1.0, "Y": 1.0}, "Legal/Fiscal": {"X": 1.0, "Y": 1.0}
    }
    dofa = {"Fortalezas": [], "Debilidades": [], "Oportunidades": [], "Amenazas": []}

    # --- TEXTOS ULTRA EXPLICATIVOS PARA EL RESUMEN EJECUTIVO ---
    if prueba_acida < 0.8:
        status_pa = ("🔴 CRÍTICO", f"Tu Prueba Ácida es de {prueba_acida:.2f}. Esto significa que por cada peso que debes a corto plazo, solo tienes {prueba_acida:.2f} pesos en activos líquidos inmediatos (excluyendo inventarios) para responder. Estás en zona de peligro inminente de iliquidez técnica si tus acreedores exigen pagos rápidos.")
    elif prueba_acida < 1.0:
        status_pa = ("🟡 ADVERTENCIA", f"Tu Prueba Ácida es de {prueba_acida:.2f}. Tienes una cobertura ajustada. Dependes casi por completo de vender rápidamente el inventario que tienes guardado para poder cumplir con tus obligaciones corrientes. Cualquier freno en las ventas congelará tu caja.")
    else:
        status_pa = ("🟢 SALUDABLE", f"Tu Prueba Ácida es de {prueba_acida:.2f}. Gozas de una posición de liquidez excelente. Tienes la capacidad de cubrir todas tus deudas de corto plazo de inmediato sin necesidad de rematar mercancía ni presionar liquidaciones de stock.")

    if dias_cartera <= 45:
        status_dc = ("🟢 EFICIENTE", f"Tus Días de Cartera son de {dias_cartera:.0f} días. El ciclo de cobranza es ágil y saludable; el dinero que prestas a tus clientes retorna rápido a la cuenta bancaria de la empresa, manteniendo activo el flujo operativo de trabajo.")
    elif dias_cartera <= 60:
        status_dc = ("🟡 TOLERABLE", f"Tus Días de Cartera son de {dias_cartera:.0f} días. Estás financiando a tus clientes por más tiempo del promedio recomendado. Tienes capital de trabajo atrapado en la calle que deberías recuperar para evitar costos financieros innecesarios.")
    else:
        status_dc = ("🔴 PREOCUPANTE", f"Tus Días de Cartera se elevan a {dias_cartera:.0f} días. Financiamiento excesivo y peligroso. Estás actuando como banco de tus clientes sin cobrar intereses. Riesgo altísimo de que esta cartera se vuelva incobrable y te ahogue.")

    if cobertura_intereses >= 3.0:
        status_ci = ("🟢 FINANCIADO", f"Tu Cobertura de Intereses es de {cobertura_intereses:.2f}x. Tu utilidad operativa es robusta y paga con holgura los intereses bancarios. Los bancos ven a la empresa como un cliente seguro y con excelente capacidad de pago.")
    elif cobertura_intereses >= 1.5:
        status_ci = ("🟡 ALERTA", f"Tu Cobertura de Intereses es de {cobertura_intereses:.2f}x. Capacidad ajustada. Gran parte de lo que produce la operación se va en pagar costos financieros. Una pequeña caída en ingresos te dejaría en problemas con los bancos.")
    else:
        status_ci = ("🔴 PREOCUPANTE", f"Tu Cobertura es de solo {cobertura_intereses:.2f}x. Alerta máxima de quiebra financiera. La operación apenas logra arañar dinero para pagar los puros intereses de la deuda. Estás al borde del impago y requieres reestructuración urgente.")

    if margen_operacional >= 12.0:
        status_mo = ("🟢 RENTABLE", f"El Margen Operacional se ubica en el {margen_operacional:.1f}%. Indica un estricto control de costos fijos y variables. El modelo de negocio genera un excelente colchón de ganancias antes de atender obligaciones financieras.")
    elif margen_operacional >= 6.0:
        status_mo = ("🟡 COMPRIMIDO", f"Tu Margen Operacional es del {margen_operacional:.1f}%. El rendimiento operativo está apretado. Cualquier incremento imprevisto en materias primas, arriendos o nómina absorberá por completo la utilidad de la MiPyme.")
    else:
        status_mo = ("🔴 DEFICITARIO", f"Tu Margen Operacional es críticamente bajo ({margen_operacional:.1f}%). Los gastos de administración y costos de venta absorben casi el 100% de los ingresos. El negocio trabaja a pérdida interna y no es viable así.")

    if endeudamiento_total <= 45.0:
        status_et = ("🟢 AUTÓNOMO", f"Tu Nivel de Endeudamiento es del {endeudamiento_total:.1f}%. La empresa se financia principalmente con recursos propios de los socios. Tienes un blindaje estructural alto ante crisis externas o subidas de tasas.")
    elif endeudamiento_total <= 65.0:
        status_et = ("🟡 EXPUESTO", f"Tu Nivel de Endeudamiento está en el {endeudamiento_total:.1f}%. Estructura de capital equilibrada pero expuesta. Tienes compromisos fijos con terceros que limitan tu agilidad para tomar nuevas oportunidades de inversión.")
    else:
        status_et = ("🔴 APALANCADO", f"El Endeudamiento alcanza un alarmante {endeudamiento_total:.1f}%. El negocio ya no es de los dueños, prácticamente le pertenece a los acreedores externos. Alto riesgo patrimonial ante variaciones macroeconómicas.")

    if carga_fiscal <= 22.0:
        status_cf = ("🟢 ÓPTIMO", f"La Carga Fiscal Efectiva es del {carga_fiscal:.1f}%. Estás aprovechando eficientemente las deducciones y beneficios tributarios legales, logrando que la mayor parte de la utilidad se quede retenida en la empresa.")
    elif carga_fiscal <= 35.0:
        status_cf = ("🟡 ESTÁNDAR", f"La Carga Fiscal representa el {carga_fiscal:.1f}%. Presión tributaria normal según la ley del sector, pero refleja una falta de planeación fiscal estratégica para mitigar el impacto sobre las ganancias netas.")
    else:
        status_cf = ("🔴 AGRESIVO", f"La Carga Fiscal drena el {carga_fiscal:.1f}% de tus ganancias antes de impuestos. El esquema impositivo está asfixiando las utilidades del ejercicio, desincentivando el retorno de inversión para los socios.")

    # --- LLENADO DE LA MATRIZ DOFA Y UBICACIÓN DE COORDENADAS ---
    # 1. Liquidez
    if prueba_acida >= 1.0:
        riesgos["Liquidez"] = {"X": 1.0, "Y": 1.0}  # Verde
        dofa["Fortalezas"].append(f"Liquidez Superior (Prueba Ácida: {prueba_acida:.2f}): Excelente disponibilidad de efectivo inmediato. Mitiga el riesgo de frenos operativos y permite negociar mejores precios con proveedores al contado.")
    elif prueba_acida >= 0.8:
        riesgos["Liquidez"] = {"X": 3.5, "Y": 1.0}  # Amarillo
        dofa["Debilidades"].append(f"Vulnerabilidad de Caja (Prueba Ácida: {prueba_acida:.2f}): Cobertura corriente muy ajustada. Se depende críticamente de la rotación del inventario para pagar las deudas operativas del mes.")
    elif prueba_acida >= 0.5:
        riesgos["Liquidez"] = {"X": 1.2, "Y": 3.5}  # Naranja
        dofa["Amenazas"].append(f"Riesgo de Liquidez Alto (Prueba Ácida: {prueba_acida:.2f}): Presión fuerte sobre el flujo de caja operativo.")
    else:
        riesgos["Liquidez"] = {"X": 4.5, "Y": 4.5}  # Rojo
        dofa["Amenazas"].append(f"Déficit Extremo de Liquidez (Prueba Ácida: {prueba_acida:.2f}): Activos líquidos insuficientes para cubrir el pasivo corriente. Peligro de suspensión de pagos o necesidad de financiamiento costoso de última hora.")

    # 2. Crédito
    if dias_cartera <= 45:
        riesgos["Crédito"] = {"X": 1.0, "Y": 1.6}  # Verde
        dofa["Fortalezas"].append(f"Cobranza de Alta Eficiencia (Cartera: {dias_cartera:.0f} días): El efectivo de las ventas regresa rápido al circuito operativo, disminuyendo al mínimo histórico las pérdidas por cuentas de cobro dudosas.")
    elif dias_cartera <= 60:
        riesgos["Crédito"] = {"X": 3.5, "Y": 1.6}  # Amarillo
        dofa["Debilidades"].append(f"Inmovilización de Capital (Cartera: {dias_cartera:.0f} días): Financiación comercial prolongada que amarra recursos en la calle, restándole velocidad financiera y liquidez al ciclo interno.")
    elif dias_cartera <= 90:
        riesgos["Crédito"] = {"X": 1.2, "Y": 4.1}  # Naranja
        dofa["Amenazas"].append(f"Cartera con Alerta de Riesgo (Cartera: {dias_cartera:.0f} días): Los tiempos de cobro se extienden peligrosamente afectando la caja.")
    else:
        riesgos["Crédito"] = {"X": 4.5, "Y": 4.1}  # Rojo
        dofa["Amenazas"].append(f"Peligro de Cartera Incobrable (Cartera: {dias_cartera:.0f} días): Riesgo inminente de pérdida permanente de capital de trabajo por insolvencia de clientes. La empresa financia la cadena sin respaldo.")

    # 3. Mercado
    if cobertura_intereses >= 3.0:
        riesgos["Mercado"] = {"X": 1.6, "Y": 1.0}  # Verde
        dofa["Fortalezas"].append(f"Capacidad Financiera Sólida (Cobertura: {cobertura_intereses:.2f}x): La rentabilidad operativa absorbe cómodamente el costo del dinero. Permite un amplio margen para solicitar nuevas líneas crediticias.")
    elif cobertura_intereses >= 1.5:
        riesgos["Mercado"] = {"X": 4.1, "Y": 1.0}  # Amarillo
        dofa["Debilidades"].append(f"Presión Bancaria Moderada (Cobertura: {cobertura_intereses:.2f}x): Margen de maniobra financiero reducido ante incrementos imprevistos en las tasas de interés preferenciales del mercado actual.")
    elif cobertura_intereses >= 1.0:
        riesgos["Mercado"] = {"X": 1.8, "Y": 3.5}  # Naranja
        dofa["Amenazas"].append(f"Cobertura Ajustada de Intereses (Cobertura: {cobertura_intereses:.2f}x): Riesgo de mercado alto por presión financiera bancaria.")
    else:
        riesgos["Mercado"] = {"X": 3.6, "Y": 4.5}  # Rojo
        dofa["Amenazas"].append(f"Insolvencia Financiera Operativa (Cobertura: {cobertura_intereses:.2f}x): El EBIT operativo está totalmente secuestrado por los gastos financieros. Riesgo directo de quiebra ante los bancos acreedores.")

    # 4. Operacional
    if margen_operacional >= 12.0:
        riesgos["Operacional"] = {"X": 1.6, "Y": 1.6}  # Verde
        dofa["Fortalezas"].append(f"Optimización de Operaciones (Margen: {margen_operacional:.1f}%): Alta eficiencia productiva y comercial. El modelo absorbe variaciones de costos sin destruir el beneficio final para los socios.")
    elif margen_operacional >= 6.0:
        riesgos["Operacional"] = {"X": 4.1, "Y": 1.6}  # Amarillo
        dofa["Debilidades"].append(f"Margen Operativo Comprimido ({margen_operacional:.1f}%): Estructura operativa vulnerable a la inflación de costos, fletes o aumentos de salarios, limitando el margen de seguridad.")
    elif margen_operacional >= 2.0:
        riesgos["Operacional"] = {"X": 1.8, "Y": 4.1}  # Naranja
        dofa["Amenazas"].append(f"Rentabilidad Operativa Crítica ({margen_operacional:.1f}%): Márgenes muy bajos que exponen severamente la operación básica.")
    else:
        riesgos["Operacional"] = {"X": 3.6, "Y": 4.1}  # Rojo
        dofa["Amenazas"].append(f"Ineficiencia Estructural Interna (Margen: {margen_operacional:.1f}%): El proceso de producción o venta destruye valor. La MiPyme trabaja para cubrir puros costos operativos fijos básicos.")

    # 5. Sistémico
    if endeudamiento_total <= 45.0:
        riesgos["Sistémico"] = {"X": 2.2, "Y": 1.0}  # Verde
        dofa["Oportunidades"].append(f"Capacidad de Apalancamiento Libre (Deuda: {endeudamiento_total:.1f}%): Autonomía financiera idónea para levantar créditos de inversión a largo plazo y expandir infraestructura comercial rápidamente.")
    elif endeudamiento_total <= 65.0:
        riesgos["Sistémico"] = {"X": 4.7, "Y": 1.0}  # Amarillo
        dofa["Debilidades"].append(f"Nivel de Apalancamiento Límite (Deuda: {endeudamiento_total:.1f}%): Nivel de deuda intermedio que frena la flexibilidad de la empresa para reaccionar rápido ante nuevas demandas del entorno.")
    elif endeudamiento_total <= 80.0:
        riesgos["Sistémico"] = {"X": 2.2, "Y": 3.5}  # Naranja
        dofa["Amenazas"].append(f"Apalancamiento Elevado (Deuda: {endeudamiento_total:.1f}%): Alta dependencia de terceros que genera un riesgo sistémico elevado.")
    else:
        riesgos["Sistémico"] = {"X": 5.0, "Y": 5.0}  # Rojo
        dofa["Amenazas"].append(f"Riesgo de Quiebra Sistémica (Deuda: {endeudamiento_total:.1f}%): Sobreendeudamiento estructural masivo. Un endurecimiento general del crédito o recesión sectorial causará un colapso total.")

    # 6. Legal/Fiscal
    if carga_fiscal <= 22.0:
        riesgos["Legal/Fiscal"] = {"X": 2.2, "Y": 1.6}  # Verde
        dofa["Oportunidades"].append(f"Eficiencia Tributaria Lograda (Impuestos: {carga_fiscal:.1f}%): Excelente uso normativo de beneficios fiscales. Permite reinvertir las utilidades líquidas directamente en el crecimiento del negocio.")
    elif carga_fiscal <= 35.0:
        riesgos["Legal/Fiscal"] = {"X": 4.7, "Y": 1.6}  # Amarillo
        dofa["Debilidades"].append(f"Ausencia de Planeación Fiscal (Impuestos: {carga_fiscal:.1f}%): Pago impositivo estándar que erosiona las ganancias operativas netas sin estrategias legales de optimización tributaria.")
    elif carga_fiscal <= 45.0:
        riesgos["Legal/Fiscal"] = {"X": 2.2, "Y": 4.1}  # Naranja
        dofa["Amenazas"].append(f"Presión Fiscal Alta (Impuestos: {carga_fiscal:.1f}%): Carga tributaria que empieza a comprometer seriamente la retención de utilidades.")
    else:
        riesgos["Legal/Fiscal"] = {"X": 5.0, "Y": 4.1}  # Rojo
        dofa["Amenazas"].append(f"Asfixia Fiscal por Carga Impositiva ({carga_fiscal:.1f}%): Alta tributación efectiva que descapitaliza el flujo neto de caja, impidiendo acumular reservas para contingencias futuras.")

    # --- RENDERIZADO DEL RESUMEN EJECUTIVO ---
    st.subheader("📋 Resumen Ejecutivo de Indicadores Clave Explicados")
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    kpi_col4, kpi_col5, kpi_col6 = st.columns(3)
    
    with kpi_col1:
        st.markdown(f"**🟢 Prueba Ácida: `{prueba_acida:.2f}`**")
        st.caption(f"**Estado:** {status_pa[0]}\n\n{status_pa[1]}")
    with kpi_col2:
        st.markdown(f"**📅 Días de Cartera: `{dias_cartera:.0f} días`**")
        st.caption(f"**Estado:** {status_dc[0]}\n\n{status_dc[1]}")
    with kpi_col3:
        st.markdown(f"**📈 Cobertura de Intereses: `{cobertura_intereses:.2f}x`**")
        st.caption(f"**Estado:** {status_ci[0]}\n\n{status_ci[1]}")
        
    st.write("") 
    
    with kpi_col4:
        st.markdown(f"**📊 Margen Operacional: `{margen_operacional:.1f}%`**")
        st.caption(f"**Estado:** {status_mo[0]}\n\n{status_mo[1]}")
    with kpi_col5:
        st.markdown(f"**🛡️ Nivel de Endeudamiento: `{endeudamiento_total:.1f}%`**")
        st.caption(f"**Estado:** {status_et[0]}\n\n{status_et[1]}")
    with kpi_col6:
        st.markdown(f"**⚖️ Carga Fiscal Efectiva: `{carga_fiscal:.1f}%`**")
        st.caption(f"**Estado:** {status_cf[0]}\n\n{status_cf[1]}")

    st.divider()
    
    # --- INTERFAZ VISUAL PRINCIPAL DOFA Y MATRIZ ---
    col_dofa, col_matriz = st.columns([1.2, 1.1])

    with col_dofa:
        st.subheader("🛡️ Matriz DOFA Financiera Automatizada (Análisis Estratégico)")
        
        st.markdown("#### 💪 Fortalezas (Ventajas Internas Detectadas)")
        if dofa["Fortalezas"]:
            for f in dofa["Fortalezas"]: st.success(f)
        else: st.caption("No se detectaron fortalezas financieras críticas en este periodo.")
            
        st.markdown("#### ⚠️ Debilidades (Puntos Críticos de Control Interno)")
        if dofa["Debilidades"]:
            for d in dofa["Debilidades"]: st.warning(d)
        else: st.caption("¡Excelente! Ninguna debilidad financiera crítica fue arrojada por los indicadores.")
            
        st.markdown("#### 🌟 Oportunidades (Potencial de Crecimiento Estructural)")
        if dofa["Oportunidades"]:
            for o in dofa["Oportunidades"]: st.info(o)
        else: st.caption("No se habilitaron oportunidades automáticas por alta ocupación de pasivos.")
            
        st.markdown("#### 🔥 Amenazas (Riesgos Externos y Estructurales de Quiebra)")
        if dofa["Amenazas"]:
            for a in dofa["Amenazas"]: st.error(a)
        else: st.caption("¡Fantástico! No hay amenazas financieras latentes detectadas actualmente.")

    with col_matriz:
        st.subheader("📈 Matriz de Riesgo Financiero de Alto Contraste")
        fig, ax = plt.subplots(figsize=(6, 5))
        
        # COLORES VIVOS Y SÓLIDOS SOLICITADOS (Sin transparencias pálidas, Alpha = 0.95)
        ax.axvspan(0, 2.5, ymin=0, ymax=0.5, color='#2ECC71', alpha=0.95, label="Riesgo Aceptable")  # Verde Sólido Vivo
        ax.axvspan(2.5, 5.5, ymin=0, ymax=0.5, color='#F1C40F', alpha=0.95, label="Riesgo Tolerable") # Amarillo Sólido Vivo
        ax.axvspan(0, 2.5, ymin=0.5, ymax=1, color='#E67E22', alpha=0.95, label="Riesgo Alto")       # Naranja Sólido Vivo
        ax.axvspan(2.5, 5.5, ymin=0.5, ymax=1, color='#E74C3C', alpha=0.95, label="Riesgo Crítico")    # Rojo Sólido Vivo

        # Colores muy oscuros para los marcadores para que tengan contraste perfecto sobre los fondos encendidos
        colores_puntos = ['#1B2A47', '#0A3D62', '#3D0C5A', '#2C3E50', '#5C0612', '#0F141D']
        
        for (nombre, coords), color in zip(riesgos.items(), colores_puntos):
            ax.scatter(coords["X"], coords["Y"], s=260, label=nombre, c=color, edgecolors='#FFFFFF', linewidths=2.5, zorder=5)
            
            # Texto con contorno negro nítido para legibilidad total sobre los cuadrantes vivos
            txt = ax.annotate(nombre, (coords["X"], coords["Y"]), xytext=(8, 4), textcoords='offset points', fontweight='bold', fontsize=10, color='white')
            txt.set_path_effects([path_effects.withStroke(linewidth=3, foreground='black')])

        # Detalles Técnicos de la Rejilla
        ax.set_xlim(0, 5.5)
        ax.set_ylim(0, 5.5)
        ax.set_xlabel("Impacto Financiero (X)", fontweight='bold', fontsize=11, color='#222222')
        ax.set_ylabel("Probabilidad de Ocurrencia (Y)", fontweight='bold', fontsize=11, color='#222222')
        ax.set_xticks([1, 2, 3, 4, 5])
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.grid(True, linestyle='--', alpha=0.3, color='#FFFFFF', zorder=1)
        
        # Configuración Limpia de la Leyenda
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels[:4], handles[:4])) 
        ax.legend(by_label.values(), by_label.keys(), loc='upper left', bbox_to_anchor=(1, 1), frameon=True, facecolor='#FFFFFF', edgecolor='#CCCCCC')
        
        st.pyplot(fig)
