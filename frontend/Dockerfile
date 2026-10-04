FROM node:18-alpine

WORKDIR /app

# Copia primeiro o package.json para aproveitar o cache de camadas do
# Docker: as dependências só são reinstaladas se este arquivo mudar.
COPY package.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
