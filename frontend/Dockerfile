FROM node:22-alpine AS css-build

WORKDIR /build

COPY package.json package-lock.json ./
RUN npm ci

COPY src/input.css ./
COPY index.html app.js ./
RUN npx @tailwindcss/cli -i ./input.css -o /out/app.css --content ./index.html,./app.js

FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY index.html /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/

COPY --from=css-build /out/app.css /opt/assets/app.css

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
