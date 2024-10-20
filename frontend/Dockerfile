FROM node:18
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"


RUN npm install -g http-server
RUN npm install -g pnpm@8.1.0 

WORKDIR /app


COPY . . 
RUN pnpm install

ENV NODE_OPTIONS="--max_old_space_size=10240"
RUN pnpm run build
FROM docker.io/nginx:1.21.1-alpine
WORKDIR /www
# COPY /app/dist /www
COPY --from=0 /app/dist /www

COPY conf.d/* /etc/nginx/conf.d/
#CMD [ "pnpm", "run", "dev" ]
EXPOSE 3000
