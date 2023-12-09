FROM  postgres:15.5
WORKDIR /postgres

ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=postgres
ENV PGUSER=postgres

# TODO not to be committed in PROD ...
ENV POSTGRES_HOST_AUTH_METHOD=trust


COPY ./init.sql /docker-entrypoint-initdb.d/