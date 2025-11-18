import streamlit as st

# --- Estructura de Descartos y Pasos ---
# Contiene el tema como clave y una lista de pasos/descartes como valor.
DESCARTES_POR_TEMA = {
    "Instalación de Software": [
        "Validar si la aplicación solicitada cumple con el VoBo de aprobación o si es solicitada por el jefe inmediato.",
        "Verificar si es un usuario nuevo (las aplicaciones las instala Carvajal al preparar el equipo).",
        "Si es una aplicación existente, se instala desde N1. Si es nueva, se escala a N2 para el VoBo del analista de seguridad.",
        "Si el software es ESET, validar que esté correctamente instalado y funcional (es responsabilidad de Infraestructura).",
        "Si es cambio de equipo, validar que el usuario haya pasado la lista de aplicaciones a Carvajal."
    ],
    "Directorio Activo (DA) - Bloqueo de Usuario de Red": [
        "Orientar al usuario para que espere **6 minutos** después del bloqueo.",
        "Si el bloqueo persiste después de **10 minutos**, escalar a N2 para el desbloqueo."
    ],
    "Directorio Activo (DA) - Restablecimiento de Contraseñas": [
        "Validar que el usuario que solicita el restablecimiento **coincida** con el usuario de red (para garantizar que no se soliciten claves ajenas).",
        "Tener presente que estos pedidos no pueden hacerse en fin de semana, salvo urgencia manifiesta con previa autorización del jefe inmediato."
    ],
    "Asignación de Carpetas Compartidas": [
        "Verificar que la solicitud provenga del jefe inmediato o cuente con su aprobación.",
        "La solicitud debe anexar la ruta de la carpeta o un usuario de referencia, e informar el tipo de permisos que se necesitan.",
        "Validar las últimas capacitaciones de Infraestructura sobre qué servidores necesitan permisos en VPN."
    ],
    "Recuperación de Carpetas": [
        "Solicitar al usuario que indique la **ruta de referencia** de la carpeta perdida, el **nombre** de la carpeta y la **fecha aproximada** de recuperación.",
        "Informar que los restablecimientos de carpetas se reescriben **mensualmente**.",
        "Validar con N2 para descartar que la carpeta haya sido movida.",
        "Si no se halla, proceder con la solicitud al proveedor indicando los datos anexados por el usuario."
    ],
    "Sedes sin Servicio (Navegación de Internet)": [
        "Asegurar que se hayan realizado los **descartes de N1** (la mesa de servicios cuenta con un manual).",
        "Si es necesario, activar el canal de cobre.",
        "Escalar a Infraestructura (N2)."
    ],
    "Intermitencias y Lentitud en la Navegación": [
        "Sacar las **evidencias** necesarias (por parte de N1).",
        "Escalar el reporte a N2 para seguimiento conjunto con el proveedor e identificar la causa."
    ],
    "Falla Extensión (Telefonía HCS)": [
        "Asegurar que la falla llegue con los **descartes de N1** (cuentan con manual) antes de ser atendida por el analista encargado en N2."
    ],
    "Fallas de Impresoras": [
        "Asegurar que la solicitud cuente con la **evidencia** del fallo.",
        "El personal de N1 debe realizar los **descartes iniciales** e intentar dar solución.",
        "Si no se resuelve, anexar las pruebas y los pasos realizados al N2."
    ],
    "Office (Falla Persistente)": [
        "El N1 debe realizar la **validación inicial**.",
        "Si la falla persiste, escalar a N2 con las evidencias y procesos realizados en N1."
    ],
    "Office (Licencia)": [
        "El caso debe ser escalado a N2, y este a su vez escalará a **Carvajal** (encargado de activar la licencia)."
    ],
    "Sistema Operativo (Falla)": [
        "El N1 debe tomar **pruebas** y realizar **descartes** para la solución de la falla.",
        "Si la falla persiste, escalar a N2, y el técnico procederá con el escalamiento a **Carvajal**."
    ],
}

def main():
    st.title("🛠️ Guía de Descartos Básicos (N1/Mesa de Servicios)")
    st.subheader("Selecciona el tema de la solicitud o incidente para ver los pasos a seguir.")
    
    # Selector de tema
    temas = ["Seleccione un Tema"] + list(DESCARTES_POR_TEMA.keys())
    tema_seleccionado = st.selectbox("Tema de la Solicitud:", temas)

    if tema_seleccionado != "Seleccione un Tema":
        st.markdown("---")
        st.markdown(f"## Pasos/Descartes para **{tema_seleccionado}**")
        
        pasos = DESCARTES_POR_TEMA[tema_seleccionado]
        
        # Mostrar los descartes/pasos
        st.info("Sigue los siguientes pasos en orden y valida su cumplimiento:")
        
        # Usamos un formulario para asegurar que la validación se realice antes de enviar
        with st.form(key='descartes_form'):
            todos_validados = True
            
            # Checkbox para cada paso de descarte
            st.markdown("### Checklist de Descartes")
            for i, paso in enumerate(pasos):
                # El estado del checkbox se guarda en 'st.session_state'
                # La clave única se construye con el índice y el nombre del tema
                checkbox_key = f"paso_{tema_seleccionado}_{i}"
                if checkbox_key not in st.session_state:
                    st.session_state[checkbox_key] = False

                st.session_state[checkbox_key] = st.checkbox(paso, key=checkbox_key)
                
                if not st.session_state[checkbox_key]:
                    todos_validados = False

            st.markdown("---")

            # Campo de comentario obligatorio
            st.markdown("### 📝 Comentarios y Resultado de la Validación")
            comentario = st.text_area(
                "Describe los resultados obtenidos en cada descarte o los pasos adicionales realizados (Obligatorio):", 
                height=150
            )

            # Botón de envío
            submit_button = st.form_submit_button(label='Finalizar Validación')

            if submit_button:
                # Lógica de validación al presionar el botón
                if not comentario:
                    st.error("🚨 **Error:** El campo de comentarios es obligatorio. Por favor, describe la validación realizada.")
                elif not todos_validados:
                    # Si el comentario existe pero no todos los pasos están validados
                    st.warning("⚠️ **Advertencia:** No has marcado todos los pasos de descarte. Asegúrate de haber completado la validación o explica por qué no fue posible en los comentarios.")
                    st.markdown("---")
                    st.success("✅ Validación de Descarte Guardada.")
                    st.markdown("### Resumen del Caso")
                    st.write(f"**Tema:** {tema_seleccionado}")
                    st.write("**Descartes Pendientes:** No todos los pasos fueron marcados.")
                    st.write("**Comentarios del Técnico:**")
                    st.code(comentario)

                else:
                    # Si todo está completo
                    st.success("🎉 **Validación Completa y Exitosa.** Todos los descartes realizados y documentados.")
                    st.markdown("### Resumen del Caso")
                    st.write(f"**Tema:** {tema_seleccionado}")
                    st.write("**Descartes Pendientes:** Ninguno.")
                    st.write("**Comentarios del Técnico:**")
                    st.code(comentario)
                    
                    # Opcional: Aquí podrías agregar lógica para guardar el resumen en un archivo o base de datos.
    else:
        st.info("👆 Selecciona un tema en el menú desplegable para comenzar la guía de descartes.")


if __name__ == "__main__":
    main()
