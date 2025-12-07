# --- Stage 1: Build (збираємо Vue) ---
# Використовуємо нову версію, щоб не було помилок
FROM node:22-alpine as build-stage

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# --- Stage 2: Production (роздаємо Nginx) ---
FROM nginx:stable-alpine as production-stage

# Копіюємо зібрані файли сайту
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Копіюємо наш файл налаштувань (Gzip, Cache)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]