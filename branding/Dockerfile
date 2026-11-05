ARG CHATWOOT_IMAGE=chatwoot/chatwoot:v4.19.1
FROM ${CHATWOOT_IMAGE}

ARG BRAND_NAME="Hospital Mandalore"
ARG LOGIN_TITLE="Hospital Mandalore Login"
ARG LOGO_VERSION=3

ENV CUSTOM_BRAND_NAME=${BRAND_NAME} \
    CUSTOM_LOGO_VERSION=${LOGO_VERSION}

COPY public/ /app/public/
COPY custom_branding.rb /app/config/initializers/zz_custom_branding.rb

# Título do login (string de i18n compilada no bundle) e defaults para instalações novas.
# O build falha se o texto original não for encontrado, sinal de que a versão mudou.
RUN set -e; \
    files=$(grep -lE "Entrar no Chatwoot|Login to Chatwoot" /app/public/vite/assets/*.js || true); \
    [ -n "$files" ] || { echo "Texto do login não encontrado no bundle"; exit 1; }; \
    for f in $files; do \
      sed -i -e "s/Entrar no Chatwoot/${LOGIN_TITLE}/g" -e "s/Login to Chatwoot/${LOGIN_TITLE}/g" "$f"; \
      rm -f "$f.gz" "$f.br"; \
    done; \
    for key in INSTALLATION_NAME BRAND_NAME; do \
      sed -i "/name: ${key}\$/,/value:/ s|value: .*|value: '${BRAND_NAME}'|" /app/config/installation_config.yml; \
    done
