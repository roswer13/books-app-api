# Escabilidad

Imagina que en esta aplicación adicionalmente se quiere tener métricas de
lectura basadas en eventos y está siendo utilizada por un millón de usuarios
simultáneos.

---

1. **¿Cómo gestionarías esta cantidad de datos a nivel técnico?**

 - Usaria una arquitetura basada en eventos (Event-driven architecture) para
   gestionar la cantidad de datos. Utilizaría un sistema de mensajería como
   Kafka o RabbitMQ para manejar los eventos de lectura de una pagina en tiempo real.
 - Aplicaria una escabilidad horizonal usabdo Kuberbenetes y balancedores ELB. Así
   podría separa por microservicios, por ejemplo autenticación, libros, metricas, etc.
 - Si tubiera que procesar muchos datos, usaría Celery para manejar tareas
   asíncronas y distribuir la carga de trabajo entre varios workers en segundo plano.
 - Usaria el Caching de algunos endpoints para evitar consultas innecesarias a la
   base de datos. Podría usar Redis para almacenar en caché los
   resultados de las consultas más frecuentes.

---

2. **¿Qué tipo de base de datos utilizarías para almacenar las métricas de lectura de los usuarios? ¿Por qué?**

- Usaria ClickHouse para almacenar las métricas de lectura de los usuarios. Es eficiente
  para consultas de analtícas de mucho volumen.

---

3. **¿Has trabajado con alguna base de datos o infraestructura que soporte un volumen alto de usuarios y qué tecnologías utilizaste**

- He tarbajado con PostgreSQL y Redis en mi ultimo puesto de trabajo. Usamos PostgreSQL
  para almacenar los datos de la aplicación y Redis para almacenar en caché los
  resultados de las consultas más frecuentes.

---