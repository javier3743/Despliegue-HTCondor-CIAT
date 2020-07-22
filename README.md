# Despliegue HTCondor CIAT

### Pasos para realizar la simulación de la automatización del despliegue de HTCondor.

    vagrant up

Se crearán 3 maquinas virtuales donde se encuentran los nodos del cluster, `master1`, `node1`, `node2`. Este proceso realiza la configuración de cada uno de los nodos y instala las librerías requeridas por medio de los scripts de aprovisionamiento.

Ademas de la instalacion y configuracion de HTCondor, se realiza la configuración la herramienta de monitoreo tanto en los nodos de trabajo como en el principal. La herramienta queda disponible en el puerto 8000 del nodo `master1`.
